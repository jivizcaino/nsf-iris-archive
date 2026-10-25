"""Tidy BERD 2023 table 10: domestic R&D performed by the company, all funders, by type of cost and industry."""
import sys, glob, re
import pandas as pd
src = glob.glob(f"{sys.argv[1]}/**/*tab010.xlsx", recursive=True)[0]
d = pd.read_excel(src, header=None)
names = ["total", "salaries_wages_fringe", "stock_comp", "temp_staffing", "expensed_equipment", "materials",
         "lease_rental", "depreciation", "royalties", "other_purchased_services", "other"]
rows = []
for r in range(4, len(d)):
    lab = d.iloc[r, 0]
    if pd.isna(lab) or str(lab).startswith(("All companies", "a ", "Note", "Source", "NOTES", "SOURCE")): continue
    rec = {"label": str(lab).strip(), "naics": None if pd.isna(d.iloc[r, 1]) else str(d.iloc[r, 1]).strip()}
    for k, nm in enumerate(names):
        v, f = d.iloc[r, 2 + 2 * k], d.iloc[r, 3 + 2 * k]
        rec[nm] = pd.to_numeric(v, errors="coerce"); rec[nm + "_flag"] = "" if pd.isna(f) else str(f).strip() or ("*" if str(v).strip() == "*" else "")
        if str(v).strip() in ("*", "D"): rec[nm + "_flag"] = (rec[nm + "_flag"] + " " + str(v).strip()).strip()
    rows.append(rec)
t = pd.DataFrame(rows)
t["s_labor_narrow"] = t.salaries_wages_fringe / t.total
t["s_labor_broad"] = t[["salaries_wages_fringe", "stock_comp", "temp_staffing"]].sum(axis=1, min_count=3) / t.total
t.to_csv(sys.argv[2], index=False)
print(t[["label", "naics", "total", "s_labor_narrow", "s_labor_broad"]].head(70).round(3).to_string())
