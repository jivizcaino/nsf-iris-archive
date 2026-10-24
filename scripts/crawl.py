"""Polite crawler for the archived NSF IRIS site (Archive-It collection 5902)."""
import re, time, sys, json, html, hashlib, urllib.parse, subprocess
from pathlib import Path

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
START = "https://wayback.archive-it.org/5902/20181003221605/https://www.nsf.gov/statistics/iris/"
DELAY = float(sys.argv[2]) if len(sys.argv) > 2 else 8
MAXN = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
KEEP = re.compile(r"nsf\.gov/statistics/iris/", re.I)
log = open(OUT / "crawl_log.tsv", "a")
state_f = OUT / "state.json"
if state_f.exists():
    st = json.loads(state_f.read_text()); seen = set(st["seen"]); queue = st["queue"]
else:
    seen = {START}; queue = [START]

def fetch(url):
    wait = 60
    for _ in range(12):
        r = subprocess.run(["curl", "-sSL", "--max-time", "120", "-w", "\n%{http_code}|%{content_type}|%{url_effective}", url],
                           capture_output=True)
        body, _, meta = r.stdout.rpartition(b"\n")
        code, ctype, eff = (meta.decode(errors="ignore").split("|") + ["", "", ""])[:3]
        if b"Rate limit reached" in body[:3000]:
            print(f"rate-limited, waiting {wait}s", flush=True); time.sleep(wait); wait = min(wait * 2, 900); continue
        return code, ctype, eff, body
    return "RL", "", url, b""

def norm(base, h):
    u = urllib.parse.urljoin(base, html.unescape(h)).split("#")[0]
    # canonical archive form: .../5902/<ts>/<orig>
    m = re.match(r"https://wayback\.archive-it\.org/5902/(\d+)[a-z_]*/(.*)", u)
    if not m: return None
    orig = m.group(2).replace("https:/www", "https://www").replace("http:/www", "http://www")
    if not KEEP.search(orig): return None
    if re.search(r"\.(gif|jpe?g|png|css|js|ico)$", orig, re.I): return None
    return f"https://wayback.archive-it.org/5902/{m.group(1)}/{orig}"

n = 0
while queue and n < MAXN:
    url = queue.pop(0); n += 1
    code, ctype, eff, body = fetch(url)
    name = hashlib.md5(url.encode()).hexdigest()[:12]
    path = urllib.parse.urlparse(re.sub(r".*?/\d{14}[a-z_]*/", "", url)).path
    ext = Path(path).suffix.lower() or ".html"
    fn = OUT / "pages" / f"{name}{ext}"; fn.parent.mkdir(exist_ok=True)
    fn.write_bytes(body)
    log.write(f"{code}\t{ctype}\t{len(body)}\t{fn.name}\t{url}\n"); log.flush()
    print(n, code, len(body), url, flush=True)
    if "html" in ctype:
        t = body.decode("latin-1")
        for h in re.findall(r'(?:href|src|action)\s*=\s*["\']([^"\']+)', t, re.I):
            u = norm(eff or url, h)
            if u and u not in seen:
                seen.add(u); queue.append(u)
    state_f.write_text(json.dumps({"seen": sorted(seen), "queue": queue}))
    time.sleep(DELAY)
print("DONE", n, "fetched;", len(queue), "left in queue")
