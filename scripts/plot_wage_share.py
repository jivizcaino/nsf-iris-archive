"""Small multiples: R&D wage share by harmonized industry, 1962-2008.

Wage share = wages of R&D personnel / total R&D cost (fringe benefits excluded; the only
definition common to SIC and NAICS years). Usage: python3 plot_wage_share.py <iris_root>
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(sys.argv[1])
SAVE_FIGURES = True
OUT = ROOT / "figures"; OUT.mkdir(exist_ok=True)

SERIES = "#2a78d6"     # categorical slot 1
REF = "#9b9a94"        # neutral reference (all industries)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"

# (hid, panel title, recommendation from the crosswalk)
PANELS = [
    ("H00", "All industries", "link"), ("HM", "Manufacturing", "link"), ("HN", "Nonmanufacturing", "link"),
    ("H05", "Chemicals", "link"), ("H10", "Fabricated metals", "link"), ("H12", "Computers and electronics", "link"),
    ("H17", "Aerospace", "link"), ("H22", "Transportation equipment", "link"), ("H01", "Food and tobacco", "care"),
    ("H11", "Machinery, except computers", "care"), ("H15", "Electrical equipment", "care"),
    ("H08", "Stone, clay, and glass", "care"), ("H19a", "Measuring instruments", "care"),
    ("H21", "SIC 35, 36, 38 aggregate", "care"), ("H09", "Primary metals", "care"),
]

w = pd.read_csv(ROOT / "data" / "panel_harmonized_rd_cost_shares.csv")
w = w[w.year.le(2008) & w.s_wages.notna()]
ref = w[w.hid.eq("H00")]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(5, 3, figsize=(7.5, 9.5), sharex=True, sharey=True)
for ax, (hid, title, rec) in zip(axes.flat, PANELS):
    x = w[w.hid.eq(hid)]
    ax.axvline(1998.5, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
    for cls in ("SIC", "NAICS"):
        r = ref[ref.classification.eq(cls)].sort_values("year")
        if hid != "H00":
            ax.plot(r.year, r.s_wages, color=REF, lw=1.2, zorder=2)
        s = x[x.classification.eq(cls)].sort_values("year")
        seg = (s.year.diff() > 2).cumsum()  # break the line across gaps (withheld years)
        for _, g in s.groupby(seg):
            ax.plot(g.year, g.s_wages, color=SERIES, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter(s.year, s.s_wages, s=9, color=SERIES, edgecolor="white", linewidth=0.6, zorder=4)
    ax.set_title(title + ("†" if rec == "care" else ""), loc="left", fontsize=8.5, color=INK, pad=3)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_ylim(0.1, 0.8); ax.set_xlim(1960, 2010)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8]); ax.set_xticks([1965, 1980, 1995, 2008])
for ax in axes[:, 0]:
    ax.set_ylabel("Wage share")
fig.tight_layout(h_pad=1.2, w_pad=0.8)

if SAVE_FIGURES:
    fig.savefig(OUT / "wage_share_by_industry_1962_2008.png", dpi=200)
    fig.savefig(OUT / "wage_share_by_industry_1962_2008.pdf")
print("saved", OUT)
