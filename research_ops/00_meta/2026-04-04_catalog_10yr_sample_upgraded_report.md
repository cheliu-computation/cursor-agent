# 升级版：全部期刊会议 10 年样本爬取成功率

日期：2026-04-04

## 升级策略

- 基于基线样本 `research_ops/02_papers/catalog_10yr_sample_status.csv` 做二次增强，不改变样本集合。
- 当 abstract 或正文缺失时，先看同一篇 work 的 `locations` / `best_oa_location`。
- 若仍缺失，再按标题搜索 OpenAlex 中的同题/同 DOI 备用版本，优先接受 arXiv、bioRxiv/medRxiv、ResearchGate、PMC/Europe PMC 与机构仓库副本。
- 升级后样本明细：`research_ops/02_papers/catalog_10yr_sample_status_upgraded.csv`。

## 总体对比

| 版本 | 样本数 | 标题成功率 | 摘要成功率 | 正文成功率 |
| --- | ---: | ---: | ---: | ---: |
| 基线 | 2923 | 2923/2923 (100.0%) | 1955/2923 (66.9%) | 1006/2923 (34.4%) |
| 升级后 | 2923 | 2923/2923 (100.0%) | 1970/2923 (67.4%) | 2827/2923 (96.7%) |

## 升级后分来源结果

| 来源类型 | 来源 | 样本数 | 标题成功率 | 摘要成功率 | 正文成功率 |
| --- | --- | ---: | ---: | ---: | ---: |
| conference | CVPR | 44 | 44/44 (100.0%) | 11/44 (25.0%) | 36/44 (81.8%) |
| conference | ECCV | 11 | 11/11 (100.0%) | 3/11 (27.3%) | 11/11 (100.0%) |
| conference | ICCV | 16 | 16/16 (100.0%) | 6/16 (37.5%) | 16/16 (100.0%) |
| conference | ICLR | 60 | 60/60 (100.0%) | 52/60 (86.7%) | 59/60 (98.3%) |
| conference | ICML | 60 | 60/60 (100.0%) | 43/60 (71.7%) | 60/60 (100.0%) |
| conference | IPMI | 0 | 0/0 (0.0%) | 0/0 (0.0%) | 0/0 (0.0%) |
| conference | ISBI | 3 | 3/3 (100.0%) | 1/3 (33.3%) | 3/3 (100.0%) |
| conference | MICCAI | 2 | 2/2 (100.0%) | 0/2 (0.0%) | 2/2 (100.0%) |
| conference | MIDL | 22 | 22/22 (100.0%) | 4/22 (18.2%) | 21/22 (95.5%) |
| conference | NeurIPS | 60 | 60/60 (100.0%) | 44/60 (73.3%) | 60/60 (100.0%) |
| journal | Artificial Intelligence Review | 110 | 110/110 (100.0%) | 45/110 (40.9%) | 110/110 (100.0%) |
| journal | BMJ | 0 | 0/0 (0.0%) | 0/0 (0.0%) | 0/0 (0.0%) |
| journal | Bioengineering | 110 | 110/110 (100.0%) | 110/110 (100.0%) | 110/110 (100.0%) |
| journal | Cell | 110 | 110/110 (100.0%) | 24/110 (21.8%) | 110/110 (100.0%) |
| journal | Cell Systems | 110 | 110/110 (100.0%) | 42/110 (38.2%) | 109/110 (99.1%) |
| journal | Communications Medicine | 60 | 60/60 (100.0%) | 60/60 (100.0%) | 60/60 (100.0%) |
| journal | Healthcare | 110 | 110/110 (100.0%) | 110/110 (100.0%) | 110/110 (100.0%) |
| journal | IEEE Access | 110 | 110/110 (100.0%) | 105/110 (95.5%) | 110/110 (100.0%) |
| journal | IEEE Transactions on Medical Imaging | 110 | 110/110 (100.0%) | 109/110 (99.1%) | 110/110 (100.0%) |
| journal | Information Fusion | 110 | 110/110 (100.0%) | 17/110 (15.5%) | 34/110 (30.9%) |
| journal | JAMA | 110 | 110/110 (100.0%) | 109/110 (99.1%) | 110/110 (100.0%) |
| journal | JAMA Network Open | 91 | 91/91 (100.0%) | 91/91 (100.0%) | 90/91 (98.9%) |
| journal | Medical Image Analysis | 110 | 110/110 (100.0%) | 26/110 (23.6%) | 109/110 (99.1%) |
| journal | Nature | 110 | 110/110 (100.0%) | 46/110 (41.8%) | 110/110 (100.0%) |
| journal | Nature Biomedical Engineering | 106 | 106/106 (100.0%) | 12/106 (11.3%) | 106/106 (100.0%) |
| journal | Nature Communications | 110 | 110/110 (100.0%) | 109/110 (99.1%) | 110/110 (100.0%) |
| journal | Nature Computational Science | 60 | 60/60 (100.0%) | 14/60 (23.3%) | 60/60 (100.0%) |
| journal | Nature Machine Intelligence | 90 | 90/90 (100.0%) | 27/90 (30.0%) | 90/90 (100.0%) |
| journal | Nature Medicine | 110 | 110/110 (100.0%) | 29/110 (26.4%) | 110/110 (100.0%) |
| journal | New England Journal of Medicine | 110 | 110/110 (100.0%) | 110/110 (100.0%) | 110/110 (100.0%) |
| journal | Radiology | 110 | 110/110 (100.0%) | 102/110 (92.7%) | 109/110 (99.1%) |
| journal | Radiology Artificial Intelligence | 80 | 80/80 (100.0%) | 72/80 (90.0%) | 77/80 (96.2%) |
| journal | Science | 110 | 110/110 (100.0%) | 110/110 (100.0%) | 110/110 (100.0%) |
| journal | Sensors | 110 | 110/110 (100.0%) | 110/110 (100.0%) | 110/110 (100.0%) |
| journal | The Lancet | 110 | 110/110 (100.0%) | 46/110 (41.8%) | 110/110 (100.0%) |
| journal | The Lancet Digital Health | 80 | 80/80 (100.0%) | 76/80 (95.0%) | 78/80 (97.5%) |
| journal | npj Digital Medicine | 98 | 98/98 (100.0%) | 95/98 (96.9%) | 97/98 (99.0%) |

## fallback 使用情况

- 摘要 fallback：
  - `alternate_version:arxiv.org`: 10
  - `alternate_version:doi.org`: 5
- 正文 fallback：
  - `alternate_location`: 1812
  - `primary_or_equivalent_location`: 9
- 命中的备用 host：
  - `doi.org`: 356
  - `ncbi.nlm.nih.gov`: 272
  - `pubmed.ncbi.nlm.nih.gov`: 272
  - `doaj.org`: 194
  - `export.arxiv.org`: 124
  - `hdl.handle.net`: 61
  - `pmc.ncbi.nlm.nih.gov`: 53
  - `proceedings.mlr.press`: 33
  - `openreview.net`: 26
  - `openaccess.thecvf.com`: 23
  - `kclpure.kcl.ac.uk`: 23
  - `escholarship.org`: 21
  - `papers.nips.cc`: 18
  - `dspace.library.uu.nl`: 15
  - `proceedings.neurips.cc`: 12
