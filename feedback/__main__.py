"""__main__.py

Program entry point.
"""

from __future__ import print_function
import sys 

try:
	from utils import parse_args, get_input
	import feedback as rrf

except ImportError:
	print('ERROR ', 'missing one or more required modules')
	sys.exit(1)


def main (args, debug=False):
	"""Performs matching process of student output
	(expected on stdin) against a regular expression
	(expected as command line argument)

	Parameters
	----------
	args : argparse.Namespace
		command line arguments passed to this program
	debug : bool
		flag used to show internal functionality as routines are executed

	Usage
	-----
	>>> main(parse_args(), debug=True)
	"""
	regex = str(args.regex)
	student_output = get_input(args, int(args.lines))

	rrf.SHOW_DEBUG = debug

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


		# debugging entries for various pattern categories
		rrf.__debug(match_data)
		rrf.__debug('matched_patterns ' + '[' + ', '.join(['\'%s\'' % str(p) for p in matched_patterns]) + ']')
		rrf.__debug('all_patterns ' + '[' + ', '.join(['\'%s\'' % str(p) for p in all_patterns]) + ']')

		print('\n[FOUND]')
		for report in rrf.generate_match_report(match_data):
			print(report)

		print('\n[NOT FOUND]')
		for pattern in unmatched_patterns:
			print('\'%s\'' % pattern)
		print('\n')

		return

	rrf.__error("No data present on \'stdin\'", exit=1)


# driver code
if __name__ == '__main__':
	main(parse_args(), debug=True)

