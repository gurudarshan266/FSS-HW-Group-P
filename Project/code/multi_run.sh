#!/usr/bin/env bash

datasets=( ivy jedit1 jedit2 jedit3 lucene velocity xalan1 xalan2 xerces )

for f in "${datasets[@]}"
do
    python3 run.py $f > ../output/$f.out && echo "Completed $f..." &
done

# python3 run.py ivy > ../output/ivy.out && echo "Completed with" &
# python3 run.py jedit1 > ../output/jedit1.out &
# python3 run.py jedit2  > ../output/jedit2.out &
# python3 run.py lucene  > ../output/lucene.out &