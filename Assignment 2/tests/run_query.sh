#!/bin/bash

# 1. Run student's query script
student_name=$(basename "$(ls *.py)" .py)
docker run --network "$student_name" --rm -v .:/app -w /app python:3 bash -c "pip install -qqq pymongo && python3 queries/q$1.py"

# 2. Get student answer vs. ground_truth
file_1=./q"$1".csv
file_2=~/ground_truth/"${student_name}"/q"$1".csv

# 3. Debug (shows line numbers)
echo "Comparing $file_1 and $file_2"
echo ">>>>>>>>>>>>>"
wc -l "$file_1"
echo "<<<<<<<<<<<<<"
wc -l "$file_2"
echo ">>>>>>>>>>>>>"

# 4. Compare results, cleanup on failue
if ! cmp -s <(tr -d '\r' < "$file_1") <(tr -d '\r' < "$file_2"); then
    echo "Error: q$1 results do not match"
    exit 1
fi

# 5. Cleanup
echo "Test passed!"
