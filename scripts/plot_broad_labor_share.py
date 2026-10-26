"""Small multiples: broad R&D labour share by industry (NAICS), 2008-2023.

Broad share = (salaries, wages, fringe benefits + stock-based compensation + temporary staffing) / total R&D cost.
Each panel also shows the wages-and-fringe share; the gap between the two lines is stock pay plus temporary staff.
Usage: python3 plot_broad_labor_share.py <iris_root>
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

ROOT = Path(sys.argv[1])
SAVE_FIGURES = True
OUT = ROOT / "figures"; OUT.mkdir(exist_ok=True)

BROAD, NARROW = "#2a78d6", "#eb6834"   # categorical slots 1 and 2
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"

PANELS = [
    ("H00", "All industries"), ("HM", "Manufacturing"), ("HN", "Nonmanufacturing"),
    ("H05", "Chemicals"), ("H05b", "Pharmaceuticals"), ("H05a", "Industrial chemicals"),
    ("H11", "Machinery, except computers"), ("H12", "Computers and other electronics"), ("H13", "Communications equipment"),
    ("H14", "Semiconductors"), ("H19a", "Measuring instruments"), ("H15", "Electrical equipment"),
    ("H17", "Aerospace"), ("H16", "Motor vehicles"), ("H10", "Fabricated metals"),
    ("HN1", "Software and computer services"), ("HN2", "Scientific R&D services"), ("HN5", "Finance, insurance, real estate"),
]

w = pd.read_csv(ROOT / "data" / "panel_harmonized_rd_cost_shares.csv")
w = w[w.classification.eq("NAICS") & w.year.between(2008, 2023)]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(6, 3, figsize=(7.5, 11.3), sharex=True, sharey=True)
for ax, (hid, title) in zip(axes.flat, PANELS):
    x = w[w.hid.eq(hid)].sort_values("year")
    for col, color in (("s_wages_fringe", NARROW), ("s_labor_broad", BROAD)):
        s = x[x[col].notna()]
        for _, g in s.groupby((s.year.diff() > 1).cumsum()):  # break across withheld years
            ax.plot(g.year, g[col], color=color, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter(s.year, s[col], s=9, color=color, edgecolor="white", linewidth=0.6, zorder=4)
    ax.set_title(title, loc="left", fontsize=8.5, color=INK, pad=3)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_ylim(0.3, 1.0); ax.set_xlim(2007, 2024)
    ax.set_yticks([0.4, 0.6, 0.8, 1.0]); ax.set_xticks([2008, 2013, 2018, 2023])
for ax in axes[:, 0]:
    ax.set_ylabel("Share of R&D cost")
handles = [Line2D([], [], color=BROAD, lw=2, marker="o", ms=3, label="Wages, fringe, stock pay, temporary staff"),
           Line2D([], [], color=NARROW, lw=2, marker="o", ms=3, label="Wages and fringe benefits")]
fig.legend(handles=handles, loc="upper left", ncol=2, frameon=False, fontsize=8, bbox_to_anchor=(0.06, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.975), h_pad=1.2, w_pad=0.8)

if SAVE_FIGURES:
    fig.savefig(OUT / "broad_labor_share_by_industry_2008_2023.png", dpi=200)
    fig.savefig(OUT / "broad_labor_share_by_industry_2008_2023.pdf")
print("saved")
