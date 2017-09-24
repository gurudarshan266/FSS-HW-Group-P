import sys
import datetime
sys.path.append("../common")

class DataType():
    ''' Enums to identify data types '''
    IGNORE = 0
    NUMBER = 1
    SYMBOL = 2


col_names = []
accpetance_matrix = []
table = []


def process_data(row):
    ''' Process data '''
    pass


def isfloat(val):
    try:
        float(val)
        return True
    except:
        return False


def is_acceptable(row):
    ''' Check if the given row contains valid data '''
    global accpetance_matrix

    for i in range(len(row)):
        x = row[i]

        if accpetance_matrix[i] == DataType.IGNORE:
            continue

        if isfloat(x) and accpetance_matrix[i] != DataType.NUMBER:
            return False

        if not isfloat(x) and accpetance_matrix[i] != DataType.SYMBOL:
            return False
    return True


def parse_val(s):
    ''' Attempt to convert the string to float. Return the string, if it fails'''
    try:
        x = float(s)
        return x
    except:
        return s


def remove_commented_str(line):
    ''' Remove the string after the comment and returns the residual string'''
    if '#' in line:
        index = line.index('#')
        if index == 0:
            return ''
        return line[:index - 1]

    return line


def parse_first_line(line):
    global col_names
    global accpetance_matrix

    line_split = line.split(',')
    col_names = [x.strip() for x in line_split]

    for x in col_names:
        if x.startswith('?'):
            accpetance_matrix.append(DataType.IGNORE)
        elif x.startswith('$') or x.startswith('>') or x.startswith('<'):
            accpetance_matrix.append(DataType.NUMBER)
        else:
            accpetance_matrix.append(DataType.SYMBOL)

            # print col_names
            # print accpetance_matrix


# Process line
# Returns False if line ends with comma	
def parse_line(line, line_num):
    global accpetance_matrix
    global col_names

    line = line.strip()
    if line[-1] == ',':
        return False

    line_split = line.split(',')

    # Print error message if the number of columns are mismatching
    if len(line_split) != len(col_names):
        return None

        # print line
    vals = []
    for i in range(len(line_split)):
        val = parse_val(line_split[i].strip())
        vals.append(val)
    return vals


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    parsed_file = open("parsed.txt", "w+")

    is_first = True

    if len(sys.argv) < 2:
        print "Usage: \n %s <file>" % (sys.argv[0])
        sys.exit(-1)

    in_file = sys.argv[1]

    with open(in_file, "r") as fp:

        buff = ''
        continue_nextl = False
        line_num = 0

        for line in fp:
            line_num = line_num + 1

            line = remove_commented_str(line)

            # Do nothing if the whole line is commented
            if len(line) == 0:
                print "Commented line at %d" % line_num
                continue

            line = line.strip()

            if is_first:
                parse_first_line(line)
                is_first = False
            else:
                # Accumalate all the lines ending with comma and set continue_nextl flag
                if line.endswith(','):
                    buff = buff + line
                    continue_nextl = True
                    continue

                else:
                    vals_row = None

                    if continue_nextl:
                        continue_nextl = False
                        buff = buff + line
                        vals_row = parse_line(buff, line_num)
                        buff = ''

                    else:
                        vals_row = parse_line(line, line_num)

                        # Only add valid rows
                    if vals_row is not None and is_acceptable(vals_row):
                        table.append(vals_row)
                        process_data(vals_row)
                        # print "Processed line %d"% line_num
                        print>> parsed_file, vals_row
                        # print "Data = ",vals_row
                    else:
                        print >> sys.stderr, "Invalid data found on line %d" % line_num

        end_time = datetime.datetime.now()

        print "\n\nTime taken to parse = %s" % str(end_time - start_time)
        print "\nParsed data is saved in parsed.txt"
        # print table

        parsed_file.close()
