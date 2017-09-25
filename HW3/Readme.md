## HW3 - Discretization

Usage:

`python SuperDiscrete.py <filename> <NUM/SYM>`

The input file by default is expected to have two columns. The first column containing the variable used for Unsupervised Descritizer and the second column for Supervised Descretizer. `UD_sample.txt` contains sample data in this format. To generate more random samples use:

`python UDiscrete_gen.py <size of sample> <NUM/SYM>`

Executing the above script regenerates `UD_sample.txt` with a new set of samples

A bash script has been provided to run the program for 20 iterations with different input sizes ( < 10000 ). To run the script use:

`./run.sh`
