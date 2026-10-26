"""Small multiples: R&D wages-and-fringe share by industry (NAICS), 2002-2023.

Share = (wages + fringe benefits of R&D personnel) / total R&D cost. 2002-08 sums the two items;
from 2009 NSF reports them combined. Usage: python3 plot_wages_fringe_share.py <iris_root>
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

SERIES = "#2a78d6"
REF = "#9b9a94"
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
w = w[w.classification.eq("NAICS") & w.year.between(2002, 2023) & w.s_wages_fringe.notna()]
ref = w[w.hid.eq("H00")].sort_values("year")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig, axes = plt.subplots(6, 3, figsize=(7.5, 11), sharex=True, sharey=True)
for ax, (hid, title) in zip(axes.flat, PANELS):
    ax.axvline(2007.5, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
    for era in ((2002, 2007), (2008, 2023)):  # survey change between 2007 and 2008: do not join
        r = ref[ref.year.between(*era)]
        if hid != "H00":
            ax.plot(r.year, r.s_wages_fringe, color=REF, lw=1.2, zorder=2)
        s = w[w.hid.eq(hid) & w.year.between(*era)].sort_values("year")
        for _, g in s.groupby((s.year.diff() > 1).cumsum()):  # break across withheld years
            ax.plot(g.year, g.s_wages_fringe, color=SERIES, lw=2, zorder=3, solid_capstyle="round")
        ax.scatter(s.year, s.s_wages_fringe, s=9, color=SERIES, edgecolor="white", linewidth=0.6, zorder=4)
    ax.set_title(title, loc="left", fontsize=8.5, color=INK, pad=3)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_ylim(0.2, 0.9); ax.set_xlim(2001, 2024)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8]); ax.set_xticks([2002, 2008, 2015, 2023])
for ax in axes[:, 0]:
    ax.set_ylabel("Wages and fringe share")
fig.tight_layout(h_pad=1.2, w_pad=0.8)

if SAVE_FIGURES:
    fig.savefig(OUT / "wages_fringe_share_by_industry_2002_2023.png", dpi=200)
    fig.savefig(OUT / "wages_fringe_share_by_industry_2002_2023.pdf")
print("saved")
