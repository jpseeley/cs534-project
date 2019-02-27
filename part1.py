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

class Constraints:
	def __init__(self, unary_inclusive=[], unary_exlusive=[], binary_equal=[], binary_not_equal=[], binary_not_simul=[]):
		self.unary_inclusive = unary_inclusive 
		self.unary_exlusive = unary_exlusive
		self.binary_equal = binary_equal
		self.binary_not_equal = binary_not_equal
		self.binary_not_simul = binary_not_simul

class Variable:
	def __init__(self, name="", length=0, domain=[], constraints=Constraints([],[],[],[],[])):
		self.name = name
		self.length = length
		self.domain = domain
		self.constraints = constraints

class CSP:
	def __init__(self, variables, domain, constraints):
		self.variables = variables
		self.domain = domain
		self.constraints = constraints

var = Variable("C", 6, ['p', 'q', 'r', 'x', 'y', 'z'], Constraints())
print(var.name)
print(var.length)
print(var.domain)
print(var.constraints.unary_inclusive)
print(var.constraints.unary_exlusive)
print(var.constraints.binary_equal)

def print_csp(csp):
	print("Constraint Satisfaction Problem")
	print("X: {}".format(CSP.variables))
	print("D: {}".format(CSP.domain))
	print("C:   ")
	print("")

def print_constraints(constraints):
	print("unary_inclusive")



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

			# Read next line
			line = fp.readline()
			file_line_count += 1 # count is for debugging and printing 

	fp.close()
except:
	print("Graph file '{}' could not be opened for reading.".format(filepath))
	print("Please check spelling and location of file.")
	exit()
