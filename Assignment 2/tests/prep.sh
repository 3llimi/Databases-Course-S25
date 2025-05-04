#!/bin/bash

# 0. Create a docker network for the student
student_name=$(basename "$(ls *.py)" .py)
docker network create "$student_name" || true

# 1. Run MongoDB in a container
docker run -q -d --name mongo --rm --network "$student_name" mongo

# 2. Run student's db initialization/filling script
docker run -q --network "$student_name" --rm -v .:/app -w /app python:3 bash -c "pip install -qqq pymongo && python3 $student_name.py"
