"""Priority crawler for the archived NSF IRIS site (Archive-It collection 5902).
Deduplicates by original URL and fetches priority topics first."""
import re, time, sys, json, html, hashlib, heapq, urllib.parse, subprocess
from pathlib import Path

OUT = Path(sys.argv[1]); (OUT / "pages").mkdir(parents=True, exist_ok=True)
DELAY = float(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2][0].isdigit() else 5
TS = "20181003221605"
PRE = f"https://wayback.archive-it.org/5902/{TS}/"
ROOT = "https://www.nsf.gov/statistics/iris/"
# topic priority: 3 type of cost, 24 FTE S&E, 25 cost per S&E, 8 detailed industry summary,
# 1 total by industry, 10 company, 16 federal, 23 employment, 27 sales, 7/13 R&D intensity
PRI_TOPICS = [3, 24, 25, 8, 1, 10, 16, 23, 27, 7, 13, 9, 26]
NAICS_PUBS = re.compile(r"nsf_(2007|2006|10-319|09-301|07-314|06-322|05-305|03-318|02-312)/")
log = open(OUT / "crawl2_log.tsv", "a")
state_f = OUT / "state2.json"

def prio(orig, parent_p):
    m = re.search(r"search_hist\.cfm\?indx=(\d+)$", orig)
    if m:
        k = int(m.group(1)); return PRI_TOPICS.index(k) * 10 if k in PRI_TOPICS else 500
    if "historical_tables/h-" in orig: return 0
    if re.search(r"\.xls$", orig, re.I):
        return parent_p + 1 if NAICS_PUBS.search(orig) else 400 + parent_p
    if re.search(r"\.doc$", orig, re.I):
        return parent_p + 2 if NAICS_PUBS.search(orig) else 450
    if "tables.cfm?pub_year" in orig: return 600
    if re.search(r"/iris/[a-z_]+\.cfm$", orig): return 0
    return parent_p + 5

if state_f.exists():
    st = json.loads(state_f.read_text()); seen = set(st["seen"]); heap = [tuple(x) for x in st["heap"]]
    if "--reprio" in sys.argv: heap = [(prio(o, 0), c, o) for q, c, o in heap]; heapq.heapify(heap)
else:
    seen = {ROOT}; heap = [(0, 0, ROOT)]
counter = len(seen)

def fetch(url):
    wait = 60
    for _ in range(15):
        r = subprocess.run(["curl", "-sSL", "--max-time", "120", "-w", "\n%{http_code}|%{content_type}|%{url_effective}", url], capture_output=True)
        body, _, meta = r.stdout.rpartition(b"\n")
        code, ctype, eff = (meta.decode(errors="ignore").split("|") + ["", "", ""])[:3]
        if b"Rate limit reached" in body[:3000]:
            print(f"rate-limited, waiting {wait}s", flush=True); time.sleep(wait); wait = min(wait * 2, 600); continue
        return code, ctype, eff, body
    return "RL", "", url, b""

def orig_of(base, h):
    u = urllib.parse.urljoin(base, html.unescape(h).strip()).split("#")[0]
    m = re.match(r"https?://wayback\.archive-it\.org/5902/\d+[a-z_]*/(.*)", u)
    o = m.group(1) if m else u
    o = re.sub(r"^https?:/+", "https://", o).replace("http://", "https://")
    if not o.lower().startswith(ROOT): return None
    if re.search(r"\.(gif|jpe?g|png|css|js|ico)$", o, re.I): return None
    return o

n = 0
while heap:
    p, _, orig = heapq.heappop(heap); n += 1
    code, ctype, eff, body = fetch(PRE + orig)
    rel = orig[len(ROOT):] or "index.html"
    safe = re.sub(r"[^A-Za-z0-9._=-]", "_", rel)
    fn = OUT / "pages" / safe
    fn.write_bytes(body)
    log.write(f"{p}\t{code}\t{ctype}\t{len(body)}\t{safe}\t{orig}\n"); log.flush()
    print(n, p, code, len(body), rel, len(heap), "queued", flush=True)
    if "html" in ctype and b"Rate limit" not in body[:3000]:
        t = body.decode("latin-1")
        for h in re.findall(r'(?:href|src|action)\s*=\s*["\']([^"\']+)', t, re.I):
            o = orig_of(eff or (PRE + orig), h)
            if o and o not in seen:
                seen.add(o); counter += 1; heapq.heappush(heap, (prio(o, p), counter, o))
    state_f.write_text(json.dumps({"seen": sorted(seen), "heap": heap}))
    time.sleep(DELAY)
print("DONE", n)
