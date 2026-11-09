#!/bin/sh
set -eu
docker build -f Dockerfile.single -t lesson37-single .
docker build -f Dockerfile -t lesson37-multi .
docker image inspect lesson37-single lesson37-multi --format '{{.RepoTags}} {{.Size}} bytes'
