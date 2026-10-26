"""SIC-NAICS crosswalk for NSF industrial R&D statistics, and harmonized industry panels.

The crosswalk defines harmonized industry groups. Each group lists the SIC industries of the IRIS
longitudinal tables (1953-98) and a NAICS recipe for the SIRD/BRDIS/BERD tables (1999-2023).
A recipe is a list of alternatives; each alternative is a signed list of NAICS codes. For each year
the first alternative whose codes are all reported is used. Signed codes allow residual groups,
for example other chemicals = 325 - 3251 - 3252 - 3254.

The mapping is checked on 1997-98, the two years NSF published under both classifications
(SIC: IRIS h-27; NAICS: NSF 02-312 table A-3).

Usage: python3 build_crosswalk.py <iris_root>
"""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from build_cost_panel import read_table  # noqa: E402

ROOT = Path(sys.argv[1])
DATA = ROOT / "data"
PAGES = ROOT / "crawl" / "pages"

# hid, label, level, SIC labels (IRIS), SIC codes, NAICS recipe, quality, note
G = [
    ("H00", "All industries", "total", ["All industries"], "all", [[("+", "ALL")]], "exact", ""),
    ("HM", "Manufacturing", "sector", ["Manufacturing"], "20-39", [[("+", "MFG")]], "close",
     "SIC manufacturing includes oil and gas extraction (SIC 13) with petroleum refining; NAICS puts it in mining (21). Before 1995 the SIC manufacturing total is not reported in h-27."),
    ("HN", "Nonmanufacturing", "sector", ["Nonmanufacturing"], "non-20-39", [[("+", "NONMFG")]], "approximate",
     "SIC nonmanufacturing covered a short list of industries before 1991 (see h-27 footnote 4)."),
    ("H01", "Food, beverages, and tobacco", "industry", ["Food, kindred, and tobacco products"], "20-21",
     [[("+", "311"), ("+", "312")]], "close", "Tobacco (SIC 21) was in other manufacturing before 1984."),
    ("H02", "Textiles, apparel, and leather", "industry", ["Textiles and apparel"], "22-23",
     [[("+", "313-16")]], "close", "NAICS 316 (leather) was SIC 31, part of SIC other manufacturing."),
    ("H03", "Wood products and furniture", "industry", ["Lumber, wood products, and furniture"], "24-25",
     [[("+", "321"), ("+", "337")]], "close", ""),
    ("H04", "Paper", "industry", ["Paper and allied products"], "26",
     [[("+", "322")], [("+", "322, 323")]], "approximate",
     "1999-2007: NAICS reports paper and printing together (322, 323); printing (SIC 27) was SIC other manufacturing."),
    ("H05", "Chemicals", "industry", ["Chemicals and allied products"], "28", [[("+", "325")]], "close", ""),
    ("H05a", "Industrial chemicals", "detail", ["Industrial chemicals"], "281-82, 286",
     [[("+", "3251"), ("+", "3252")]], "close", "Agricultural chemicals (SIC 287, NAICS 3253) are in other chemicals on both sides."),
    ("H05b", "Pharmaceuticals", "detail", ["Drugs and medicines"], "283", [[("+", "3254")]], "close", ""),
    ("H05c", "Other chemicals", "detail", ["Other chemicals"], "284-85, 287-89",
     [[("+", "325"), ("-", "3251"), ("-", "3252"), ("-", "3254")]], "close", "Residual."),
    ("H06", "Petroleum and coal products", "industry", ["Petroleum refining and extraction"], "13, 29",
     [[("+", "324")]], "approximate", "SIC group includes oil and gas extraction (SIC 13); NAICS 324 excludes it (NAICS 211, in mining 21)."),
    ("H07", "Rubber and plastics products", "industry", ["Rubber products"], "30", [[("+", "326")]], "close", ""),
    ("H08", "Stone, clay, glass, and nonmetallic minerals", "industry", ["Stone, clay, and glass products"], "32",
     [[("+", "327")]], "close", ""),
    ("H09", "Primary metals", "industry", ["Primary metals"], "33", [[("+", "331")]], "close", ""),
    ("H10", "Fabricated metal products", "industry", ["Fabricated metal products"], "34", [[("+", "332")]], "close", ""),
    ("H11", "Machinery, except computers", "industry", ["Other machinery, except electrical"], "351-56, 358-59",
     [[("+", "333")]], "close", ""),
    ("H12", "Computers, audio and video, and other electronics", "industry",
     ["Office, computing, and accounting machines", "Radio and TV receiving equipment"], "357, 365",
     [[("+", "334"), ("-", "3342"), ("-", "3344"), ("-", "3345")]], "approximate",
     "NAICS residual of 334 (3341, 3343, 3346). SIC 365 is not reported in most years; when it is missing the SIC side is SIC 357 only."),
    ("H13", "Communications equipment", "industry", ["Communication equipment"], "366", [[("+", "3342")]], "close", ""),
    ("H14", "Semiconductors and electronic components", "industry", ["Electronic components"], "367",
     [[("+", "3344")]], "close", ""),
    ("H15", "Electrical equipment, appliances, and components", "industry", ["Other electrical equipment"],
     "361-64, 369", [[("+", "335")]], "close", ""),
    ("H16", "Motor vehicles and parts", "industry", ["Motor vehicles and motor vehicles equipment"], "371",
     [[("+", "3361-63")]], "close", ""),
    ("H17", "Aerospace", "industry", ["Aircraft and missiles"], "372, 376", [[("+", "3364")]], "close", ""),
    ("H18", "Other transportation equipment", "industry", ["Other transportation equipment"], "373-75, 379",
     [[("+", "336"), ("-", "3361-63"), ("-", "3364")]], "close", "Residual."),
    ("H19", "Instruments and medical equipment", "industry", ["Professional and scientific instruments"], "38",
     [[("+", "3345"), ("+", "3391")]], "approximate",
     "Photographic equipment (SIC 386) and optical instruments moved to other NAICS industries; NAICS 3345 also takes electrical measuring instruments from SIC 36."),
    ("H19a", "Measuring and control instruments", "detail", ["Scientific and mechanical measuring instruments"],
     "381-82", [[("+", "3345")]], "approximate", "See H19."),
    ("H19b", "Medical, optical, and photographic equipment", "detail",
     ["Optical, surgical, photographic, and other instruments"], "384-87", [[("+", "3391")]], "approximate", "See H19."),
    ("H20", "Other manufacturing", "industry", ["Other manufacturing industries"], "27, 31, 39",
     [[("+", "323"), ("+", "339"), ("-", "3391")], [("+", "339"), ("-", "3391")]], "approximate",
     "1999-2007 excludes printing (in H04). From 1996 SIC other manufacturing includes all small manufacturers (h-27 footnote 3)."),
    ("H21", "Machinery, electrical, electronic, and instruments (35, 36, 38)", "aggregate",
     ["Machinery", "Electrical equipment", "Professional and scientific instruments"], "35, 36, 38",
     [[("+", "333"), ("+", "334"), ("+", "335"), ("+", "3391")], [("+", "333"), ("+", "334"), ("+", "335")]], "close",
     "Robust aggregate: absorbs the moves of computers, instruments, and audio equipment between SIC 35, 36, 38 and NAICS 333-335. When 3391 is withheld, NAICS side is 333-335 only (see built_from)."),
    ("H22", "Transportation equipment", "aggregate", ["Transportation equipment"], "37", [[("+", "336")]], "close", ""),
    ("HN1", "Software and computer services", "industry", ["Computer and data processing services"], "737",
     [[("+", "5112"), ("+", "5415"), ("+", "518")], [("+", "5112"), ("+", "5415")]], "approximate",
     "SIC side from 1995. NAICS 518 (data processing) is reported from 2005."),
    ("HN2", "Scientific R&D services", "industry", ["Research, development, and testing"], "873",
     [[("+", "5417")]], "approximate", "SIC 873 includes testing laboratories (NAICS 541380). SIC side from 1995."),
    ("HN3", "Engineering and architectural services", "industry", ["Engineering, architectural, and surveying"],
     "871", [[("+", "5413")]], "close", "SIC side from 1995."),
    ("HN4", "Trade", "industry", ["Trade"], "50-59", [[("+", "42"), ("+", "44, 45")], [("+", "42, 44, 45")]],
     "approximate", "NAICS retail includes electronic shopping. SIC side from 1995."),
    ("HN5", "Finance, insurance, and real estate", "industry", ["Finance, insurance, and real estate"], "60-67",
     [[("+", "52"), ("+", "53")], [("+", "52, 53")]], "close", "SIC side from 1995."),
    ("HN6", "Utilities", "industry", ["Electric, gas, and sanitary services"], "49", [[("+", "22")]], "close",
     "SIC side from 1995."),
    ("HN7", "Health care services", "industry", ["Health services"], "80", [[("+", "621-23")]], "close",
     "SIC side from 1995."),
]


# Alternative SIC recipes (signed IRIS labels), tried after the direct label(s).
SIC_ALT = {
    "HM": [[("+", "All industries"), ("-", "Nonmanufacturing")]],
    "H11": [[("+", "Machinery"), ("-", "Office, computing, and accounting machines")]],
    "H12": [[("+", "Office, computing, and accounting machines")]],
    "H15": [[("+", "Electrical equipment"), ("-", "Radio and TV receiving equipment"), ("-", "Communication equipment"), ("-", "Electronic components")]],
    "H19": [[("+", "Scientific and mechanical measuring instruments"), ("+", "Optical, surgical, photographic, and other instruments")]],
    "H21": [[("+", "Machinery"), ("+", "Electrical equipment"), ("+", "Scientific and mechanical measuring instruments"), ("+", "Optical, surgical, photographic, and other instruments")]],
    "H22": [[("+", "Motor vehicles and motor vehicles equipment"), ("+", "Other transportation equipment"), ("+", "Aircraft and missiles")]],
}


def norm_code(c, label=""):
    if c is None or (isinstance(c, float) and np.isnan(c)) or str(c).strip() in ("", "nan"):
        return {"All industries": "ALL", "Manufacturing": "MFG", "Nonmanufacturing": "NONMFG"}.get(label, None)
    s = " ".join(str(c).replace("–", "-").split())
    if re.fullmatch(r"21-23, 31-33, 42(, 44)?-81", s): return "ALL"
    if re.fullmatch(r"21-23, 42(, 44)?-81", s): return "NONMFG"
    if s == "31-33": return "MFG"
    rep = {"313-316": "313-16", "3361-3363": "3361-63", "3361, 3362, 3363": "3361-63", "621-623": "621-23",
           "48, 49": "48-49", "336411-336413": "336411-13", "336414, 336415, 336419": "336414-15, 336419",
           "454111, 454112": "454111-12"}
    return rep.get(s, s)


def naics_dollars():
    """NAICS cost items in $ millions by year and normalized code (percent tables converted)."""
    l = pd.read_csv(DATA / "panel_rd_cost_by_type_long.csv", dtype={"code": str})
    l = l[l.classification.eq("NAICS")].copy()
    l["ncode"] = [norm_code(c, lab) for c, lab in zip(l.code, l.label)]
    tot = l[l.variable.eq("total")].set_index(["year", "ncode"])["value"]
    tot = tot[~tot.index.duplicated()]
    l = l.join(tot.rename("tot"), on=["year", "ncode"])
    l["usd"] = np.where(l.unit.eq("pct_of_total"), l.value / 100 * l.tot, l.value)
    return l.drop_duplicates(["year", "ncode", "variable"])


def h25_totals():
    """Total R&D by SIC industry and year from IRIS h-25 (wide layout, three column blocks)."""
    d = pd.read_excel(PAGES / "excel-files_historical_tables_h-25.xls", header=None)
    hdr = list(d.index[d[0].astype(str).str.contains("Industry and size", na=False)]) + [len(d)]
    out = {}
    for a, b in zip(hdr[:-1], hdr[1:]):
        starts = [c for c in range(d.shape[1]) if str(d.iloc[a, c]).startswith("Industry")]
        for k, c0 in enumerate(starts):
            c1 = starts[k + 1] if k + 1 < len(starts) else d.shape[1]
            years = {c: int(str(d.iloc[a, c])[:4]) for c in range(c0 + 2, c1) if pd.notna(d.iloc[a, c])}
            pending = ""
            for r in range(a + 1, b):
                lab = d.iloc[r, c0]
                if pd.isna(lab):
                    continue
                lab = " ".join(re.sub(r"[.…]{2,}.*$", "", str(lab)).split())
                lab = re.sub(r"(?<=[a-z])\d+,?$", "", lab).rstrip(",").strip() if not lab.endswith(" and") else lab
                if "size of company" in lab.lower():
                    break
                vals = {y: pd.to_numeric(str(d.iloc[r, c]).replace(",", ""), errors="coerce") for c, y in years.items()}
                if all(pd.isna(v) for v in vals.values()):
                    pending = (pending + " " + lab) if (pending and lab[:1].islower()) else lab
                    continue
                if pending and lab[:1].islower():
                    lab = pending + " " + lab
                pending = ""
                for y, v in vals.items():
                    if pd.notna(v) and (y, lab) not in out:
                        out[(y, lab)] = float(v)
    return out


def sic_dollars():
    l = pd.read_csv(DATA / "panel_rd_cost_by_type_long.csv", dtype={"code": str})
    l = l[l.classification.eq("SIC")].copy()
    tot = l[l.variable.eq("total")].set_index(["year", "label"])["value"]
    tot = tot[~tot.index.duplicated()]
    l = l.join(tot.rename("tot"), on=["year", "label"])
    # 1985: h-27 reports shares without dollar totals; use h-25 totals as weights
    h25 = h25_totals()
    miss = l.tot.isna() & l.year.eq(1985)
    l.loc[miss, "tot"] = [h25.get((y, lab), np.nan) for y, lab in zip(l.year[miss], l.label[miss])]
    tv = l.variable.eq("total") & l.value.isna() & l.year.eq(1985)
    l.loc[tv, "value"] = l.loc[tv, "tot"]
    # a few 1995-98 rows store percent components as fractions; detect by their sum
    psum = l[l.unit.eq("pct_of_total")].groupby(["year", "label"]).value.sum().rename("psum")
    l = l.join(psum, on=["year", "label"])
    scale = np.where(l.psum < 1.5, 1.0, 100.0)
    l["usd"] = np.where(l.unit.eq("pct_of_total"), l.value / scale * l.tot, l.value)
    l.loc[l.variable.isin(["wages_se", "wages_support"]), "variable"] = "wages_split"
    l = l.groupby(["year", "label", "variable"], as_index=False).agg(usd=("usd", lambda s: s.sum(min_count=len(s))))
    # before 1976 wages are reported by occupation; their sum is wages
    w = l[l.variable.eq("wages_split")].assign(variable="wages")
    l = pd.concat([l[~l.variable.isin(["wages_split", "wages"])], l[l.variable.eq("wages")], w]).drop_duplicates(["year", "label", "variable"])
    return l


def apply_recipe(table, key, year, variable, recipe):
    """table: dict (year, key, variable) -> value. Returns (value, alternative used) or (nan, '')."""
    for alt in recipe:
        vals = [table.get((year, code, variable), np.nan) for _, code in alt]
        if not any(np.isnan(v) for v in vals):
            return sum(v if s == "+" else -v for (s, _), v in zip(alt, vals)), " ".join(s + c for s, c in alt)
    return np.nan, ""


def harmonize_cost():
    n = naics_dollars(); s = sic_dollars()
    nt = {(y, c, v): x for y, c, v, x in zip(n.year, n.ncode, n.variable, n.usd) if pd.notna(x)}
    st = {(y, c, v): x for y, c, v, x in zip(s.year, s.label, s.variable, s.usd) if pd.notna(x)}
    rows = []
    for hid, hlab, level, sic_labs, sic_codes, recipe, q, note in G:
        for y in sorted(set(n.year)):
            for v in sorted(set(n[n.year.eq(y)].variable)):
                val, used = apply_recipe(nt, "naics", y, v, recipe)
                if pd.notna(val):
                    rows.append(dict(hid=hid, group=hlab, level=level, classification="NAICS", year=y, variable=v, usd_m=val, built_from=used))
        sic_recipe = [[("+", lab) for lab in sic_labs]] + SIC_ALT.get(hid, [])
        for y in sorted(set(s.year)):
            for v in sorted(set(s[s.year.eq(y)].variable)):
                val, used = apply_recipe(st, "sic", y, v, sic_recipe)
                if pd.notna(val):
                    rows.append(dict(hid=hid, group=hlab, level=level, classification="SIC", year=y, variable=v, usd_m=val, built_from=used))
    h = pd.DataFrame(rows)
    w = h.pivot_table(index=["hid", "group", "level", "classification", "year"], columns="variable", values="usd_m").reset_index()
    for c in [c for c in w.columns if c not in ("hid", "group", "level", "classification", "year", "total")]:
        w["s_" + c] = w[c] / w["total"]
    w["s_wages_fringe"] = w.get("s_salaries_wages_fringe").fillna(w["s_wages"] + w["s_fringe"])
    w["s_labor_broad"] = w["s_wages_fringe"] + w["s_stock_comp"] + w["s_temp_staffing"]
    return h, w


def harmonize_fte():
    l = pd.read_csv(DATA / "panel_fte_rd_scientists_engineers_long.csv", dtype={"code": str})
    l = l[l.variable.eq("fte_se")]
    n = l[l.classification.eq("NAICS")].copy()
    n["ncode"] = [norm_code(c, lab) for c, lab in zip(n.code, n.label)]
    nt = {(y, c, "fte_se"): x for y, c, x in zip(n.year, n.ncode, n.value) if pd.notna(x)}
    s = l[l.classification.eq("SIC")]
    st = {(y, c, "fte_se"): x for y, c, x in zip(s.year, s.label, s.value) if pd.notna(x)}
    rows = []
    for hid, hlab, level, sic_labs, sic_codes, recipe, q, note in G:
        for y in sorted(set(n.year)):
            val, used = apply_recipe(nt, "naics", y, "fte_se", recipe)
            if pd.notna(val):
                rows.append(dict(hid=hid, group=hlab, level=level, classification="NAICS", year=y, fte_se_thousands=val, built_from=used))
        sic_recipe = [[("+", lab) for lab in sic_labs]] + SIC_ALT.get(hid, [])
        for y in sorted(set(s.year)):
            val, used = apply_recipe(st, "sic", y, "fte_se", sic_recipe)
            if pd.notna(val):
                rows.append(dict(hid=hid, group=hlab, level=level, classification="SIC", year=y, fte_se_thousands=val, built_from=used))
    return pd.DataFrame(rows)


def overlap_check(h):
    """Compare SIC (h-27) and NAICS (NSF 02-312 table A-3) total R&D in 1997 and 1998."""
    a3 = read_table(PAGES / "excel-files_nsf_02-312_a-3.xls", 3, {"y1997": 5, "y1998": 6}, 0, "a-3")
    a3 = pd.DataFrame(a3)
    a3["ncode"] = [norm_code(c, lab) for c, lab in zip(a3.code, a3.label)]
    t = {}
    for c, v, x in zip(a3.ncode, a3.variable, a3.value):
        if pd.notna(x):
            t[(int(v[1:]), c, "total")] = x
    rows = []
    for hid, hlab, level, sic_labs, sic_codes, recipe, q, note in G:
        for y in (1997, 1998):
            nv, used = apply_recipe(t, "naics", y, "total", recipe)
            sv = h[(h.hid == hid) & (h.classification == "SIC") & (h.year == y) & (h.variable == "total")].usd_m
            sv = sv.iloc[0] if len(sv) else np.nan
            rows.append(dict(hid=hid, group=hlab, year=y, sic_total=sv, naics_total=nv, ratio_naics_to_sic=nv / sv if sv else np.nan))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    cw = pd.DataFrame([dict(hid=g[0], group=g[1], level=g[2], sic_industries="; ".join(g[3]), sic_codes=g[4],
                            naics_recipe=" | ".join(" ".join(s + c for s, c in alt) for alt in g[5]),
                            quality=g[6], note=g[7]) for g in G])
    h, w = harmonize_cost()
    f = harmonize_fte()
    chk = overlap_check(h)
    cw = cw.merge(chk.pivot_table(index="hid", columns="year", values="ratio_naics_to_sic").add_prefix("ratio_naics_sic_").reset_index(), on="hid", how="left")
    cw.to_csv(DATA / "crosswalk_sic_naics_rd.csv", index=False)
    chk.to_csv(DATA / "crosswalk_check_1997_98.csv", index=False)
    w.to_csv(DATA / "panel_harmonized_rd_cost_shares.csv", index=False)
    f.to_csv(DATA / "panel_harmonized_fte_se.csv", index=False)
    pd.set_option("display.width", 220)
    print(chk.pivot_table(index=["hid", "group"], columns="year", values=["sic_total", "naics_total", "ratio_naics_to_sic"]).round(2).to_string())


def assess(cw, w, f):
    """Evidence for linking each group across 1998-99, and a recommendation."""
    out = []
    for hid in cw.hid:
        x = w[w.hid.eq(hid)]
        sic = x[x.classification.eq("SIC") & x.s_wages.notna()]
        nai = x[x.classification.eq("NAICS") & x.s_wages.notna()]
        s_end = sic[sic.year.between(1995, 1998)].s_wages.mean()
        n_beg = nai[nai.year.between(1999, 2002)].s_wages.mean()
        fs = f[f.hid.eq(hid)]
        out.append(dict(hid=hid, sic_years_wage_share=len(sic), sic_first_year=sic.year.min() if len(sic) else np.nan,
                        naics_years_wage_share=len(nai), wage_share_sic_1995_98=s_end, wage_share_naics_1999_2002=n_beg,
                        wage_share_gap=n_beg - s_end, fte_sic_years=int(fs.classification.eq("SIC").sum()),
                        fte_naics_years=int(fs.classification.eq("NAICS").sum())))
    a = cw.merge(pd.DataFrame(out), on="hid")
    r = a[["ratio_naics_sic_1997", "ratio_naics_sic_1998"]].mean(axis=1)
    ok_level = r.between(0.85, 1.15)
    ok_share = a.wage_share_gap.abs() < 0.05
    no_ev = r.isna() & a.wage_share_gap.isna()
    a["link_recommendation"] = np.select(
        [ok_level & ok_share, ok_share & r.isna(), ok_level & a.wage_share_gap.isna(), ok_level | ok_share, no_ev],
        ["link", "link (share evidence only)", "link (level evidence only)", "link with care", "no overlap evidence"], "do not link")
    return a


if __name__ == "__main__":
    a = assess(cw, w, f)
    a.to_csv(DATA / "crosswalk_sic_naics_rd.csv", index=False)
    cols = ["hid", "group", "quality", "ratio_naics_sic_1997", "ratio_naics_sic_1998", "wage_share_sic_1995_98",
            "wage_share_naics_1999_2002", "wage_share_gap", "sic_first_year", "sic_years_wage_share", "naics_years_wage_share", "link_recommendation"]
    print(a[cols].round(2).to_string())
