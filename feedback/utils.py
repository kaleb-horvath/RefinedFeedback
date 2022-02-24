"""utils.py

This file holds interface functionality and should be
imported as a module by __main__.py with the following functions:

	* parse_args - returns positional and optional command line arguments
	* get_input - read lines from 'stdin' until EOF is encountered
"""

import argparse
import sys

student_output = """"""

def parse_args ():
	"""Get and parse both positional and optional command 
	line arguments using 'argparse' library. Should
	be called and passed to 'main' in '__main__.py'.

	Returns
	-------
	argparse.Namespace
		object containing parsed command line arguments

	Usage
	-----
	>>> parse_args()
	"""
	# required command line arguments, positionally dependent
	parser = argparse.ArgumentParser(description="""Score student output against regex pattern""")
	parser.add_argument('lines', help="number of lines to read from \'stdin\'")
	parser.add_argument('regex', help="regular expressions pattern to use for matching, use quotes")
	
	# setup group of optional command line flags
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-i', '--ignore-stdin',
		action='store_true',
		help='ignore program\'s \'stdin\' and read lines from memory (\'student_output\' variable)')

	return parser.parse_args()

def get_input (args, n_lines, test_mode=False):
	"""Readlines from program 'stdin' until EOF is encountered
	or until no characters (including '\n') are encountered. This
	implies EOF on most systems. Should be called and passed to
	'get_matches' in 'feedback.py'.

	Parameters
	----------
	args : argparse.Namespace
		object containing parsed command line arguments
	n_lines : int
		number of lines to read from stdin
	test_mode : bool
		allows us to bypass use of argparse.Namespace,
		saves memory and time when unittesting

	Returns
	-------
	lines
		a list of strings representing lines from student's output

	Usage
	-----
	>>> # read ten lines from 'stdin' or until EOF
	>>> student_output = get_input(
			parser.parse_args(),
			10
		) 
	"""
	if test_mode:
		ignore_stdin = args
	else:
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
