#!/bin/sh
set -eu
docker compose up --build -d --scale backend=3
for attempt in 1 2 3 4 5 6 7 8 9; do
  curl -fsS http://127.0.0.1:3000/
  printf '\n'
done
