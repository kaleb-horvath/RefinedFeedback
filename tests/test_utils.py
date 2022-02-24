"""test_utils.py

This module performs unit testing over the functions found in 'utils.py'
using the 'unittest' framework provided by the Python3 stdlib.

NOTE: In reality, the only code we are testing here is the 'get_input'
function. We have a few different options. We could spawn
a subprocess, write to its 'stdin', capture the output, and 
assert its equality with the expected. 

OR

import the 'get_input' method, write to our own 'stdin' and then check. will
introduce blocking issues because method will never encounter EOF?
"""
import unittest
import os
import sys

try:
	from feedback import utils

except ImportError:
	this_module = os.path.basename(__file__)
	print(
		'%s: ERROR ' % this_module, 
		'missing one or more required modules'
	)
	sys.exit(1)


class TestGetInput (unittest.TestCase):

	# fields for writing to stdin
	command = 'echo \'%s\' > /proc/%s/fd/0'
	pid = os.getpid()

	# all test inputs to write to stdin, pilcrow should be present
	student_outputs = [
	'hello world 4',
	'this is a test case',
	'this is a multiline\ntest case',
	'this one has blank\n\nlines'
	]
	expected = [l.replace('\n', '\u00B6') for l in student_outputs]



	def test_case_1 (self):
		"""
		"""
		print('\nRunning Test Case 1 for TestGetInput\n')

		# get length of longest student output in lines
		most_lines = max([
			len(output.split('\n')) for output in self.student_outputs
		])
		for case in self.student_outputs:
			os.system(self.command % (case, self.pid))

			# gather student output off of stdin, should already be written
			# not encountering EOF?
			lines = utils.get_input(False, most_lines, test_mode=True)

			print(case, lines)
			continue

if __name__ == '__main__':
	unittest.main()
