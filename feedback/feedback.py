
import sys, re
import sre_constants

SHOW_DEBUG = True
SHOW_ERROR = True

def __debug (message):
	if SHOW_DEBUG: print('DEBUG ', message) 
	return


def __error (message, exit=0):
	if SHOW_ERROR:
		print('ERROR ', message)
	if exit: sys.exit(1)
	return


def __associate_regex (word, regex):
	association = ''
	for pattern in regex.split('|'):
		if '*.' in pattern:
			literals = pattern.split('*.')
			try:
				assert False not in [l in word for l in literals]
				association = pattern

			except AssertionError: continue
		else:
			if pattern == word:
				association = pattern 

	return association


def get_matches (lines, regex):
	match_data = {}
	for index, line in enumerate(lines, start=1):

		__debug('searching line %d' % index)

		try:
			# returns iterator containing <_sre.SRE_Match object> references
			match_objects = re.finditer(regex, line)

		except sre_constants.error: __error('illegal regular expression pattern given')

		match_data[index] = []
		for match_object in match_objects:

			__debug(match_object)

			start, end = match_object.start(), match_object.end()
			word = match_object.group(0)
			substring_location = (start, end)

			match = (__associate_regex(word, regex),
				word,
				substring_location,
				line)

			match_data[index].append(match)

		if match_data[index] == []:
			__debug('no matches found on line %d' % index)

	return match_data


def generate_match_report (match_data):

	# calculate length of longest matched pattern for formatting purposes
	pattern_lengths = []
	for k, v in match_data.items():
		line = []
		for match in v:
			line.append(match[0])
		pattern_lengths.append(line)

	pattern_lengths = [len(l) for i in pattern_lengths for l in i]
	max_pattern_length = max(pattern_lengths)

	# yield the table annotated view headers
	regex_header = 'REGEX'
	lineno_header = 'LINE'
	match_header = 'MATCH'

	yield '%s' % regex_header + (' ' * (max_pattern_length - len(regex_header) + 4)) + lineno_header + '  %s' % match_header


	for l_index, matches in match_data.items():

		if matches == []: 
			# no matches on this line
			continue
		else:
			for match in matches:

				delim = ' '
				delimiter_chars = len(delim)

				# account for surrounding space in formatted string
				count = match[2][0] + delimiter_chars
				count += len(str(l_index)) + len(match[1])
				count += 6

				# here we calculate the appropriate padding
				current_pattern = match[0]
				padding = (max_pattern_length - len(current_pattern)) + 2
				#__debug('padding %d' % padding)
				spaces = '{:>' + str(count + max_pattern_length + 2) + '}'

				yield "\'{current_pattern}\'{padding}{index}    {delim}{line}\n{underscore}".format(
					underscore=spaces.format('^' * (len(match[1]))),
					current_pattern=str(current_pattern),
					padding=' ' * padding,
					index=l_index,
					line=match[3].strip(),
					delim=delim)

