#!/usr/bin/env python3
"""Shared HTTP headers and source-specific fetch policy helpers."""
from __future__ import annotations

import os
import re
from urllib.parse import urlparse

CONTACT_EMAIL = os.environ.get("RESEARCH_OPS_CONTACT_EMAIL", "").strip()

# Browser-like headers reduce avoidable 403s on OA landing pages while still
# identifying the client as a research automation workflow.
BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36 research-ops/1.0"
)

# For APIs that want a contact channel (e.g. Crossref), prefer a real email via
# RESEARCH_OPS_CONTACT_EMAIL. Fall back to a plain agent string instead of an
# invalid placeholder domain.
API_UA = (
    f"research-ops/1.0 (mailto:{CONTACT_EMAIL})"
    if CONTACT_EMAIL
    else "research-ops/1.0"
)

HIGH_FRICTION_DOI_PREFIXES = (
    "10.1016/",  # Elsevier / Cell / Lancet families
    "10.1056/",  # NEJM
    "10.1001/",  # JAMA
    "10.1148/",  # RSNA
)

HIGH_FRICTION_HOSTS = {
    "www.cell.com",
    "www.thelancet.com",
    "pubs.rsna.org",
    "www.biorxiv.org",
    "www.medrxiv.org",
    "jamanetwork.com",
    "www.nejm.org",
    "www.mdpi.com",
    "academic.oup.com",
    "onlinelibrary.wiley.com",
    "www.sciencedirect.com",
    "www.science.org",
    "www.bmj.com",
    "dl.acm.org",
    "syndication.highwire.org",
    "diabetesjournals.org",
    "pmc.ncbi.nlm.nih.gov",
    "nottingham-repository.worktribe.com",
    "ir.ymlib.yonsei.ac.kr",
    "digitalcommons.library.tmc.edu",
    "pubs.acs.org",
    "www.tandfonline.com",
    "www.dovepress.com",
    "ieeexplore.ieee.org",
    "linkinghub.elsevier.com",
}

PREPRINT_MODALITY_TAGS = {
    "preprint_broad",
    "preprint_biorxiv",
    "preprint_medrxiv",
}


def browser_headers(accept: str | None = None) -> dict[str, str]:
    return {
        "User-Agent": BROWSER_UA,
        "Accept": accept or "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "no-cache",
    }


def api_headers() -> dict[str, str]:
    return {
        "User-Agent": API_UA,
        "Accept": "application/json,text/plain;q=0.9,*/*;q=0.8",
    }


def canonicalize_url(url: str) -> str:
    url = url.strip()
    if url.startswith("http://doi.org/"):
        return "https://doi.org/" + url.removeprefix("http://doi.org/")
    if url.startswith("http://dx.doi.org/"):
        return "https://doi.org/" + url.removeprefix("http://dx.doi.org/")
    return url


def classify_policy_skip(url: str, doi: str = "") -> str | None:
    """Return a stable skip reason for URLs we should not hammer directly."""
    parsed = urlparse(canonicalize_url(url))
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    doi = doi.strip().lower().removeprefix("https://doi.org/")

    if host in {"doi.org", "dx.doi.org"} and doi.startswith(HIGH_FRICTION_DOI_PREFIXES):
        return "doi_landing_high_friction_publisher"

    if host in {"doi.org", "dx.doi.org"} and doi.startswith("10.1101/"):
        return "preprint_doi_filtered"

    if host in {"www.cell.com", "www.thelancet.com"} and path.endswith("/pdf"):
        return "publisher_pdf_blocked"

    if host == "pubs.rsna.org" and ("/doi/pdf/" in path or path.startswith("/doi/")):
        return "publisher_landing_high_friction"

    if host in {"pmc.ncbi.nlm.nih.gov"} and "/pdf/" in path:
        return "pmc_direct_pdf_prefer_article"

    if host in {"www.biorxiv.org", "www.medrxiv.org"} and path.endswith(".full.pdf"):
        return "preprint_pdf_blocked"

    if host == "jamanetwork.com" and "/articlepdf/" in path:
        return "publisher_pdf_blocked"

    if host == "www.nejm.org" and "/doi/pdf/" in path:
        return "publisher_pdf_blocked"

    if host == "www.mdpi.com" and "/pdf" in path:
        return "low_priority_publisher_pdf_blocked"

    return None


def classify_terminal_error(url: str, err: str, doi: str = "") -> str | None:
    """Return a policy skip reason for terminal fetch errors unlikely to recover."""
    msg = (err or "").lower()
    parsed = urlparse(canonicalize_url(url))
    host = parsed.netloc.lower()
    doi = doi.strip().lower().removeprefix("https://doi.org/")

    if "403" in msg or "forbidden" in msg:
        if host in HIGH_FRICTION_HOSTS:
            return "blocked_by_publisher"
        if host in {"doi.org", "dx.doi.org"} and doi.startswith(HIGH_FRICTION_DOI_PREFIXES):
            return "doi_landing_high_friction_publisher"
        if host in {"doi.org", "dx.doi.org"} and doi.startswith("10.1101/"):
            return "preprint_doi_filtered"
    if host == "hdl.handle.net" and (
        "connection reset" in msg or "500" in msg or "404" in msg
    ):
        return "repository_handle_unstable"
    return None


def allow_arxiv_fallback(
    url: str,
    year: str,
    venue: str,
    doi: str,
    tags_modality: str,
) -> bool:
    """Allow arXiv only as a recent fallback for non-preprint primary records.

    Policy:
    - default: filter arXiv/preprint full-text fetches out
    - allow only if the record is recent and appears to have a non-preprint
      primary venue / DOI, so arXiv acts as a fallback copy rather than the
      main discovery source
    """
    host = urlparse(canonicalize_url(url)).netloc.lower()
    if "arxiv.org" not in host:
        return True

    year = (year or "").strip()
    venue_low = (venue or "").lower()
    doi_low = (doi or "").lower()
    modality_tags = {
        t.strip()
        for t in (tags_modality or "").split("|")
        if t.strip()
    }

    if modality_tags & PREPRINT_MODALITY_TAGS:
        return False
    if "arxiv" in venue_low:
        return False

    try:
        y = int(year)
    except ValueError:
        return False

    # Only keep very recent fallback paths where a publisher-backed record exists.
    if y < 2024:
        return False
    if not doi_low or doi_low.startswith("10.48550/arxiv."):
        return False
    return True


def url_attempts(primary: str) -> list[str]:
    """Ordered URL attempts: HTML/XML landing variants first, then raw URL."""
    primary = canonicalize_url(primary)
    seen: set[str] = set()
    out: list[str] = []
    for candidate in _known_landing_variants(primary) + _expand_arxiv(primary):
        if candidate and candidate not in seen:
            seen.add(candidate)
            out.append(candidate)
    if primary not in seen:
        out.append(primary)
    return out


def _known_landing_variants(url: str) -> list[str]:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path
    variants: list[str] = []

    # Prefer the PMC article page over direct PDF paths.
    m = re.match(r"^/articles/(PMC\d+)/pdf/[^/]+$", path)
    if host == "pmc.ncbi.nlm.nih.gov" and m:
        variants.append(f"https://pmc.ncbi.nlm.nih.gov/articles/{m.group(1)}/")

    # bioRxiv / medRxiv direct PDF links often have an HTML abstract/full page.
    if host in {"www.biorxiv.org", "www.medrxiv.org"} and path.endswith(".full.pdf"):
        base = url[: -len(".full.pdf")]
        variants.extend([base + ".abstract", base + ".full", base])

    # RSNA often blocks direct PDF URLs but allows landing/full pages.
    if host == "pubs.rsna.org" and "/doi/pdf/" in path:
        variants.append(url.replace("/doi/pdf/", "/doi/full/", 1))
        variants.append(url.replace("/doi/pdf/", "/doi/", 1))

    # Cell / Lancet direct /pdf URLs may have an article landing page at the
    # same path without the trailing /pdf.
    if host in {"www.cell.com", "www.thelancet.com"} and path.endswith("/pdf"):
        variants.append(url[:-4])

    return variants


def _expand_arxiv(url: str) -> list[str]:
    aid = arxiv_id_from_url(url)
    if not aid:
        return []
    ulow = url.lower()
    if "arxiv.org/pdf/" in ulow or "export.arxiv.org" in ulow:
        return [
            f"https://arxiv.org/abs/{aid}",
            f"https://export.arxiv.org/pdf/{aid}.pdf",
        ]
    if "arxiv.org/abs/" in ulow:
        return [f"https://export.arxiv.org/pdf/{aid}.pdf"]
    return []


def arxiv_id_from_url(url: str) -> str | None:
    u = canonicalize_url(url).split("?", 1)[0].strip()
    m = re.search(r"arxiv\.org/(?:pdf|abs)/([^/]+?)(?:\.pdf)?$", u, re.I)
    if m:
        return m.group(1).rstrip("/")
    m = re.search(r"doi\.org/10\.48550/arxiv\.(.+)$", u, re.I)
    if m:
        return m.group(1).rstrip("/")
    return None
