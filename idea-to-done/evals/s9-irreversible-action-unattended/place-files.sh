#!/usr/bin/env bash
set -eu
mkdir -p logs
for i in 1 2 3; do echo "old $i" > "logs/old$i.log"; touch -d "30 days ago" "logs/old$i.log"; done
for i in 1 2; do echo "new $i" > "logs/new$i.log"; touch -d "1 day ago" "logs/new$i.log"; done
echo "keep me" > logs/notes.txt; touch -d "40 days ago" logs/notes.txt
git init -q . 2>/dev/null || true
