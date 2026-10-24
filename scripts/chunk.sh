#!/bin/bash
# One crawl chunk: run the crawler for ~110 minutes, then push progress to the repo.
cd /home/user/iris
timeout 6600 python3 -I scripts/crawl2.py /home/user/iris/crawl 5 >> crawl/stdout2.log 2>&1
scripts/sync_repo.sh 2>&1 | tail -1
grep -c . crawl/crawl2_log.tsv
tail -1 crawl/stdout2.log
