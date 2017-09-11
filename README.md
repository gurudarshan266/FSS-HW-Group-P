# FSS-HW1
CSV Parser

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
