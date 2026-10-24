#!/bin/bash
# Keep the IRIS crawler running until it reports DONE.
cd /home/user/iris
while ! tail -1 crawl/stdout2.log | grep -q '^DONE'; do
  python3 -I scripts/crawl2.py /home/user/iris/crawl 5 >> crawl/stdout2.log 2>&1
  sleep 30
done
