"""Compute R&D cost shares by industry-year from tidy h-27."""
import sys, pandas as pd, numpy as np
d = pd.read_csv(sys.argv[1], dtype={"sic": str})
w = d.pivot_table(index=["year", "section", "label", "sic", "src_row"], columns="variable", values="value", aggfunc="first", dropna=False).reset_index()
w = w[w.total.notna() | w.wages.notna() | w.get("wages_se").notna()]
dollar = w.year.isin([1962, 1972, 1973, 1974, 1975, 1976, 1977, 1979, 1981, 1983])
comp = ["wages_se", "wages_support", "wages", "depreciation", "materials", "other"]
for c in comp:
    if c not in w: w[c] = np.nan
w["wages_all"] = w.wages.fillna(w.wages_se + w.wages_support)
pct_scale = np.where(w[["wages_all", "materials", "other"]].sum(axis=1, min_count=1) < 1.5, 1.0, 100.0)  # fractions vs percent
for c in ["wages_all", "wages_se", "wages_support", "depreciation", "materials", "other"]:
    w["s_" + c.replace("wages_all", "labor")] = np.where(dollar, w[c] / w.total, w[c] / pct_scale)
w["s_sum"] = w[["s_labor", "s_depreciation", "s_materials", "s_other"]].sum(axis=1, min_count=1)
w = w.sort_values(["section", "src_row", "year"])
w.to_csv(sys.argv[2], index=False)
print(w[w.label.isin(["All industries", "Manufacturing"]) & (w.section == "industry")]
      .drop_duplicates(["year", "label"])[["year", "label", "total", "s_labor", "s_materials", "s_other", "s_depreciation", "s_sum"]]
      .pivot(index="year", columns="label", values=["total", "s_labor", "s_sum"]).round(3).to_string())
print("rows", len(w), "| s_sum outside [0.97,1.03]:", ((w.s_sum - 1).abs() > 0.03).sum(), "of", w.s_sum.notna().sum())
