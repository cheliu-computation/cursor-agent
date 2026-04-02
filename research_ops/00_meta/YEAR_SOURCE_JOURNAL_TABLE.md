# 年份 × 来源渠道 × 期刊类型 统计表

## 期刊类型定义（三类 + 补充）

优先级：**算法类 → Nature/通用高影响 → 医学类 → 预印本 → 其他**（避免 “Nature Medicine” 被宽泛 `medicine` 词误分）。

| 类型 | 含义 | 规则要点 |
|------|------|----------|
| **算法/ML/CV** | 算法、机器学习、计算机视觉路线 | venue 含 NeurIPS/ICML/ICLR/CVPR/ICCV/ECCV 等；或 `tags_modality` 为 machine_learning / computer_vision；或 `tags_method` 为 deep_learning、transformers、segmentation 等；或 `source_batch` 含上述会议缩写 |
| **医学/临床/影像** | 临床医学与医学影像应用 | venue 含 Radiology、Lancet、NEJM、MedIA、IEEE TMI、clinical、pathology 等；或 `tags_modality` 含 clinical_*、medical_imaging、radiology、pathology 等 |
| **通用高影响/Nature系** | Nature / Science / Cell / npj 等综合刊与交叉科学 | venue 含 nature、science、cell、npj、PNAS 等；或批次名含对应前缀（且 venue 非明显专科影像刊） |
| **预印本/未细分** | 主要为 arXiv 等预印本、尚未被上类规则吸收 | arXiv venue 或 preprint 标签 |
| **其他/混合** | 不满足以上 | — |

## 数据来源（仅保留可读全文后）

- **PDF**：`pdf_extract_index.csv` 且 `has_body=yes` 且 **PDF 文件仍存在**。
- **HTML**：`html_readable_index.csv` 且 **HTML 文件仍存在**（去标签后 ≥200 字符）。
- **XML**：Europe PMC `fullTextXML`，**T205_*.xml / T211_*.xml 文件仍存在**。

- **统计条数**（PDF/HTML/XML 分别计数，同一篇可多种形式）：**2085**

## 表 1：按年份 × 来源大类（篇数，便于阅读）

| 年份 | Europe PMC（病例XML） | Europe PMC（论文XML） | Frontiers | HAL | HTML（缓存全文页） | IEEE | Springer/Nature/BMC | arXiv | bioRxiv | medRxiv | 机构库及其他主机 | **合计** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 0 | 0 | 0 | 0 | 21 | 0 | 0 | 82 | 0 | 0 | 0 | **103** |
| 2019 | 0 | 0 | 0 | 0 | 46 | 0 | 0 | 90 | 0 | 0 | 0 | **136** |
| 2020 | 0 | 0 | 0 | 1 | 42 | 0 | 0 | 112 | 0 | 0 | 1 | **156** |
| 2021 | 0 | 0 | 0 | 0 | 57 | 0 | 0 | 123 | 0 | 0 | 1 | **181** |
| 2022 | 0 | 0 | 0 | 0 | 68 | 0 | 0 | 168 | 0 | 0 | 3 | **239** |
| 2023 | 0 | 13 | 0 | 2 | 9 | 8 | 113 | 218 | 0 | 0 | 3 | **366** |
| 2024 | 0 | 15 | 2 | 3 | 36 | 16 | 138 | 185 | 1 | 0 | 9 | **405** |
| 2025 | 0 | 12 | 0 | 0 | 200 | 48 | 130 | 59 | 3 | 1 | 5 | **458** |
| 2026 | 20 | 0 | 0 | 0 | 1 | 20 | 0 | 0 | 0 | 0 | 0 | **41** |

<details>
<summary>表 1b：按年份 × 细粒度主机（展开）</summary>

| 年份 | Cambridge | Europe_PMC_XML | Europe_PMC_XML_case | Frontiers | HAL | HTML_cache | IEEE | JMIR | Springer/Nature/BMC | Thieme | aaltodoc.aalto.fi | arXiv | assets.cureus.com | biblio.ugent.be | bioRxiv | cris.maastrichtuniversity.nl | discovery.dundee.ac.uk | doras.dcu.ie | liu.diva-portal.org | medRxiv | pubs.usgs.gov | pure-oai.bham.ac.uk | pure.amsterdamumc.nl | repository.ubn.ru.nl | traffic.libsyn.com | unsworks.unsw.edu.au | www.jstage.jst.go.jp | www.osti.gov | www.repository.cam.ac.uk | www.zora.uzh.ch | **合计** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 0 | 0 | 0 | 0 | 0 | 21 | 0 | 0 | 0 | 0 | 0 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **103** |
| 2019 | 0 | 0 | 0 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 0 | 90 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **136** |
| 2020 | 0 | 0 | 0 | 0 | 1 | 42 | 0 | 0 | 0 | 0 | 0 | 112 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **156** |
| 2021 | 0 | 0 | 0 | 0 | 0 | 57 | 0 | 0 | 0 | 0 | 1 | 123 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **181** |
| 2022 | 0 | 0 | 0 | 0 | 0 | 68 | 0 | 0 | 0 | 0 | 0 | 168 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | **239** |
| 2023 | 0 | 13 | 0 | 0 | 2 | 9 | 8 | 0 | 113 | 0 | 0 | 218 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | **366** |
| 2024 | 0 | 15 | 0 | 2 | 3 | 36 | 16 | 1 | 138 | 0 | 0 | 185 | 1 | 0 | 1 | 1 | 2 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **405** |
| 2025 | 1 | 12 | 0 | 0 | 0 | 200 | 48 | 0 | 130 | 1 | 0 | 59 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | **458** |
| 2026 | 0 | 0 | 20 | 0 | 0 | 1 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **41** |

</details>


## 表 2：按年份 × 期刊类型（各来源合并）

| 年份 | 算法/ML/CV | 医学/临床/影像 | 通用高影响/Nature系 | 预印本/未细分 | 其他/混合 | **合计** |
|---|---|---|---|---|---|---|
| 2018 | 103 | 0 | 0 | 0 | 0 | **103** |
| 2019 | 136 | 0 | 0 | 0 | 0 | **136** |
| 2020 | 156 | 0 | 0 | 0 | 0 | **156** |
| 2021 | 181 | 0 | 0 | 0 | 0 | **181** |
| 2022 | 237 | 0 | 2 | 0 | 0 | **239** |
| 2023 | 201 | 0 | 79 | 86 | 0 | **366** |
| 2024 | 298 | 8 | 99 | 0 | 0 | **405** |
| 2025 | 379 | 0 | 79 | 0 | 0 | **458** |
| 2026 | 5 | 36 | 0 | 0 | 0 | **41** |

## 表 3：按来源渠道 × 期刊类型（全时期）

| 来源渠道 | 算法/ML/CV | 医学/临床/影像 | 通用高影响/Nature系 | 预印本/未细分 | 其他/混合 | **合计** |
|---|---|---|---|---|---|---|
| Cambridge | 1 | 0 | 0 | 0 | 0 | **1** |
| Europe_PMC_XML | 36 | 0 | 4 | 0 | 0 | **40** |
| Europe_PMC_XML_case | 0 | 20 | 0 | 0 | 0 | **20** |
| Frontiers | 2 | 0 | 0 | 0 | 0 | **2** |
| HAL | 6 | 0 | 0 | 0 | 0 | **6** |
| HTML_cache | 446 | 2 | 32 | 0 | 0 | **480** |
| IEEE | 77 | 15 | 0 | 0 | 0 | **92** |
| JMIR | 1 | 0 | 0 | 0 | 0 | **1** |
| Springer/Nature/BMC | 152 | 7 | 222 | 0 | 0 | **381** |
| Thieme | 1 | 0 | 0 | 0 | 0 | **1** |
| aaltodoc.aalto.fi | 1 | 0 | 0 | 0 | 0 | **1** |
| arXiv | 951 | 0 | 0 | 86 | 0 | **1037** |
| assets.cureus.com | 1 | 0 | 0 | 0 | 0 | **1** |
| biblio.ugent.be | 1 | 0 | 0 | 0 | 0 | **1** |
| bioRxiv | 4 | 0 | 0 | 0 | 0 | **4** |
| cris.maastrichtuniversity.nl | 1 | 0 | 0 | 0 | 0 | **1** |
| discovery.dundee.ac.uk | 2 | 0 | 0 | 0 | 0 | **2** |
| doras.dcu.ie | 1 | 0 | 0 | 0 | 0 | **1** |
| liu.diva-portal.org | 1 | 0 | 0 | 0 | 0 | **1** |
| medRxiv | 1 | 0 | 0 | 0 | 0 | **1** |
| pubs.usgs.gov | 1 | 0 | 0 | 0 | 0 | **1** |
| pure-oai.bham.ac.uk | 1 | 0 | 0 | 0 | 0 | **1** |
| pure.amsterdamumc.nl | 1 | 0 | 0 | 0 | 0 | **1** |
| repository.ubn.ru.nl | 1 | 0 | 0 | 0 | 0 | **1** |
| traffic.libsyn.com | 1 | 0 | 0 | 0 | 0 | **1** |
| unsworks.unsw.edu.au | 1 | 0 | 0 | 0 | 0 | **1** |
| www.jstage.jst.go.jp | 1 | 0 | 0 | 0 | 0 | **1** |
| www.osti.gov | 1 | 0 | 1 | 0 | 0 | **2** |
| www.repository.cam.ac.uk | 1 | 0 | 0 | 0 | 0 | **1** |
| www.zora.uzh.ch | 1 | 0 | 0 | 0 | 0 | **1** |
