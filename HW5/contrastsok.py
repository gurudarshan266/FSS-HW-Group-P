import sys
sys.path.append("../common")
sys.path.append("../HW4")

import datetime
from defines import *
from Tbl import Tbl
import sdtree as tree

import contrasts as CON

col_names = []
accpetance_matrix = []
table = []
tbl = None

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
    global tbl
    tbl = Tbl(line)


# Process line
# Returns False if line ends with comma
def parse_line(line, line_num):
    global accpetance_matrix
    global col_names
    global tbl
    line = line.strip()
    if line[-1] == ',':
        return False

    #print "Line = %d"%line_num

    # call add row here
    tbl.add_row(line)





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
                print >> sys.stderr, "Commented line at %d" % line_num
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
                        parse_line(buff, line_num)
                        buff = ''

                    else:
                        parse_line(line, line_num)


        end_time = datetime.datetime.now()

        #print "\n\nTime taken to parse = %s" % str(end_time - start_time)
        #print "\nParsed data is saved in parsed.txt"
        # print table

        parsed_file.close()

        sorted_dscores = tbl.get_sorted_indices()
        #print sorted_dscores
        print "Headers"
        print tbl.headers
        print "Printing top 5"
        for i in sorted_dscores[:-6:-1]:
            print tbl.Rows[i[0]].cells

        print "Printing bottom 5"
        for i in (sorted_dscores[:5])[::-1]:
            print tbl.Rows[i[0]].cells


        t2 = tbl.discretizeRows(tbl.dom)
        t2.write_to_file(dom_scores=tbl.compute_domination_scores())
        print "\n\n\nSupervised Dom based table created..."

        for head in t2.x["cols"]:
            if head.bins:
                print str(len(head.bins)) +" "+ head.txt

        tr = tree.grow(t2,y=tbl.dom)
        tree.tprint(tr)

        b = CON.branches(tr)
        print "\n==================== Show branches \n\n"
        CON.maprint(b)
        print("\n==================== What to do: (plans= here to better) ")
        CON.plans(b)
        print("\n==================== What to fear: (monitors = here to worse) ")
        CON.monitors(b)



        # dom_tbl = tbl.compute_domination_scores()
        # dom_t2 = t2.compute_domination_scores()
        #
        # dom_diff = [dom_tbl[i]-dom_t2[i] for i in range(len(dom_t2))]
        # print dom_diff





