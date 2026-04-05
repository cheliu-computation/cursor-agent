#!/usr/bin/env python3
"""Helpers for the unified journal/conference fetch catalog."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HarvestSource:
    catalog_id: str
    source_name: str
    source_kind: str
    openalex_source_id: str
    openalex_display_name: str
    openalex_source_type: str
    fetch_mode: str
    enabled_for_harvest: bool
    priority: str
    notes: str


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def load_harvest_sources(
    catalog_path: Path,
    *,
    source_kind: str = "all",
    enabled_only: bool = True,
) -> list[HarvestSource]:
    rows: list[HarvestSource] = []
    with catalog_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            item = HarvestSource(
                catalog_id=(row.get("catalog_id") or "").strip(),
                source_name=(row.get("source_name") or "").strip(),
                source_kind=(row.get("source_kind") or "").strip(),
                openalex_source_id=(row.get("openalex_source_id") or "").strip(),
                openalex_display_name=(row.get("openalex_display_name") or "").strip(),
                openalex_source_type=(row.get("openalex_source_type") or "").strip(),
                fetch_mode=(row.get("fetch_mode") or "").strip(),
                enabled_for_harvest=_as_bool(row.get("enabled_for_harvest") or ""),
                priority=(row.get("priority") or "").strip(),
                notes=(row.get("notes") or "").strip(),
            )
            if enabled_only and not item.enabled_for_harvest:
                continue
            if source_kind != "all" and item.source_kind != source_kind:
                continue
            rows.append(item)
    return rows


def load_harvest_source_ids(
    catalog_path: Path,
    *,
    source_kind: str = "all",
) -> list[HarvestSource]:
    return [
        item
        for item in load_harvest_sources(catalog_path, source_kind=source_kind)
        if item.fetch_mode == "openalex_source_id" and item.openalex_source_id
    ]


def resolve_harvest_source(catalog_path: Path, token: str) -> HarvestSource:
    wanted = token.strip().casefold()
    if not wanted:
        raise ValueError("empty source token")

    matches = [
        item
        for item in load_harvest_sources(catalog_path, enabled_only=False)
        if wanted
        in {
            item.catalog_id.casefold(),
            item.source_name.casefold(),
            item.openalex_source_id.casefold(),
            item.openalex_display_name.casefold(),
        }
    ]
    if not matches:
        raise ValueError(f"unknown source token: {token}")
    if len(matches) > 1:
        names = ", ".join(sorted(item.source_name for item in matches))
        raise ValueError(f"ambiguous source token {token!r}: {names}")
    return matches[0]
