#!/usr/bin/python

from __future__ import print_function
import argparse
import sys
import re
import string

def generate_pattern(arguments):
	return re.compile('({}):\s*(\S.*)'.format('|'.join(arguments)))

class ParserParameter:
	arguments = ('description', 'epilog', 'prog')

	pattern = generate_pattern(arguments)

	def __init__(self):
		self.params = {}

	def update_line(self, line):
		match = self.pattern.match(line)
		if match:
			self.params[match.group(1)] = match.group(2)

	def merge(self, other):
		self.params.update(other.params)

class ArgumentParameter:
	arguments = ('action', 'nargs', 'const', 'default', 'type', 'choices',
		'required', 'help', 'metavar', 'dest')

	pattern = generate_pattern(arguments)

	def __init__(self):
		self.params = {}
		self.names = []

	def update_line(self, line):
		match = self.pattern.match(line)
		if match:
			self.params[match.group(1)] = eval(match.group(2))
		else:
			self.names.extend(line.split())

class DeadParameter:
	def update_line(self, line):
		pass

def create_parser(input_lines):
	parameters = []
	current_parameter = DeadParameter()

	#parse input.
	for line in input_lines:
		line = line.strip()
		if line == ':parser:':
			parameters.append(current_parameter)
			current_parameter = ParserParameter()
		elif line == ':argument:':
			parameters.append(current_parameter)
			current_parameter = ArgumentParameter()
		elif line == ':end:':
			parameters.append(current_parameter)
			current_parameter = DeadParameter()
			break
		elif line == '':
			pass
		else:
			current_parameter.update_line(line)

	parameters.append(current_parameter)

	combined = ParserParameter()

	#merge all parser parameters
	for param in parameters:
		if isinstance(param, ParserParameter):
			combined.merge(param)

	#Then remove them. This also takes care of the DeadParameter
	argument_parameters = [x for x in parameters if isinstance(x, ArgumentParameter)]

	constructed_parser = argparse.ArgumentParser(
	    formatter_class=argparse.ArgumentDefaultsHelpFormatter, **combined.params)

	for argument in argument_parameters:
		constructed_parser.add_argument(*argument.names, **argument.params)

	return constructed_parser

def make_variable_name(var):
	valid_chars = string.letters + string.digits + '_'

	def replace_char(char):
		if char == '-':
			return '_'
		elif char in valid_chars:
			return char
		return ''

	return ''.join(map(replace_char, var))

def escape_quotes(var):
	return re.sub('"', '\\"', str(var))

def make_variable_data(var):
	if var is None:
		return ''
	elif var is True:
		return 'true'
	elif var is False:
		return 'false'
	elif isinstance(var, list):
		return ' '.join(map(make_variable_data, var))
	else:
		return escape_quotes(var)

def main():
	parser = create_parser(sys.stdin)

	try:
		parsed_arguments = vars(parser.parse_args())
	except SystemExit:
		exit(10)

	for argument_name, argument_data in parsed_arguments.items():
		argument_name = make_variable_name(argument_name)
		argument_data = make_variable_data(argument_data)

		print('{}="{}";'.format(argument_name, argument_data))

	exit(0)

if __name__ == '__main__':
	main()


