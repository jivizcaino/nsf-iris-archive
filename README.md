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

## Open questions

1. Whether "wages" in 1962 to 1998 includes fringe benefits, or whether fringe benefits sit in "other costs". The technical notes (`tn.doc`) for each year should settle this. They are in the crawl queue.
2. In which year fringe benefits first appear as a separate item (between 1999 and 2007).
3. Coverage of Form RD-1 by year, to compare the cost-type universe with total R&D.
