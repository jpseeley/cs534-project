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
	print("Input file not specified.")
	print("Usage:")
	print("> python part1.py <input.txt>")
	exit()

# We could either have a full list of constraints for each variable within each variable object
# This simplifies things like arc-consistency, etc. but makes the setup hard. It also makes it not universal. Say
# we have a constraint that all are not the same, we would have to create a binary constraint with each variable and that 
# would be hard on the beginning. 

class Constraint_Matrix:
	def __init__(self, m1, m2, domain, dim):
		self.m1 = m1
		self.m2 = m2
		self.dim = dim
		self.domain = domain
		self.matrix = self.make_matrix(dim)

	def make_matrix(self, dim):
		matrix = [[2 for x in range(dim)] for y in range(dim)]
		return matrix

	def add_excl(self, name, excl):
		for value in excl:
			for i in range(self.dim):
				if name==self.m1:
					self.matrix[self.domain.index(value)][i] = 0
				else:
					self.matrix[i][self.domain.index(value)] = 0

	def add_incl(self, name, excl):
		for value in excl:
			for i in range(self.dim):
				if name==self.m1:
					if self.matrix[self.domain.index(value)][i] != 0:
						self.matrix[self.domain.index(value)][i] = 1
				else:
					if self.matrix[i][self.domain.index(value)] != 0:
						self.matrix[i][self.domain.index(value)] = 1

	def add_bin_e(self):
		for i in range(self.dim):
			if self.matrix[i][i] != 0:
				self.matrix[i][i] = 1

	def add_bin_ne(self):
		for i in range(self.dim):
			self.matrix[i][i] = 0

	def cleanup(self):
		for i in range(self.dim):
			for j in range(self.dim):
				if self.matrix[i][j] == 2:
					self.matrix[i][j] = 0

cm = Constraint_Matrix('C', 'G', ['p', 'q', 'r', 'x', 'y', 'z'], 6)

def print_matrix(matrix):
	# print("")
	for row in matrix:
		print(row)

print_matrix(cm.matrix)
cm.add_excl('C',['q', 'r'])
cm.add_incl('G',['p', 'r', 'y', 'z'])
cm.add_bin_e()
cm.cleanup()
print_matrix(cm.matrix)


# cm = [[0]]

# def dim_increase(matrix):
# 	dim = len(matrix) 
# 	row_plus_one = [0]*(dim+1)
# 	matrix.append(row_plus_one)
# 	counter = 0
# 	while counter < dim:
# 		matrix[counter] = row_plus_one[:]
# 		counter += 1

# def print_matrix_test():
# 	count = 0
# 	print("matrix print")
# 	while count < 3:
# 		print(cm)
# 		dim_increase(cm)
# 		count += 1	
# 	print("end matrix print")
# print_matrix_test()

# id_cm = [[1,0,0],[0,1,0],[0,0,1]]

# def identity_matrix(matrix):
# 	id_matrix = matrix[:]
# 	counter = 0
# 	# print(id_matrix)
# 	while counter < len(id_matrix):
# 		#print(id_matrix)
# 		id_matrix[counter][counter] = 1

# 		counter += 1
# 	#print(id_matrix)
# 	return id_matrix

# print(identity_matrix(cm))
# print()
# print(cm)
# cm[0][0] = 1
# #cm[1][1] = 1
# #cm[2][2] = 1
# print(cm)


'''
variable_list = []
domain_list = []
cm = [[]]
print(cm)
cm[0].append(0)
cm.append([])
print(cm)
'''

# class Constraints:
# 	def __init__(self, unary_inclusive=[], unary_exlusive=[], binary_equal=[], binary_not_equal=[], binary_not_simul=[]):
# 		self.unary_inclusive = unary_inclusive 
# 		self.unary_exlusive = unary_exlusive
# 		self.binary_equal = binary_equal
# 		self.binary_not_equal = binary_not_equal
# 		self.binary_not_simul = binary_not_simul

class Variable:
	def __init__(self, name='', length=0, domain=[]):
		self.name = name
		self.length = length
		self.domain = domain
		# self.constraints = constraints

class CSP:
	def __init__(self, variables, domain, constraints):
		self.variables = variables
		self.domain = domain
		self.constraints = constraints

# var = Variable("C", 6, ['p', 'q', 'r', 'x', 'y', 'z'], Constraints())
# print(var.name)
# print(var.length)
# print(var.domain)

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


constraint_list = []


deadline = 0
variable_list = []
var_name_list = []
file_line_count = 0
file_section_count = 0
## Loop to read graph data from .txt file and to store it in the nodes list
## using the functions above
# Reading in data from node file
# try:
with open(filepath) as fp:
	line = fp.readline()
	while line:

		# Process the line
		line_info = line.split()

		if str.splitlines(line[0:5]) == ['#####']:
			file_section_count += 1
		else:
			# Ensuring file began correctly
			if file_section_count == 0:
				print("File did not begin with '#####'' marker")
				exit()

			if file_section_count == 1: # variables
				variable_list.append(Variable(line_info[0], line_info[1], []))
				var_name_list.append(line_info[0])
			elif file_section_count == 2: # values
				for var in variable_list:
					var.domain.append(line_info[0])
			elif file_section_count == 3: # deadline constraint
				deadline = line_info[0]

				# take the time to create a constraint matrix for all binary constraints
				for variable in variable_list:
					# print(variable.name)
					# print(var_name_list)
					adj_list = var_name_list[:]
					adj_list.remove(variable.name)
					# print(adj_list)
					for var in adj_list:
						# Crate constraint matrix Variable\x
						copy_c_list = constraint_list[:]
						already_inside = 0
						for constraint in copy_c_list:
							if constraint.m1 == var or constraint.m1 == var:
								already_inside = 1
						if not already_inside:
							constraint_list.append(Constraint_Matrix(variable.name, var, variable.domain, len(variable.domain)))
				# print(len(constraint_list))
			elif file_section_count == 4: # unary inclusive
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] or constraint.m2 == line_info[0]:
						constraint.add_incl(line_info[0], line_info[1:len(line_info)])
			elif file_section_count == 5: # unary exclusive
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] or constraint.m2 == line_info[0]:
						constraint.add_excl(line_info[0], line_info[1:len(line_info)])
			elif file_section_count == 6: # binary equals
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] and constraint.m2 == line_info[1]:
						constraint.add_bin_e()
			elif file_section_count == 7: # binary not equals
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] and constraint.m2 == line_info[1]:
						constraint.add_bin_ne()
			elif file_section_count == 8: # binary not simultaneous
				i = 1


			# Choose what to do for each section

		print("{}:{} = {}".format(file_section_count, file_line_count, line_info))

		# Read next line
		line = fp.readline()
		file_line_count += 1 # count is for debugging and printing 

# Clean up all matrices
for constraint in constraint_list:
	constraint.cleanup()

def print_constraints(var):
	for c in constraint_list:
		if c.m1 == var or c.m2 == var:
			print("{}/{}".format(c.m1, c.m2))
			print_matrix(c.matrix)

print_constraints('C')


fp.close()
# except:
# 	print("Graph file '{}' could not be opened for reading.".format(filepath))
# 	print("Please check spelling and location of file.")
# 	exit()

def complete_assignment():
	return true

'''
def recursive_backtracking(assignment, csp):
	if complete_assignment(assignment):
		return assignment
	variable = select_unassigned(assignemnt, csp)

	for d in order_domain(variable):
		if consistent(d, assignment, csp):
			add_value(d, assignment)
			result = recursive_backtracking(assignment, csp)
			if success(result):
				return result
		remove_value(d, assignment)
	return false
'''
'''
def recursive_backtracking(assignment, csp):
	if complete_assignment(assignment):
		return assignment
	variable = select_unassigned(assignemnt, csp)

	for value in order_domain(variable, assignment, csp):
		if consistent(value, assignment, csp):
			add_value(value, assignment)
			inferences = inference(csp, variable, value) # AC-3 stuff
			if inferences != failure:
				add_inferences(assignment, inferences)
				result = recursive_backtracking(assignment, csp)
				if success(result):
					return result
		remove_value(value, assignment)
		remove_inferences(inferences, assignment)
	return failure



'''
































