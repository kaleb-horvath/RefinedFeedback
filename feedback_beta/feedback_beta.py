
import sys

def get_input (n_lines):
	"""Readlines from program 'stdin' until EOF is encountered
	or until no characters (including '\n') are encountered. This
	implies EOF on most systems. Should be called and passed to
	'get_matches' in 'feedback.py'.

	Parameters
	----------
	n_lines : int
		number of lines to read from stdin

	Returns
	-------
	student_output
		string representing lines from student's output

	Usage
	-----
	>>> # read ten lines from 'stdin' or until EOF
	>>> student_output = get_input(10) 
	"""
	lines_read = 0
	lines = ""
	# loop read from stdin until EOF encountered
	while True:
		try:
			if (lines_read != n_lines):
				line = sys.stdin.readline()

				if line == '': raise EOFError
				lines_read += 1
				lines += line
				continue
			break
		except EOFError: break 
		except IOError:
			rrf.__error('Problem reading from \'stdin\'', exit=1)
	lines = ''.join([
		l.replace('\n', '\u00B6') for l in lines
	])

	return lines


print(get_input(int(sys.argv[1])))