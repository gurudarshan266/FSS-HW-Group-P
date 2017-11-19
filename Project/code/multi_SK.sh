#!/usr/bin/env bash
BASE_DIR='../results/f1'

kouts=( $(ls $BASE_DIR/*.kout) )

for f in "${kouts[@]}"
do
    echo "Evaluating for $f...."
    cat $f | python SK.py
    echo -e "\n\n"
done