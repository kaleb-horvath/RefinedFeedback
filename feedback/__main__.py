
from __future__ import print_function
import sys
import argparse
import feedback as rrf

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


def main (args):
	regex = str(args.regex)
	debug = args.debug
	student_output = get_input(args)

	if not debug: rrf.SHOW_DEBUG = False

	if not (student_output == [] or student_output == """"""):
		rrf.__debug('student_output %s' % student_output)
		rrf.__debug('regex \'%s\'' % regex)

		# begin matching process against regex
		match_data = rrf.get_matches(student_output, regex)
		all_patterns = regex.split('|')
		matched_patterns = []

		for line, matches in match_data.items():
			for match in matches:
				matched_patterns.append(match[0])

		# what didn't get a match?
		unmatched_patterns = set(all_patterns) - set(matched_patterns)

		rrf.__debug(match_data)
		rrf.__debug('all_patterns ' + '[' + ', '.join(['\'%s\'' % str(p) for p in all_patterns]) + ']')
		rrf.__debug('matched_patterns ' + '[' + ', '.join(['\'%s\'' % str(p) for p in matched_patterns]) + ']')

		# all found patterns
		print('\n[FOUND]')
		for report in rrf.generate_match_report(match_data):
			print(report)

		# all patterns that were not found
		print('\n[NOT FOUND]')
		for pattern in unmatched_patterns:
			print('\'%s\'' % pattern)
		print('\n')

		return

	rrf.__error("No data present on \'stdin\'", exit=1)


if __name__ == '__main__':
	main(parse_args())

