#!/bin/bash
# Push crawl progress every 2 hours; final push when the crawl reports DONE.
LOG=/home/user/iris/crawl/sync.log
while true; do
  sleep 7200
  { date -u; /home/user/iris/scripts/sync_repo.sh; } >> "$LOG" 2>&1
  if tail -1 /home/user/iris/crawl/stdout2.log | grep -q '^DONE'; then { date -u; /home/user/iris/scripts/sync_repo.sh; } >> "$LOG" 2>&1; break; fi
done
