
import argparse
import sys

student_output = """"""

def parse_args ():
	# required command line arguments, positionally dependent
	parser = argparse.ArgumentParser(description="""Score student output against regex pattern""")
	parser.add_argument('lines', help="number of lines to read from \'stdin\'")
	parser.add_argument('regex', help="regular expressions pattern to use for matching, use quotes")
	
	# setup group of optional command line flags
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d', '--debug', action='store_true', help='enable debugger')
	group.add_argument('-i', '--ignore-stdin',
		action='store_true',
		help='ignore program\'s \'stdin\' and read lines from memory (\'student_output\' variable)')

	return parser.parse_args()

def get_input (args):
	"""
	Read-lines from stdin until EOF
	"""
	n_lines = int(args.lines)
	ignore_stdin = args.ignore_stdin
	lines = list()

	if not ignore_stdin:
		lines_read = 0

		# loop read from stdin until EOF encountered
		while True:
			try:
				if (lines_read != n_lines):
					line = sys.stdin.readline()

					if line == '': raise EOFError
					lines_read += 1
					lines.append(line)
					continue
				break
			except EOFError: break 
			except IOError:
				rrf.__error('Problem reading from \'stdin\'', exit=1)
	else:
		lines = student_output.split('\n')
	lines = [
		l.replace('\n', '\u00B6') for l in lines
	]
	
	return lines
