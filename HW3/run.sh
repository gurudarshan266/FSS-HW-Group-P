#!/bin/bash

for i in {1..20}
do
	
	echo -e "\nRUN = #$i\n"
	python Udiscrete_gen.py
	python SuperDiscrete.py UD_sample.txt
	echo -e "-------------------------------------------------------------------------------------------------------------------\n\n"
done
