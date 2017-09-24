#!/bin/bash

for i in {1..20}
do
	N=`expr $RANDOM % 10000`
	echo -e "\nRUN = #$i\n"
	python Udiscrete_gen.py $N
	python SuperDiscrete.py UD_sample.txt
	echo -e "-------------------------------------------------------------------------------------------------------------------\n\n"
done
