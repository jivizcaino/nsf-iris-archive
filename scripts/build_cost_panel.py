"""Build an industry-by-year panel of R&D costs by type, 1962-2023.

Sources
  1962-98  IRIS longitudinal table h-27 (SIC), tidy file from tidy_h27.py
  1999-2007 IRIS single-year SIRD tables (NAICS), percent of total cost
  2008-10  BRDIS: company-funded plus other-funded tables (NAICS), $ millions
  2011-14  BRDIS: all-funders table (NAICS), $ millions
  2015-23  BRDIS/BRDS/BERD table 10 (NAICS), $ millions

Usage: python3 build_cost_panel.py <iris_root>
"""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1])
PAGES = ROOT / "crawl" / "pages"
OUT = ROOT / "data"

# Column positions (0-based) of each cost item in each table; flags sit in the next column.
IRIS = {
    1999: ("excel-files_nsf_02-312_a-34.xls", 1, dict(total=2, wages=3, materials=4, depreciation=5, other=6)),
    2000: ("excel-files_nsf_03-318_a-29.xls", 5, dict(total=7, wages=9, materials=11, depreciation=13, other=15)),
    2001: ("excel-files_nsf_05-305_a-33.xls", 1, dict(total=2, wages=4, fringe=6, materials=8, depreciation=10, other=12)),
    2002: ("excel-files_nsf_06-322_7.xls", 1, dict(total=3, wages=5, fringe=7, materials=9, depreciation=11, other=13)),
    2003: ("excel-files_nsf_07-314_7.xls", 1, dict(total=2, wages=4, fringe=6, materials=8, depreciation=10, other=12)),
    2004: ("excel-files_nsf_09-301_6.xls", 1, dict(total=2, wages=5, fringe=7, materials=9, depreciation=11, other=13)),
    2005: ("excel-files_nsf_10-319_6.xls", 1, dict(total=2, wages=6, fringe=8, materials=10, depreciation=12, other=14)),
    2006: ("excel-files_nsf_2006_6.xls", 1, dict(total=2, wages=5, fringe=7, materials=9, depreciation=11, other=13)),
    2007: ("excel-files_nsf_2007_36.xls", 1, dict(total=2, wages=6, fringe=8, materials=10, depreciation=12, other=14)),
}
B08 = dict(total=2, wages=4, fringe=6, stock_comp=8, temp_staffing=10, expensed_equipment=12, materials=14,
           lease_rental=16, depreciation=18, other=20)
B09 = dict(total=2, salaries_wages_fringe=4, stock_comp=6, temp_staffing=8, expensed_equipment=10, materials=12,
           lease_rental=14, depreciation=16, other_purchased_services=18, allocated_costs=20, other=22)
B10 = dict(total=2, salaries_wages_fringe=4, stock_comp=6, temp_staffing=8, expensed_equipment=10, materials=12,
           lease_rental=14, depreciation=16, other_purchased_services=18, other=20)
BRDIS = {
    2008: [("brdis/nsf13332_tables_tab06.xls", B08), ("brdis/nsf13332_tables_tab18.xls", B08)],
    2009: [("brdis/nsf13332_tables_tab55.xls", B09), ("brdis/nsf13332_tables_tab67.xls", B09)],
    2010: [("brdis/nsf13332_tables_tab99.xls", B10), ("brdis/nsf13332_tables_tab110.xls", B10)],
    2011: [("brdis/2015_nsf15307_tables_tab10.xlsx", B10)],
    2012: [("brdis/2016_nsf16301_tables_tab11.xlsx", B10)],
    2013: [("brdis/2016_nsf16313_tables_tab18.xlsx", B10)],
    2014: [("brdis/2018_nsf18302_tables_tab12.xlsx", B10)],
}
SIZE_ROW = re.compile(r"^\s*(\d|fewer|all companies|small compan|medium compan|large compan|company size|size of compan|\[)", re.I)


def parse_value(v):
    """Return (number, flag) from a cell such as 182823, '(S) 44.8', 'D', '(D)', '*', 'i'."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return np.nan, ""
    if isinstance(v, (int, float, np.integer, np.floating)):
        return float(v), ""
    s = str(v).strip()
    flags = re.findall(r"\(([A-Z])\)|\b(D|NA|S|T)\b|(\*)", s)
    flag = " ".join(a or b or c for a, b, c in flags)
    num = re.sub(r"\([A-Z]\)|\bNA\b|[,*]|\b[DST]\b", "", s).strip()
    if not num and "*" in flag:
        return 0.0, flag
    try:
        return float(num), flag
    except ValueError:
        return np.nan, flag


def read_table(path, code_col, cols, year, source):
    d = pd.read_excel(path, header=None)
    first = d.index[d.iloc[:, :code_col].astype(str).apply(lambda r: r.str.strip().str.startswith("All industries")).any(axis=1)][0]
    rows = []
    pending = ""
    for r in range(first, len(d)):
        labs = [str(x) for x in d.iloc[r, :code_col].tolist() if pd.notna(x) and str(x).strip()]
        if not labs:
            continue
        lab = " ".join(re.sub(r"[.…]{2,}.*$", "", labs[0]).split())
        if r > first + 10 and SIZE_ROW.match(lab):
            break
        has_data = any(pd.notna(d.iloc[r, c]) and str(d.iloc[r, c]).strip() for c in cols.values())
        if pending and lab[:1].islower():
            lab = pending + " " + lab
        pending = ""
        if not has_data:
            pending = lab
            continue
        code = d.iloc[r, code_col]
        code = None if pd.isna(code) else re.sub(r"\s+", " ", str(code)).strip()
        for var, c in cols.items():
            val, flag = parse_value(d.iloc[r, c])
            nxt = d.iloc[r, c + 1] if c + 1 < d.shape[1] and (c + 1) not in cols.values() else None
            if nxt is not None and pd.notna(nxt) and str(nxt).strip():
                flag = (flag + " " + str(nxt).strip()).strip()
            rows.append(dict(year=year, label=lab, code=code, variable=var, value=val, flag=flag,
                             source=source, src_row=r + 1))
    return rows


def iris_naics():
    rows = []
    for y, (f, code_col, cols) in IRIS.items():
        for rec in read_table(PAGES / f, code_col, cols, y, f):
            rec["unit"] = "usd_millions" if rec["variable"] == "total" else "pct_of_total"
            rows.append(rec)
    return pd.DataFrame(rows)


def brdis():
    rows = []
    for y, parts in BRDIS.items():
        for f, cols in parts:
            code_col = 1
            rows += [dict(r, unit="usd_millions") for r in read_table(PAGES / f, code_col, cols, y, f)]
    d = pd.DataFrame(rows)
    # 2008-10: add company-funded and other-funded parts; keep the cell flags of both parts.
    g = d.groupby(["year", "code", "label", "variable"], dropna=False, sort=False)
    out = g.agg(value=("value", lambda s: s.sum(min_count=len(s))), flag=("flag", lambda s: " ".join(x for x in s if x)),
                source=("source", lambda s: "+".join(sorted(set(s)))), src_row=("src_row", "first"), unit=("unit", "first")).reset_index()
    return out


def berd():
    d = pd.read_csv(OUT / "berd_tab10_type_of_cost_2015_2023_long.csv", dtype={"naics": str})
    d = d.rename(columns={"naics": "code"})
    d["unit"] = "usd_millions"
    d["source"] = "BERD/BRDS/BRDIS table 10"
    return d


def sic():
    d = pd.read_csv(OUT / "h27_type_of_cost_1962_98_long.csv", dtype={"sic": str})
    d = d[d.section == "industry"].rename(columns={"sic": "code"}).drop(columns=["section", "indent"])
    d["source"] = "IRIS h-27"
    d.loc[d.variable.isin(["wages_se", "wages_support"]), "variable"] = d.variable  # kept as reported
    return d


def to_wide(long):
    """Industry-year rows with dollar amounts and shares of total cost."""
    idx = ["classification", "year", "code", "label"]
    l = long.copy()
    l["code"] = l["code"].fillna("")
    tot = l[l.variable.eq("total")].set_index(idx)["value"].rename("tot")
    l = l.join(tot, on=idx)
    l["share"] = np.where(l.unit.eq("pct_of_total"), l.value / 100.0, l.value / l.tot)
    w = l.pivot_table(index=idx, columns="variable", values="value", aggfunc="first", dropna=False).reset_index()
    s = l[l.variable.ne("total")].pivot_table(index=idx, columns="variable", values="share", aggfunc="first", dropna=False)
    s.columns = ["s_" + c for c in s.columns]
    w = w.join(s, on=idx)
    w = w[w.drop(columns=idx).notna().any(axis=1)]
    comp_d = ["salaries_wages_fringe", "stock_comp", "temp_staffing", "expensed_equipment", "materials", "lease_rental",
              "depreciation", "royalties", "other_purchased_services", "allocated_costs", "other"]
    dollar_rows = w.year >= 2008
    for y in sorted(w.year[dollar_rows].unique()):
        m = (w.year == y) & w.total.isna()
        if y == 2008:
            use = ["wages", "fringe", "stock_comp", "temp_staffing", "expensed_equipment", "materials", "lease_rental", "depreciation", "other"]
        else:
            use = [c for c in comp_d if c in w and l[(l.year == y) & l.variable.eq(c)].shape[0] > 0]
        mask = m & w[use].notna().all(axis=1)
        w.loc[mask, "total"] = w[use].sum(axis=1)[mask]
        w.loc[mask, "total_computed"] = True
        for c in use:
            w.loc[(w.year == y) & w["s_" + c].isna(), "s_" + c] = w[c] / w.total
    # wages for SIC years before 1976 are split by occupation
    if "s_wages_se" in w:
        w["s_wages"] = w["s_wages"].fillna(w["s_wages_se"] + w["s_wages_support"])
    w["s_wages_fringe"] = w.get("s_salaries_wages_fringe")
    w["s_wages_fringe"] = w["s_wages_fringe"].fillna(w["s_wages"] + w["s_fringe"])
    w["s_labor_broad"] = w["s_wages_fringe"] + w["s_stock_comp"] + w["s_temp_staffing"]
    share_cols = [c for c in w.columns if c.startswith("s_") and c not in ("s_wages_fringe", "s_labor_broad", "s_sum")]
    base = [c for c in share_cols if c not in ("s_wages_se", "s_wages_support", "s_salaries_wages_fringe")]
    w["s_sum"] = w[base].sum(axis=1, min_count=1) + w["s_salaries_wages_fringe"].fillna(0)
    return w


if __name__ == "__main__":
    s = sic(); s["classification"] = "SIC"
    n = iris_naics(); n["classification"] = "NAICS"
    b = brdis(); b["classification"] = "NAICS"
    e = berd(); e["classification"] = "NAICS"
    long = pd.concat([s, n, b, e], ignore_index=True)[
        ["classification", "year", "code", "label", "variable", "value", "unit", "flag", "source", "src_row"]]
    long["label"] = long["label"].astype(str).map(lambda x: " ".join(x.split()))
    long = long.drop_duplicates(["classification", "year", "code", "label", "variable"], keep="first")
    long.to_csv(OUT / "panel_rd_cost_by_type_long.csv", index=False)
    w = to_wide(long)
    w.to_csv(OUT / "panel_rd_cost_shares.csv", index=False)
    print("long", long.shape, "wide", w.shape)
    tot = w[w.label.eq("All industries")].set_index("year")
    print(tot[["classification", "total", "s_wages", "s_fringe", "s_wages_fringe", "s_labor_broad", "s_materials", "s_depreciation", "s_other", "s_sum"]].round(3).to_string())
