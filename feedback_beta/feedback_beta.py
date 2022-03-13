
import sys, re
import sre_constants



def get_input (n_lines):
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

def __associate_pattern (word, regex):
	association = ''
	for pattern in regex.split('|'):
		if '.*' in pattern:
			literals = pattern.split('.*')
			try:
				assert False not in [l in word for l in literals]
				association = pattern

			except AssertionError: continue
		else:
			if pattern == word:
				association = pattern 

	return association

def get_matches (student_output, regex):
	match_data = {}
	match_objects = re.finditer(
		regex, 
		student_output, 
		re.MULTILINE
	)
	matches = 0
	for match_object in match_objects:
		matches += 1
		start, end = match_object.start(), match_object.end()
		word = match_object.group(0)
		substring_location = (start, end)

		associated_pattern = __associate_pattern(word, regex)

		match = (associated_pattern,
			word,
			substring_location)

		match_data[matches] = match 

	return match_data

student_output = get_input(int(sys.argv[1]))
match_data = get_matches(student_output, sys.argv[2])
print(match_data)