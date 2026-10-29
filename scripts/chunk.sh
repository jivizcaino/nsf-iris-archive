#!/bin/bash
# One crawl chunk: test one request first; if the archive still rate-limits, stop (retry at next check-in).
# Otherwise run the crawler for ~110 minutes, then push progress to the repo.
cd /home/user/iris
if curl -sS --max-time 60 "https://wayback.archive-it.org/5902/20181003221605/https://www.nsf.gov/statistics/iris/" | grep -q "Rate limit reached"; then
  echo "BLOCKED: archive still rate-limiting at $(date -u +%H:%M) UTC"
  grep -c . crawl/crawl2_log.tsv
  exit 0
fi
timeout 6600 python3 -I scripts/crawl2.py /home/user/iris/crawl 5 >> crawl/stdout2.log 2>&1
scripts/sync_repo.sh 2>&1 | tail -1
grep -c . crawl/crawl2_log.tsv
tail -1 crawl/stdout2.log
