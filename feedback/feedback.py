"""feedback.py

This file defines core program functionality and should be imported
as a module by __main__.py with the following functions being
made available:

	* get_matches - returns DS containing information about each matched literal 
	* generate_match_report - yields detailed strings that report each match
"""

import sys, re
import sre_constants

SHOW_DEBUG = True
SHOW_ERROR = True

def __debug (message):
	"""Simple debugging function, for internal use only
	"""
	if SHOW_DEBUG: print('DEBUG ', message) 
	return


def __error (message, exit=0):
	"""Error formatting function, for internal use only
	"""
	if SHOW_ERROR:
		print('ERROR ', message)
	if exit: sys.exit(1)
	return


def __associate_pattern (word, regex):
	"""Associate a regular expression with a literal that was
	definitely found within student_output. Should be called by
	'get_matches'. For internal use only.

	Parameters
	----------
	word : str
		the literal to be associated, should be 'm.group(0)' 
		where 'm' is some 'sre.SRE_Match object' instance found
		in the iterator returned by 're.finditer'
	regex : str
		the full regex used by 'get_matches'

	Returns
	-------
	association
		the first sub-pattern in regex that would result
		in a match with 'word'

	Usage
	-----
	>>> __associate_pattern('hello', 'he*.llo|world')
	'he*.llo'

	NOTE: Only works assuming literals to be matched are seperated
	using the stdlib RegEx 'or' operator, '|' within the passed
	regex string.
	"""
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
	"""Return a DS containing information about each matched literal. Still
	returns DS on no-matches, will contain empty lists. Should be called
	and passed to 'generate_match_report' as first and only argument. 
	Programmer should ensure 'lines' is not empty before calling this function.
	
	Parameters
	----------
	lines : list
		list of all lines read from stdin, should be result of 'utils.get_input'
	regex : str
		full regex pattern containing all literals to be matched

	Returns
	-------
	match_data 
		dictionary containing lists representing matches on each line,
		further containing an n-tuple representing each match

	Usage
	-----
	>>> from utils import *
	>>> ...
	>>> regex = 'hello*.world|this is not relevant'
	>>> match_data = get_matches(get_input(args, 10), regex)

	# this is what the dictionary will look like
	{1: [(..), ..], 2: ..}
	"""
	match_data = {}
	for index, line in enumerate(lines, start=1):

		__debug('searching line %d' % index)

		try:
			# returns iterator containing <_sre.SRE_Match object> references
			match_objects = re.finditer(regex, line, re.MULTILINE)

		except sre_constants.error: __error('illegal regular expression pattern given')

		match_data[index] = []
		for match_object in match_objects:

			__debug(match_object)

			start, end = match_object.start(), match_object.end()
			word = match_object.group(0)
			substring_location = (start, end)

			associated_pattern = __associate_pattern(word, regex)
			# __debug('associated_pattern %s' % associated_pattern)

			match = (associated_pattern,
				word,
				substring_location,
				line)

			match_data[index].append(match)

		if match_data[index] == []:
			__debug('no matches found on line %d' % index)

	return match_data


def generate_match_report (match_data):
	"""yields detailed strings that report each match with such information
	as line number, index, and the pattern that was matched. Essentially unpacks
	'match_data' DS returned by 'get_matches' and string formats it accordingly.
	Should be called by 'main' in __main__.py, and passed result of 'get_matches'.

	Parameters
	----------
	match_data : dict
		all matches found by 'finditer', built by 'get_matches' function

	Returns
	-------
	generator
		containing string representation of all literals matched
		(done using 'yield' statement)

	Usage
	-----
	>>> match_data = get_matches(student_output, regex)
	>>>
	>>> # show all matched pattern data
	>>> for match in generate_match_report(match_data):
		print(match)
	"""

	# calculate length of longest matched pattern for formatting purposes
	pattern_lengths = []
	for k, v in match_data.items():
		line = []
		for match in v:
			line.append(match[0])
		pattern_lengths.append(line)

	pattern_lengths = [len(l) for i in pattern_lengths for l in i]
	if pattern_lengths == []: return
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

