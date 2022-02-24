"""
:Date: 2022-02-23
:Version: 2
:Authors: - https://github.com/kaleb-horvath
:Purpose: This module allows 'feedback' directory to be passed to 'python3 <program name>'.


"""

from __future__ import print_function
import feedback as rrf
from utils import *

def main (args, debug=False):
	"""
	Program entryt point, performs matching process of student
	output (expected on stdin) against a regular expression
	(expected as command line argument, see 'python3 feedback --help')
	
	:param args: command line arguments passed to this program
	:param debug: show internal functionality as routines are executed

	:type debug: 'bool'
	:type args: 'argparse.Namespace'

	:Example:

	>>> main(parse_args(), debug=True)
	"""
	regex = str(args.regex)
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
	main(parse_args(),)

