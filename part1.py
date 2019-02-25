# Project Part I
# Justin Seeley and Alex Stylos
# CS 534 - Spring 2019
# Due __________ at __________

# Imports needed
# sys needed to format some outputs
import sys

# Path to graph node file
# Must be in same directory as python script
try:
	filepath = sys.argv[1]
except:
	print("Graph file not specified.")
	print("Usage:")
	print("> python part1.py <input.txt>")
	exit()

task_list = []
processor_list = []

class Task:
	def __init__(self, name="", length=0, unary_inclusive=[], unary_exlusive=[], binary_equal=[], binary_not_simul=[]):
		self.name = name
		self.length = length
		self.unary_inclusive = unary_inclusive 
		self.unary_exlusive = unary_exlusive
		self.binary_equal = binary_equal
		self.binary_not_equal = binary_not_equal
		self.binary_not_simul = binary_not_simul

# Will have costs associated with them in part II
class Processor:
	def __init__(self, name):
		self.name = name

file_line_count = 0
file_section_count = 0
## Loop to read graph data from .txt file and to store it in the nodes list
## using the functions above
# Reading in data from node file
try:
	with open(filepath) as fp:
		line = fp.readline()
		while line:

			# Process the line
			line_info = line.split()

			# don't do anything for the last line
			# if not line_info:
			# 	break
			if str.splitlines(line[0:5]) == ['#####']:
				file_section_count += 1
			else:
				# Ensuring file began correctly
				if file_section_count == 0:
					print("File did not begin with '#####'' marker")
					exit()

				# Choose what to do for each section


			
			print("{}:{} = {}".format(file_section_count, file_line_count, line_info))
			'''
			# If we hit the ##### marker dont do anything just move to next line
			# But signify that we are not adding distances and not connections
			if str.splitlines(line) == ['#####']:
				top_half = 0
			else:
				if top_half == 1:
					# find the node in the nodes list
					add_connection(line_info[0], line_info[1], line_info[2])
					current_node = Node(line_info[0], 0, line_info[1])
				else:
					add_distance(line_info[0], line_info[1])
			'''

			# Read next line
			line = fp.readline()
			file_line_count += 1 # count is for debugging and printing 

	fp.close()
except:
	print("Graph file '{}' could not be opened for reading.".format(filepath))
	print("Please check spelling and location of file.")
	exit()
