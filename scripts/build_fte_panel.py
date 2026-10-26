"""Build an industry-by-year panel of full-time-equivalent (FTE) R&D scientists and engineers, 1954-2023.

Sources
  1954-99  IRIS longitudinal table h-19 (SIC), thousands, January of the year after the survey year
  1999-2007 IRIS single-year SIRD tables (NAICS), thousands
  2008-23  BRDIS/BRDS/BERD tables (NAICS), thousands; from 2011 also FTE R&D employees (all occupations)

Usage: python3 build_fte_panel.py <iris_root>
"""
import re, sys, glob
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from build_cost_panel import read_table, parse_value  # noqa: E402

ROOT = Path(sys.argv[1])
P = ROOT / "crawl" / "pages"
OUT = ROOT / "data"

TABLES = {  # year: (file, code column, {variable: column})
    1999: ("excel-files_nsf_02-312_a-38.xls", 1, dict(fte_se=2)),
    2000: ("excel-files_nsf_03-318_a-33.xls", 5, dict(fte_se=7)),
    2001: ("excel-files_nsf_05-305_a-37.xls", 1, dict(fte_se=2)),
    2002: ("excel-files_nsf_06-322_41.xls", 1, dict(fte_se=2)),
    2003: ("excel-files_nsf_07-314_42.xls", 1, dict(fte_se=2)),
    2004: ("excel-files_nsf_09-301_37.xls", 1, dict(fte_se=2)),
    2005: ("excel-files_nsf_10-319_37.xls", 1, dict(fte_se=2)),
    2006: ("excel-files_nsf_2006_28.xls", 1, dict(fte_se=2)),
    2007: ("excel-files_nsf_2007_67.xls", 1, dict(fte_se=2)),
    2008: ("brdis/nsf13332_tables_tab31.xls", 1, dict(fte_se=2)),
    2009: ("brdis/nsf13332_tables_tab80.xls", 1, dict(fte_se=2)),
    2010: ("brdis/nsf13332_tables_tab124.xls", 1, dict(fte_se=2)),
    2011: ("brdis/2015_nsf15307_tables_tab37.xlsx", 1, dict(fte_rd_emp=2, fte_se=11)),
    2012: ("brdis/2016_nsf16301_tables_tab50.xlsx", 1, dict(fte_rd_emp=2, fte_se=11)),
    2013: ("brdis/2016_nsf16313_tables_tab59.xlsx", 1, dict(fte_rd_emp=2, fte_se=11)),
    2014: ("brdis/2018_nsf18302_tables_tab53.xlsx", 1, dict(fte_rd_emp=2, fte_se=11)),
}
BERD = {2015: "tab056", 2016: "tab059", 2017: "tab059", 2018: "tab059", 2019: "tab061",
        2020: "tab053", 2021: "tab053", 2022: "tab053", 2023: "tab052"}


def sic_h19():
    d = pd.read_excel(P / "excel-files_historical_tables_h-19.xls", header=None)
    hdr = list(d.index[d[0].astype(str).str.contains("Industry and size", na=False)]) + [len(d)]
    rows = []
    for a, b in zip(hdr[:-1], hdr[1:]):
        for lab_c, code_c, ycols in ((0, 1, range(2, 21)), (21, 22, range(23, d.shape[1]))):
            years = {c: int(str(d.iloc[a, c])[:4]) for c in ycols if pd.notna(d.iloc[a, c])}
            section = "industry"; pending = ""
            for r in range(a + 1, b):
                lab = d.iloc[r, lab_c]
                if pd.isna(lab):
                    continue
                lab = " ".join(re.sub(r"[.…]{2,}.*$", "", str(lab)).split())
                lab = re.sub(r"(\D)\d,?$", r"\1", lab).rstrip(",").strip() if not lab.endswith(" and") else lab
                if "size of company" in lab.lower() or lab.startswith("[Number"):
                    section = "size"; continue
                if lab.startswith(("Distribution by", "See explanatory", "Number of full", "Total (")):
                    continue
                vals = {y: parse_value(d.iloc[r, c]) for c, y in years.items()}
                if all(np.isnan(v) and not f for v, f in vals.values()):
                    pending = (pending + " " + lab) if (pending and lab[:1].islower()) else lab
                    continue
                if pending and lab[:1].islower():
                    lab = pending + " " + lab
                pending = ""
                code = d.iloc[r, code_c]
                for y, (v, f) in vals.items():
                    rows.append(dict(classification="SIC", year=y, label=lab, section=section,
                                     code=None if pd.isna(code) else str(code).strip(), variable="fte_se",
                                     value=v, flag=f, source="IRIS h-19", src_row=r + 1))
    out = pd.DataFrame(rows)
    out["label"] = out["label"].str.replace(r"(?<=[a-z])\d+$", "", regex=True)
    out = out[out.section.eq("industry")].drop(columns="section")
    return out.drop_duplicates(["year", "label", "code"], keep="first")


def naics():
    rows = []
    for y, (f, code_col, cols) in TABLES.items():
        rows += read_table(P / f, code_col, cols, y, f)
    for y, t in BERD.items():
        f = glob.glob(str(ROOT / "berd" / f"y{y}" / f"*{t}.xlsx"))[0]
        rows += read_table(Path(f), 1, dict(fte_rd_emp=2, fte_se=10), y, Path(f).name)
    d = pd.DataFrame(rows)
    d["classification"] = "NAICS"
    d["label"] = d["label"].map(lambda x: " ".join(str(x).split()))
    return d


if __name__ == "__main__":
    long = pd.concat([sic_h19(), naics()], ignore_index=True)
    long["unit"] = "thousands"
    long = long[["classification", "year", "code", "label", "variable", "value", "unit", "flag", "source", "src_row"]]
    long.to_csv(OUT / "panel_fte_rd_scientists_engineers_long.csv", index=False)
    a = long[long.label.eq("All industries")].pivot_table(index=["classification", "year"], columns="variable", values="value", aggfunc="first")
    print(long.shape); print(a.to_string())
