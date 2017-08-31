import sys

col_names = []
accpetance_matrix = []
values = []


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
		return line[:index-1]
		
	return line
	
	
		
def parse_first_line(line):
	global col_names
	global accpetance_matrix
	
	line_split = line.split(',')
	col_names = [ x.strip() for x in line_split]
	accpetance_matrix = [ not x.startswith('?') for x in col_names ]
	print col_names
	print accpetance_matrix

	
	
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
		print "Wrong number of columns found at %d"%line_num
		return None
	
	print line
	vals = []
	for i in range(len(line_split)):
		if accpetance_matrix[i]:
			val = parse_val(line_split[i].strip())
			vals.append(val)
	return vals
	
	
	

	
if __name__ == '__main__':
	is_first = True
	
	if len(sys.argv) < 2:
		print "Usage: \n %s <file>"%(sys.argv[0])
		sys.exit(-1)
		
	in_file = sys.argv[1]
	
	with open(in_file, "r") as fp:
	
		buff = ''
		continue_nextl = False
		line_num = 2
		
		for line in fp:
			line = remove_commented_str(line)
			
			# Do nothing if the whole line is commented
			if len(line) == 0:
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
					if continue_nextl:
						continue_nextl = False
						buff = buff + line
						
						#Only add valid rows
						vals_row = parse_line(buff,line_num)
						if vals_row is not None:
							values.append(vals_row)
							
						buff = ''
					else:
						#Only add valid rows
						vals_row = parse_line(line,line_num)
						if vals_row is not None:
							values.append(vals_row)
						
			line_num = line_num + 1
			
		