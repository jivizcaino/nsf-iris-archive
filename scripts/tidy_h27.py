"""Tidy IRIS table h-27: total R&D by industry, size of company, and type of cost, 1962-98 (SIC)."""
import re, sys
import pandas as pd

SRC, OUT = sys.argv[1], sys.argv[2]
df = pd.read_excel(SRC, header=None)
DOLLAR_YEARS = {1962, 1972, 1973, 1974, 1975, 1976, 1977, 1979, 1981, 1983}  # footnote 5

def year_of(v):
    if pd.isna(v): return None
    s = str(int(v)) if isinstance(v, float) else str(v).strip()
    return int(s[:4])

def parse(v):
    if pd.isna(v): return None, ""
    if isinstance(v, (int, float)): return float(v), ""
    s = str(v).strip()
    flag = " ".join(re.findall(r"\(([A-Z])\)|\b(NA)\b", s) and [a or b for a, b in re.findall(r"\(([A-Z])\)|\b(NA)\b", s)])
    num = re.sub(r"\([A-Z]\)|NA|[,*]", "", s).strip()
    try: return float(num), flag
    except ValueError: return None, flag or s

hdr = list(df.index[df[0].astype(str).str.contains("Industry and size", na=False)]) + [len(df)]
rows = []
for a, b in zip(hdr[:-1], hdr[1:]):
    years = [year_of(df.iloc[a, 2]), year_of(df.iloc[a, 7])]
    section = "industry"; pending = ""
    for r in range(a + 7, b):
        lab = df.iloc[r, 0]
        if pd.isna(lab): continue
        lab_s = str(lab)
        if lab_s.strip().startswith(("See explanatory", "Total (company", "size of company,", "1 ", "KEY", "NOTE", "SOURCE")) or re.match(r"^\s*\d\s+", lab_s): continue
        if "Distribution by size" in lab_s: section = "size"; continue
        if "Distribution by industry" in lab_s or "[Number of" in lab_s: continue
        name = re.sub(r"[.…]+$", "", re.sub(r"[.…]{2,}.*$", "", lab_s)).rstrip()
        name_clean = re.sub(r"(\D)\d$", r"\1", name.strip())
        if name_clean.endswith(","):  # label wraps onto the next line
            pending = name_clean + " "; continue
        if pending and name_clean[:1].islower(): name_clean = pending + name_clean
        pending = ""
        indent = len(lab_s) - len(lab_s.lstrip())
        sic = df.iloc[r, 1]
        for k, y in enumerate(years):
            if y is None: continue
            c0 = 2 + 5 * k
            cells = [parse(df.iloc[r, c]) for c in range(c0, c0 + 5)]
            if all(v is None and not f for v, f in cells): continue
            if y < 1976: names = ["total", "wages_se", "wages_support", "materials", "other"]
            elif y < 1998: names = ["total", "wages", None, "materials", "other"]
            else: names = ["total", "wages", "depreciation", "materials", "other"]
            for nm, (v, f) in zip(names, cells):
                if nm is None: continue
                unit = "usd_millions" if nm == "total" or y in DOLLAR_YEARS else "pct_of_total"
                rows.append(dict(year=y, section=section, label=name_clean.strip(), indent=indent,
                                 sic=None if pd.isna(sic) else str(sic).strip(), variable=nm,
                                 value=v, unit=unit, flag=f, src_row=r + 1))
out = pd.DataFrame(rows)
# The 1995-98 nonmanufacturing blocks repeat "All industries"/"Manufacturing" in fraction form; keep first occurrence.
out = out.drop_duplicates(subset=["year", "section", "label", "sic", "variable"], keep="first")
# Express percent components in percent (some cells are stored as fractions).
pct = out.unit.eq("pct_of_total")
out.to_csv(OUT, index=False)
print(out.shape, sorted(out.year.unique()))
