# FSS-HW1
CSV Parser

`parser.py` can be used to parse CSV files. 

Usage:

`python parser.py <filename.csv>`

The parser sequentially parses every line and stores or ignores the data in the columns as per the conditions specifed in the header row.

Parsed data will be output to `parsed.txt`

Error logs are printed on stderr. Example:

`Invalid data found on line 91`


Time taken to parse the file is shown on stdout. Example:

`Time taken to parse = 0:00:00.275000`