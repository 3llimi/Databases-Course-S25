#!/bin/bash

student_name=$(basename "$(ls *.py)" .py)

docker stop mongo >/dev/null || true
docker container prune -f >/dev/null || true
docker network rm "$student_name" >/dev/null || true
