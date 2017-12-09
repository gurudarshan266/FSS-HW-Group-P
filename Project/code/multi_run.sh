#!/usr/bin/env bash

datasets=( ivy jedit1 jedit2 jedit3 lucene velocity xalan1 xalan2 xerces )

for f in "${datasets[@]}"
do
    python3 run.py $f f1 &> ../output/$f.out && echo "Completed $f..." &
done
