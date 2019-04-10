
# Constraint_Matrix Class:
# 	Provides constraint information for two variables binary and unary constraints
class Constraint_Matrix:
	def __init__(self, m1, m2, domain, dim):
		self.m1 = m1 # variables name 1
		self.m2 = m2 # variables name 2
		self.bin_tag = 0 # used in degree heuristic
		self.dim = dim # dim x dim matrix size
		self.domain = domain # domain of values that variables can possess
		self.matrix = self.make_matrix(dim) # create an empty matrix on instantiation

	# Make an empty matrix of unassigned values
	def make_matrix(self, dim):
		matrix = [[2 for x in range(dim)] for y in range(dim)]
		return matrix

	# Add unary exclusive constraint
	def add_excl(self, name, excl):
		for value in excl:
			for i in range(self.dim):
				if name==self.m1:
					self.matrix[self.domain.index(value)][i] = 0
				else:
					self.matrix[i][self.domain.index(value)] = 0

	# Add unary inclusive constraint
	# Note: This is not used in script				
	def add_incl(self, name, excl):
		for value in excl:
			for i in range(self.dim):
				if name==self.m1:
					if self.matrix[self.domain.index(value)][i] != 0:
						self.matrix[self.domain.index(value)][i] = 1
				else:
					if self.matrix[i][self.domain.index(value)] != 0:
						self.matrix[i][self.domain.index(value)] = 1

	# Add binary equals constraint
	def add_bin_e(self):
		for i in range(self.dim):
			for j in range(self.dim):
				if i != j:
					self.matrix[i][j] = 0
				else:
					if self.matrix[i][j] != 0:
						self.matrix[i][j] = 1
		self.bin_tag = 1

	# Add binary not equals constraint
	def add_bin_ne(self):
		for i in range(self.dim):
			self.matrix[i][i] = 0
		self.bin_tag = 1

	# Add binary not simultaneous constraint
	def add_bin_ns(self, values):
		m1_index = self.domain.index(values[0])
		m2_index = self.domain.index(values[1])
		self.matrix[m1_index][m2_index] = 0

	# Convert unassigned values in matrix to 1
	def cleanup(self):
		for i in range(self.dim):
			for j in range(self.dim):
				if self.matrix[i][j] == 2:
					self.matrix[i][j] = 1

# Variable class:
# 	Defines CSP variable (task)
class Variable:
	def __init__(self, name='', length=0, domain=[]):
		self.name = name # name of variable
		self.length = length # length of variable
		self.domain = domain # current domain of variable
		self.assignment = '?' # current assignment of variable

# CSP Class:
#	Defines CSP with:
#	variables
#	domain
#	constraints
class CSP:
	def __init__(self, variables, domain, constraints, deadline):
		self.variables = variables # list of variable class objects
		self.domain = domain # list of domain values
		self.constraints = constraints # list of constraint matrices
		self.deadline = deadline # deadline constraint

	# Return matrix index of given domain value
	# Common to all variables
	def get_index(self, value):
		return self.domain.index(value)

 	# Returns assignment of given variable name
	def get_assignment(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				return var.assignment

	# Returns domain list of given variable name
	def get_domain(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				return var.domain

	# Add assignment of given value to given variable
	def add_assignment(self, var_name, value):
		for var in self.variables:
			if var.name == var_name:
				var.assignment = value

	# Remove assignment from given variable name
	def remove_assignment(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				var.assignment = '?'

	# Print assignment for each variable
	def print_assignments(self):
		for var in self.variables:
			print("{}[{}]	= {}".format(var.name, var.length, var.assignment))

	# Get value at (i, j) within constraint matrix
	# Given m1 and m2 (variable name) and
	# val1 and val2 (value names)
	# Returns 0 or 1 from constraint matrix
	def get_constraint_val(self, m1, m2, val1, val2):
		value = 0
		for constraint in self.constraints:
			if constraint.m1 == m1 and constraint.m2 == m2:
				value = constraint.matrix[self.get_index(val1)][self.get_index(val2)]
			elif constraint.m2 == m1 and constraint.m1 == m2:
				value = constraint.matrix[self.get_index(val2)][self.get_index(val1)]
		return value