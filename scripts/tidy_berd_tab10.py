"""Tidy table 10 (domestic R&D performed by the company, all funders, by type of cost) for BRDIS/BRDS/BERD 2015-2023."""
import sys, glob, re
import pandas as pd

ROOT, OUT = sys.argv[1], sys.argv[2]
KEYS = [("Total", "total"), ("Salaries", "salaries_wages_fringe"), ("Stock", "stock_comp"), ("Temporary", "temp_staffing"),
        ("Expensed", "expensed_equipment"), ("Materials", "materials"), ("Lease", "lease_rental"), ("Depreciation", "depreciation"),
        ("Royalties", "royalties"), ("Other purchased", "other_purchased_services"), ("Other", "other")]
rows = []
for y in range(2015, 2024):
    f = glob.glob(f"{ROOT}/y{y}/*tab010.xlsx")[0]
    d = pd.read_excel(f, header=None)
    h = next(r for r in range(2, 10) if str(d.iloc[r, 0]).startswith("Industry"))
    cols = {}
    for c in range(2, d.shape[1]):
        lab = d.iloc[h, c]
        if pd.isna(lab): continue
        lab = re.sub(r"\s+", " ", str(lab))
        cols[next(n for k, n in KEYS if lab.startswith(k))] = c
    for r in range(h + 1, len(d)):
        lab = d.iloc[r, 0]
        if pd.isna(lab): continue
        lab = re.sub(r"\s+", " ", str(lab)).strip()
        if lab.startswith(("All companies", "Small companies", "Medium companies", "Large companies")) or re.match(r"^[\d,–-]+", lab):
            break  # company-size block follows the industry block
        naics = d.iloc[r, 1]
        for nm, c in cols.items():
            v = d.iloc[r, c]
            fl = d.iloc[r, c + 1] if c + 1 < d.shape[1] and c + 1 not in cols.values() else None
            vs = str(v).strip()
            rows.append(dict(year=y, label=lab,
                             naics=None if pd.isna(naics) else re.sub(r"\s+", " ", str(naics)).strip(), variable=nm,
                             value=pd.to_numeric(vs.replace(",", ""), errors="coerce"),
                             flag=(" ".join(x for x in [vs if vs in ("D", "*", "-") else "", "" if fl is None or pd.isna(fl) else str(fl).strip()] if x)),
                             src_row=r + 1))
long = pd.DataFrame(rows)
long.to_csv(OUT, index=False)
w = long.pivot_table(index=["year", "naics", "label"], columns="variable", values="value", aggfunc="first").reset_index()
w["s_labor_narrow"] = w.salaries_wages_fringe / w.total
w["s_labor_broad"] = w[["salaries_wages_fringe", "stock_comp", "temp_staffing"]].sum(axis=1, min_count=3) / w.total
w.to_csv(OUT.replace("_long", "_shares"), index=False)
print(long.shape, long.year.value_counts().sort_index().to_dict())
print(w[w.label.isin(["All industries", "Manufacturing industries", "Nonmanufacturing industries"])].pivot(index="year", columns="label", values=["s_labor_narrow", "s_labor_broad"]).round(3).to_string())
