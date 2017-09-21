# FSS-HW

## HW1 - CSV Parser

### Description
Read each line, kill whitepsace and anything after comment characters (#), break each line on comma, read rows into a list of lists (one list per row), converting strings to numbers where appropriate. Note that some column headers contain ?: all such columns should be ignored. For now you can ignore the other magic characters in row1.

<br><br>

`parser.py` can be used to parse CSV files. 

Usage:

`python parser.py <filename.csv>`

The parser sequentially parses every line and stores or ignores the data in the columns as per the conditions specifed in the header row.

Parsed data will be output to `parsed.txt`<br><br>

Error logs are printed on stderr. Example:

`Invalid data found on line 91`
<br><br>

Time taken to parse the file is shown on stdout. Example:

`Time taken to parse = 0:00:00.275000`

<br><br><br><br>

## HW2 - Table Parser

Usage:

`python table_parser.py <filename.csv>`

<br><br><br><br>

## HW2 - Discretization

Usage:

`python SuperDiscrete.py <filename>`

The input file by default is expected to have two columns. The first column containing the variable used for Unsupervised Descritizer and the second column for Supervised Descretizer. `UD_sample.txt` contains sample data in this format. To generate more random samples use:

`python UDiscrete_gen`

Executing the above script regenerates `UD_sample.txt` with a new set of samples
