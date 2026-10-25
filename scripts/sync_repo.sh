#!/bin/bash
# Copy crawl output, scripts, and tidy data into the archive repo, then commit and push.
set -e
SRC=/home/user/iris; DST=/home/user/nsf-iris-archive; BR=ccr-3e40781d-04vz1j
mkdir -p "$DST/raw/pages" "$DST/raw/logs" "$DST/scripts" "$DST/data"
cp -ru "$SRC"/crawl/pages/. "$DST/raw/pages/"
cp "$SRC/crawl/crawl2_log.tsv" "$SRC/crawl/state2.json" "$DST/raw/logs/"
cp -u "$SRC"/scripts/* "$DST/scripts/"
cp -u "$SRC"/data/* "$DST/data/" 2>/dev/null || true
cp -u "$SRC/README.md" "$DST/README.md"
mkdir -p "$DST/raw_brdis_berd"; for y in 2015 2016 2017 2018 2019 2020 2021 2022 2023; do mkdir -p "$DST/raw_brdis_berd/$y"; cp -u "$SRC"/berd/y$y/*.xlsx "$DST/raw_brdis_berd/$y/"; done; rm -rf "$DST/raw_berd2023"
cd "$DST"
git checkout -q -B "$BR" 2>/dev/null || true
git add -A
if git diff --cached --quiet; then echo "nothing new"; exit 0; fi
N=$(ls raw/pages | wc -l)
git commit -q -m "Sync IRIS crawl: $N files

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01F89xGNCM2FYURff6ajQreG"
for i in 1 2 3 4; do git push -q -u origin "$BR" && break || sleep $((2**i)); done
echo "pushed $N files"
