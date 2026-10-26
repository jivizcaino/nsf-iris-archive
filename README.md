# IRIS archive: download and first inventory

Source: NSF Industrial Research and Development Information System (IRIS), Archive-It collection 5902, snapshot of 3 October 2018.
URL: https://wayback.archive-it.org/5902/20181003221605/https://www.nsf.gov/statistics/iris/

## Contents of the archive

- One publication per survey year, 1953 to 2007, about 2,600 Excel tables in total.
- Industry classification: SIC through 1998, NAICS from 1999 to 2007.
- Longitudinal tables (`excel-files/historical_tables/h-*.xls`), one per topic, cover 1953 to 1998 (SIC only). NAICS years have no longitudinal tables.
- Archive-It allows roughly one request every 1 to 7 minutes, so the crawl is slow. It fetches priority topics first.

## Folders

- `raw/pages/`: downloaded files, named after their path on the original site (`/` replaced by `_`). For example, `excel-files_nsf_2007_36.xls` is `excel-files/nsf_2007/36.xls`.
- `raw/logs/crawl2_log.tsv`: one line per fetched file (priority, HTTP status, type, bytes, file, original URL).
- `raw/logs/state2.json`: crawler state (files seen and queue), used to resume.
- `scripts/crawl2.py`: resumable crawler. `scripts/run_crawl.sh` restarts it until done. `scripts/sync_repo.sh` pushes progress here.
- `scripts/tidy_h27.py`, `scripts/shares_h27.py`: extraction of table h-27.
- `data/`: tidy outputs.

The crawl is in progress. This repository is updated every few hours until it finishes.

## Table h-27: R&D cost by type, by industry and company size, 1962 to 1998

Files: `data/h27_type_of_cost_1962_98_long.csv` (long format, with disclosure flags) and `data/h27_cost_shares_1962_98.csv` (cost shares).

- Years: 1962 to 1977, 1979 to 1997 every other year, and 1998. Not collected in 1978, 1980, ..., 1996.
- Cost types: total, wages, materials and supplies, other. Wages are split into scientists and engineers versus supporting personnel before 1976. Depreciation is separate only in 1998.
- Units: total in millions of dollars. Components in millions of dollars in 1962, 1972 to 1977, 1979, 1981, 1983, and in percent of total in all other years. The 1985 dollar total is blank in the source.
- Detailed nonmanufacturing industries are available only from 1995.
- Flags: D = withheld for confidentiality, S = more than 50 percent imputed, T = included in total only, NA = not available. Components sum to 100 percent in 810 of 836 industry-year rows. The rest have withheld cells.

Labour (wage) share of total R&D cost, all industries:

| 1962 | 1965 | 1970 | 1975 | 1979 | 1983 | 1985 | 1989 | 1993 | 1997 | 1998 |
|---|---|---|---|---|---|---|---|---|---|---|
| 47.5 | 50.0 | 50.0 | 49.5 | 45.7 | 45.6 | 43.0 | 39.9 | 42.3 | 47.0 | 48.0 |

## Table 36, 2007 (NAICS)

File: `raw/pages/excel-files_nsf_2007_36.xls`.

- Cost types: wages, employer cost of fringe benefits, materials and supplies, depreciation, other. Wages 46.7 percent and fringe benefits 10.1 percent of total in 2007.
- Type-of-cost data come only from Form RD-1, the questionnaire sent to larger R&D performers. The cost-type universe is therefore smaller than total industrial R&D. This also explains why h-27 totals fall below published total industrial R&D in early years.
- Industry estimates from 2004 onward are not directly comparable with earlier years (change in the method that assigns industry codes).

## BRDIS, BRDS, and BERD, 2015 to 2023

All Excel data tables for each year are in `raw_brdis_berd/<year>/`. Sources (NCSES report numbers): 2015 NSF 18-313, 2016 NSF 19-318 (BRDIS); 2017 NSF 20-311, 2018 NSF 21-312 (BRDS); 2019 NSF 22-329, 2020 NSF 23-314, 2021 NSF 23-351, 2022 NSF 24-335, 2023 NSF 25-354 (BERD). Table numbers differ by year; table 10 (type of cost) is the same in every year.

Panel extract of table 10, 2015 to 2023: `data/berd_tab10_type_of_cost_2015_2023_long.csv` (long, with flags) and `data/berd_tab10_type_of_cost_2015_2023_shares.csv` (shares). The cost items are identical across years, except that royalties and licensing fees start in 2016.

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| Salaries, wages, fringe / total | 57.4 | 57.4 | 57.8 | 56.2 | 54.4 | 55.8 | 54.7 | 53.5 | 53.7 |
| Adding stock pay and temporary staff | 66.9 | 67.6 | 68.0 | 66.9 | 66.6 | 69.2 | 69.4 | 68.3 | 69.7 |

The 2008 to 2014 BRDIS reports are only on Archive-It. They are queued in the crawler.

### BERD 2023 table guide (NSF 25-354)

Extract of table 10 for 2023 only: `data/berd2023_tab10_type_of_cost.csv`.

Tables relevant to the panel, all by NAICS industry (about 70 rows, including detailed nonmanufacturing) and company size:

| Table | Content |
|---|---|
| 10 | Domestic R&D performed by the company, all funders, by type of cost. Same concept as IRIS cost-by-type tables. |
| 25, 32 | Same, company-funded and funded by others. |
| 45 | Capital expenditures, including domestic R&D capital expenditures by type of asset (flow, not stock). |
| 46, 47 | Total and R&D employment (headcount); R&D cost per R&D employee. |
| 52 | FTE R&D employees and FTE R&D scientists and engineers. Same FTE concept as SIRD up to 2007. |
| 65 | R&D, depreciation, R&D capital expenditures, and R&D adjusted for capitalization. |
| 57, 58 | R&D by industry, 2008 (or 2009) to 2023. |

Type-of-cost items in table 10: salaries, wages, and fringe benefits; stock-based compensation; temporary staffing; expensed equipment; materials and supplies; lease and rental; depreciation; royalties and licensing; other purchased services; other.

Labour share of total cost, all industries, 2023: 53.7 percent for salaries, wages, and fringe benefits; 69.7 percent adding stock-based compensation (11.7) and temporary staffing (4.2). Comparable 2007 SIRD figure: 56.8 percent (wages 46.7 plus fringe benefits 10.1). Stock-based compensation and temporary staffing are not separate items in SIRD; their treatment there must be checked in the technical notes.

## Industry panel

Built by `scripts/build_cost_panel.py` and `scripts/build_fte_panel.py`. The crawl was stopped after the 1999 to 2014 tables; the 2,123 pre-1999 single-year IRIS tables were not fetched, because the longitudinal tables cover 1953 to 1998.

### R&D cost by type, 1962 to 2023

- `data/panel_rd_cost_by_type_long.csv`: one row per classification, year, industry, and cost item, with the reported value, unit, disclosure flag, source file, and source row.
- `data/panel_rd_cost_shares.csv`: one row per classification, year, and industry. Dollar amounts (millions) where reported, and shares of total cost (`s_*`).

| Years | Classification | Source | Cost items | Unit of components |
|---|---|---|---|---|
| 1962 to 1998 | SIC | IRIS h-27 | wages (split by occupation before 1976), materials, depreciation (1998 only), other | dollars in 1962, 1972 to 1977, 1979, 1981, 1983; percent otherwise |
| 1999 to 2000 | NAICS | SIRD single-year tables | wages, materials, depreciation, other | percent |
| 2001 to 2007 | NAICS | SIRD single-year tables | wages, fringe benefits, materials, depreciation, other | percent |
| 2008 | NAICS | BRDIS (company-funded plus other-funded) | wages, fringe benefits, stock compensation, temporary staffing, expensed equipment, materials, lease, depreciation, other | dollars |
| 2009 to 2010 | NAICS | BRDIS (company-funded plus other-funded) | salaries, wages, and fringe combined; the 2008 items otherwise; other purchased services; allocated costs (2009) | dollars |
| 2011 to 2023 | NAICS | BRDIS, BRDS, BERD (all funders) | as 2010; royalties from 2016 | dollars |

Labour cost share, all industries (percent of total R&D cost):

| | 1962 | 1970 | 1980s low (1989) | 1998 | 1999 | 2002 | 2007 | 2008 | 2014 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Wages | 47.5 | 50.0 | 39.9 | 48.0 | 44.8 | 44.5 | 46.7 | 46.5 | | |
| Wages and fringe benefits | | | | | | 53.0 | 56.8 | 57.3 | 57.4 | 53.7 |
| Adding stock pay and temporary staff | | | | | | | | 62.4 | 66.4 | 69.7 |

Comparability:

1. Fringe benefits are reported separately from 2001. The fall in "other costs" between 2000 and 2002 (41.7 to 31.0 percent) matches the size of fringe benefits, so fringe benefits were part of "other costs" up to 2000. The 2001 fringe share (4.3 percent) looks incomplete; 2002 onward is about 9 to 11 percent.
2. Wages alone are reported up to 2008; salaries, wages, and fringe benefits are combined from 2009. The series that runs longest without a break in definition is wages alone, 1962 to 2008.
3. SIC to NAICS in 1999. IRIS has no SIC-NAICS crosswalk table for cost by type; the 1999 report (NSF 02-312) reclassifies 1997 and 1998 totals. A crosswalk of industries is not yet built.
4. NSF changed the method that assigns industry codes in 2004 (SIRD) and the survey changed in 2008 (BRDIS). At the all-industries level, the labour share moves smoothly across 2007 to 2008.
5. In 2008 to 2010 the all-funders figures are sums of the company-funded and other-funded tables. A total is rebuilt from components when the reported total is withheld and all components are reported (`total_computed`). Cells marked * (less than $0.5 million) are set to zero.
6. Rows whose shares do not sum to one have withheld components (flag D).

### FTE R&D scientists and engineers, 1954 to 2023

`data/panel_fte_rd_scientists_engineers_long.csv`: thousands, by classification, year, and industry. Variable `fte_se` (scientists and engineers) in all years; `fte_rd_emp` (all R&D employees) from 2011.

- 1954 to 1999 (SIC, IRIS h-19): FTE counted in January of the year after the survey year. Annual coverage from 1971 to 1999, with gaps before. Detailed nonmanufacturing industries from 1983. (S) marks cells withheld before 1993.
- 1999 to 2007 (NAICS, SIRD).
- 2008 to 2023 (NAICS, BRDIS, BRDS, BERD).

Break: the count falls from 1,130,500 in 2007 (SIRD) to 832,000 in 2008 (BRDIS). This reflects the change of survey and of the employment concept. The series must not be spliced across 2007 to 2008 without an adjustment.

## SIC to NAICS crosswalk

Built by `scripts/build_crosswalk.py`.

- `data/crosswalk_sic_naics_rd.csv`: 37 harmonized groups (all industries, manufacturing, nonmanufacturing, 28 manufacturing groups and aggregates, 7 nonmanufacturing groups). For each group: the IRIS SIC industries, SIC codes, the NAICS recipe, a definitional quality grade, the 1997-98 level check, the wage-share check, and a linking recommendation.
- `data/panel_harmonized_rd_cost_shares.csv`: R&D cost by type for each harmonized group and year, SIC years 1962-98 and NAICS years 1999-2023 (dollar amounts and shares; `built_from` records the codes used).
- `data/panel_harmonized_fte_se.csv`: FTE R&D scientists and engineers for each harmonized group and year.
- `data/crosswalk_check_1997_98.csv`: total R&D in 1997 and 1998 under both classifications.

Method:

1. NAICS recipes are signed sums of codes, tried in order; the first one whose codes are all reported in a year is used. Residual groups are built by subtraction (for example other chemicals = 325 - 3251 - 3252 - 3254), which handles the changing "other" categories in the NAICS tables. SIC groups are built the same way from IRIS labels; for example, transportation equipment before 1985 is the sum of its three subgroups.
2. Level check: NSF published 1997 and 1998 total R&D under NAICS (NSF 02-312, table A-3). The ratio of the NAICS to the SIC total is 1.00 for all industries and between 0.95 and 1.13 for food, primary metals, fabricated metals, machinery, computers, measuring instruments, aerospace, transportation equipment, and scientific R&D services. Ratios far from one (electrical equipment 0.5, medical and photographic equipment 0.57, wood 0.74, trade 1.45, health 0.51) reflect companies moving between industries: NSF assigns each company to one industry, so the change of classification moved whole firms.
3. Share check: the wage share averaged over 1995-98 (SIC) against 1999-2002 (NAICS).
4. Recommendation: "link" when the level ratio is within 0.85-1.15 and the wage-share gap is under 0.05; "link with care" when one of the two holds; "no overlap evidence" when NSF withheld the overlap cells; "do not link" otherwise.

Groups recommended for a series from 1962: all industries, chemicals, fabricated metal products, computers and other electronics (from 1972), aerospace, transportation equipment (from 1972); with care, food, machinery except computers, electrical equipment, stone-clay-glass, measuring instruments, and the aggregate of SIC 35, 36, and 38. Primary metals passes the level check but its wage share jumps from 0.51 to 0.73 in 1999, as reported by NSF. Nonmanufacturing groups have SIC data only from 1995 and are of limited use for a long series.

The wage share alone (excluding fringe benefits) is the measure available on both sides, 1962-2008. Wages and fringe benefits are combined from 2009.

## Figure: R&D wage share by industry, 1962 to 2008

`figures/wage_share_by_industry_1962_2008.png` and `.pdf`, produced by `scripts/plot_wage_share.py` from `data/panel_harmonized_rd_cost_shares.csv`.

Caption: Wages of R&D personnel as a share of total R&D cost, by harmonized industry group (blue), against all industries (gray). Fringe benefits excluded. SIC classification through 1998 and NAICS from 1999 (dashed line); the two segments are not joined. Data are biennial from 1977 to 1997; lines break where NSF withheld or did not report a year. The 1985 group values use IRIS h-25 total R&D as weights, because h-27 reports no dollar totals for 1985. † marks groups whose SIC-NAICS link is recommended with care (see `data/crosswalk_sic_naics_rd.csv`). Source: NSF Survey of Industrial Research and Development (IRIS h-27; SIRD 1999-2007) and BRDIS 2008.

## Figure: R&D wages-and-fringe share by industry, 2002 to 2023

`figures/wages_fringe_share_by_industry_2002_2023.png` and `.pdf`, produced by `scripts/plot_wages_fringe_share.py` from `data/panel_harmonized_rd_cost_shares.csv` (NAICS side).

Caption: Wages and fringe benefits of R&D personnel as a share of total R&D cost, by industry (blue), against all industries (gray). 2002-08: sum of the two reported items; from 2009 NSF reports them as one item. Stock-based compensation and temporary staffing (reported from 2008) are excluded. The dashed line marks the change from SIRD to BRDIS between 2007 and 2008; the two segments are not joined. Lines break where NSF withheld a year. Source: NSF SIRD 2002-07, BRDIS 2008-16, BRDS 2017-18, BERD 2019-23.

## Figure: broad R&D labour share by industry, 2008 to 2023

`figures/broad_labor_share_by_industry_2008_2023.png` and `.pdf`, produced by `scripts/plot_broad_labor_share.py` from `data/panel_harmonized_rd_cost_shares.csv` (NAICS side).

Caption: Share of total R&D cost, by industry. Blue: salaries, wages, fringe benefits, stock-based compensation, and temporary staffing. Orange: salaries, wages, and fringe benefits. The gap between the lines is stock-based compensation plus temporary staffing. Lines break where NSF withheld a year; the blue line is missing more often because stock pay and temporary staffing are withheld more often. Source: NSF BRDIS 2008-16, BRDS 2017-18, BERD 2019-23.

## Open questions

1. How SIRD treated stock-based compensation and temporary staff before 2008 (wages, other costs, or not counted).
2. Coverage of Form RD-1 by year, to compare the cost-type universe with total industrial R&D before 2008.
