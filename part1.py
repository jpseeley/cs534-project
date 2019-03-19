# Project Part I
# Justin Seeley and Alex Stylos
# CS 534 - Spring 2019
# Due __________ at __________

# Imports needed
# sys needed to format some outputs
from random import shuffle
import sys
import time
import copy

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

constraint_list = []


class Constraint_Matrix:
	def __init__(self, m1, m2, domain, dim):
		self.m1 = m1
		self.m2 = m2
		self.bin_tag = 0
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
			for j in range(self.dim):
				if i != j:
					self.matrix[i][j] = 0
				else:
					if self.matrix[i][j] != 0:
						self.matrix[i][j] = 1
		self.bin_tag = 1

	def add_bin_ne(self):
		for i in range(self.dim):
			self.matrix[i][i] = 0
		self.bin_tag = 1

	def add_bin_ns(self, values):
		# print("valus = {}".format(values))
		m1_index = self.domain.index(values[0])
		m2_index = self.domain.index(values[1])
		self.matrix[m1_index][m2_index] = 0

	def cleanup(self):
		for i in range(self.dim):
			for j in range(self.dim):
				if self.matrix[i][j] == 2:
					self.matrix[i][j] = 1

# cm = Constraint_Matrix('C', 'G', ['p', 'q', 'r', 'x', 'y', 'z'], 6)

def print_matrix(matrix):
	# print("")
	for row in matrix:
		print(row)

def print_constraints(var):
	for c in constraint_list:
		if var == 'all':
			print("{}/{}".format(c.m1, c.m2))
			print_matrix(c.matrix)
		elif c.m1 == var or c.m2 == var:
			print("{}/{}".format(c.m1, c.m2))
			print_matrix(c.matrix)

# print_matrix(cm.matrix)
# cm.add_excl('C',['q', 'r'])
# cm.add_incl('G',['p', 'r', 'y', 'z'])
# cm.add_bin_e()
# cm.cleanup()
# print_matrix(cm.matrix)



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
		self.assignment = '?'
		# self.constraints = constraints

class CSP:
	def __init__(self, variables, domain, constraints, deadline):
		self.variables = variables
		self.domain = domain
		self.constraints = constraints
		self.deadline = deadline

	def get_index(self, value):
		return self.domain.index(value)

	def get_assignment(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				return var.assignment

	def get_domain(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				return var.domain

	def add_assignment(self, var_name, value):
		for var in self.variables:
			if var.name == var_name:
				var.assignment = value

	def remove_assignment(self, var_name):
		for var in self.variables:
			if var.name == var_name:
				var.assignment = '?'

	def print_assignments(self):
		for var in self.variables:
			print("{}[{}]	= {}".format(var.name, var.length, var.assignment))

	def get_constraint_val(self, m1, m2, val1, val2):
		value = 0
		for constraint in self.constraints:
			if constraint.m1 == m1 and constraint.m2 == m2:
				value = constraint.matrix[self.get_index(val1)][self.get_index(val2)]
			elif constraint.m2 == m1 and constraint.m1 == m2:
				value = constraint.matrix[self.get_index(val2)][self.get_index(val1)]
		return value

# var = Variable("C", 6, ['p', 'q', 'r', 'x', 'y', 'z'], Constraints())
# print(var.name)
# print(var.length)
# print(var.domain)

def print_csp(csp):
	print("Constraint Satisfaction Problem Status")
	for var in csp.variables:
		print("{}[{}] 	= {} of domain {} ".format(var.name, var.length, var.assignment, var.domain))

	# print("X: {}".format(csp.variables))
	# print("D: {}".format(csp.domain))
	# print("C: ...")
	# print("")



# def print_constraints(constraints):
	# print("unary_inclusive")



# Will have costs associated with them in part II
class Processor:
	def __init__(self, name):
		self.name = name



def list_diff(list_1, list_2):
    return list(set(list_1).symmetric_difference(set(list_2)))


deadline = 0
variable_list = []
var_name_list = []
domain_list = []
file_line_count = 0
file_section_count = 0
inclusive_list = []
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
			# print_constraints('C')
			# print("FILE SECTION # = {}".format(file_section_count))
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
				domain_list.append(line_info[0])
			elif file_section_count == 3: # deadline constraint
				deadline = line_info[0]

				# take the time to create a constraint matrix for all binary constraints
				for variable in variable_list:
					# print(variable.name)
					# print(var_name_list)
					adj_list = copy.deepcopy(var_name_list)
					adj_list.remove(variable.name)
					# print(adj_list)
					for var in adj_list:
						# Crate constraint matrix Variable\x
						copy_c_list = copy.deepcopy(constraint_list)
						already_inside = 0
						for constraint in copy_c_list:
							if constraint.m1 == var or constraint.m1 == var:
								already_inside = 1
						if not already_inside:
							constraint_list.append(Constraint_Matrix(variable.name, var, variable.domain, len(variable.domain)))
				# print(len(constraint_list))
			elif file_section_count == 4: # unary inclusive
				# inclusive_list.append(line_info[0]) # add current var to list
				# for constraint in constraint_list:
				# 	if constraint.m1 == line_info[0] or constraint.m2 == line_info[0]:
				# 		constraint.add_incl(line_info[0], line_info[1:len(line_info)])
				complement_set = list_diff(line_info[1:len(line_info)], domain_list)
				# print("{} -> {}".format(line_info[1:len(line_info)], complement_set))
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] or constraint.m2 == line_info[0]:
						constraint.add_excl(line_info[0], complement_set)
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
				for constraint in constraint_list:
					if constraint.m1 == line_info[0] and constraint.m2 == line_info[1]:
						constraint.add_bin_ns(line_info[2:4])

			# Choose what to do for each section

		# print("{}:{} = {}".format(file_section_count, file_line_count, line_info))

		# Read next line
		line = fp.readline()
		file_line_count += 1 # count is for debugging and printing 
fp.close()
# except:
# 	print("Graph file '{}' could not be opened for reading or another error has occurred.".format(filepath))
# 	print("Please check spelling and location of file.")
# 	print("{}".format(sys.exc_info()[0]))
# 	exit()


# # Clean up all matrices and fill in inclusive for those that were not specified
# unassigned_inclusive = diff(inclusive_list, var_name_list)
# print(unassigned_inclusive)
# for var in unassigned_inclusive:
# 	for constraint in constraint_list:
# 		if constraint.m1 == var or constraint.m2 == var:
# 			constraint.add_incl(var, domain_list)
for constraint in constraint_list:
	constraint.cleanup()


#### DATA IMPORT COMPLETED ####



# print_constraints('C')

#### BEGINNING CSP SOLUTION ####

# Create Constraint Satisfaction Problem with:
# Variables, Domain, & Constraints
csp_global = CSP(variable_list, domain_list, constraint_list, deadline)


def complete_assignment(csp):
	for var in csp.variables:
		if var.assignment == '?':
			return 0
	return 1



def get_sorted_mrv(csp):
	mrv = [[]]
	for var in csp.variables:
		if var.assignment == '?':
			if len(mrv[0]) == 0: # empty
				mrv[0] = [var.name, len(var.domain)]
			else:
				# do a looped comparison
				counter = 0
				did_assign = 0
				copy_mrv = copy.deepcopy(mrv)

				for var_mrv in copy_mrv:
					if var_mrv[1] > len(var.domain) and not did_assign: # 2 elt list
						mrv.insert(counter, [var.name, len(var.domain)])
						did_assign = 1
					counter += 1

				# if we didnt break
				if not did_assign:
					mrv.append([var.name, len(var.domain)])
	return mrv

def is_assigned(name, csp):
	for var in csp.variables:
		if var.name == name and var.assignment != '?':
			return 1
	return 0

def has_constraint(cm):
	counter = 0
	for i in range(len(cm.matrix[0])):
		for j in range(len(cm.matrix[0])):
			if cm.matrix[i][j] == 0:
				counter += 1
	return counter

def get_degree(csp, slice_mrv):
	deg = copy.deepcopy(slice_mrv) # make a copy of it
	for tie_mrv in slice_mrv:
		# have our ['C', 10] --> only need 'C'
		degree = 0
		for cm in csp.constraints:
			if cm.m1 == tie_mrv[0]:
				if (not is_assigned(cm.m2, csp)) and has_constraint(cm) and cm.bin_tag == 1:
					degree += 1
			elif cm.m2 == tie_mrv[0]: # have a cm for that variable
				if (not is_assigned(cm.m1, csp)) and has_constraint(cm) and cm.bin_tag == 1:
					degree += 1
		deg[slice_mrv.index(tie_mrv)] = [tie_mrv[0], degree]
	return deg

		# for var in csp.variables:
		# 	if var.assignment == '?':
		# 		if len(mrv[0]) == 0: # empty
		# 			mrv[0] = [var.name, len(var.domain)]
		# 		else:
		# 			# do a looped comparison
		# 			counter = 0
		# 			did_assign = 0
		# 			copy_mrv = copy.deepcopy(mrv)
		#			should not be running i dont think			
		# 			for var_mrv in copy_mrv:
		# 				if var_mrv[1] > len(var.domain) and not did_assign: # 2 elt list
		# 					mrv.insert(counter, [var.name, len(var.domain)])
		# 					did_assign = 1
		# 				counter += 1

		# 			# if we didnt break
		# 			if not did_assign:
		# 				mrv.append([var.name, len(var.domain)])
		# return mrv

# del csp.variables[0].domain[0]
# del csp.variables[0].domain[1]
# del csp.variables[1].domain[0]
# del csp.variables[1].domain[1]
# del csp.variables[4].domain[0]
# del csp.variables[4].domain[1]
# csp.variables[0].assignment = 'p'

# for var in csp.variables:
# 	if var.name != 'C':
# 		var.assignment = 'q'

# print(get_sorted_mrv(csp))


def sort_ascending(list1):
	sorted_list = sorted(list1, key=lambda x: x[1])
	return sorted_list


def select_unassigned(csp):
	# minimum remaining values heuristic
	mrv = get_sorted_mrv(csp)
	# print("### select_unassigned() - {} (mrv's) ###".format(mrv))

	# Solve simple case and create list for degree case
	if len(mrv) == 1:
		print("Selected variable {} because it was the only one left".format(mrv[0][0]))
		return mrv[0][0]	
	elif mrv[0][1] != mrv[1][1]: # singular mrv
		print("Selected variable {} because it had the least mrv (= {})".format(mrv[0][0], mrv[0][1]))
		return mrv[0][0]
	else:
		# They could all be the same 
		counter = 0
		slice_index = 0

		for var_mrv in mrv:
			if var_mrv[1] > mrv[0][1] and slice_index == 0:
				# print(var_mrv)
				slice_index = mrv.index(var_mrv)
		if not slice_index:
			slice_mrv = copy.deepcopy(mrv)
		else:
			slice_mrv = mrv[0:slice_index]
		# print("mrv ties: {}".format(slice_mrv))

		# create list of each tie with degree heuristic value
		deg_mrv = get_degree(csp, slice_mrv)
		# print("deg list: {}".format(deg_mrv))

		# sort list ascending order
		deg_sorted = sort_ascending(deg_mrv)
		# print("deg sort: {}".format(deg_sorted))

		# use variable in front
		print("Selected variable {} because it had the lowest degree heuristic (= {})".format(deg_sorted[0][0], deg_sorted[0][1]))

		return deg_sorted[0][0]

# print_constraints('C')
# print_constraints('D')

# select_unassigned(csp_global)






def order_domain_values(var_name, csp):
	# Using least-constraining-value heuristic
	# We are given a variable
	# 	1. Create a list of it's domain
	#		a. Each of those values will ultimately have a "score"
	#		b. Score is the # of domain elimanations it caused
	# 		c. We want to order them in ascending order to choose LCV
	# 	- Difficult part is the score part
	# 	- Idea1: create a snapshot (deepcopy) of the current variables
	#		- sum length of domain of every variable
	# 	- Iteratively change out the assignment of the current variable to this snapshot (C=p, C=q, etc.)
	#		- Use constraint matrices to delete domain elements in UNASSIGNED VARIABLES
	#		- sum length of domain of every variable, assign to 2-elt list 

	if len(csp.get_domain(var_name)) == 0:
		return []

	csp_copy = copy.deepcopy(csp)

	# old_domain_value = len(csp.get_domain(var_name))
	# get the current score
	domain_count = 0
	for var in csp_copy.variables:
		domain_count += len(var.domain)
	# print(domain_count)

	value_scores = [[]]
	for values in csp_copy.get_domain(var_name):
		if len(value_scores[0]) == 0:
			value_scores = [[values, 0]]
		else:
			value_scores.append([values, 0])
	# print("value scores: {}".format(value_scores))

	# print("##### order_domain_values() - FINDING LCV FOR {} #####".format(var_name))
	# for each of our potential values determine the change in domain
	for val_score in value_scores:
		csp_copy = copy.deepcopy(csp)
		# csp_copy.print_assignments()
		csp_copy.add_assignment(var_name, val_score[0]) # adds our testing assignment to the csp
		# csp_copy.print_assignments()

		# print("GETTING SCORE FOR VALUE {}".format(val_score[0]))
		current_score = 0

		# csp_copy.print_assignments()
		# now we need to perform arc consistency to eliminate domain values
		for var in csp_copy.variables:
			if var.assignment == '?': # only care about unassigned variables (including current one)
				# print("name={}".format(var.name))
				var_domain_copy = copy.deepcopy(var.domain)
				for value in var_domain_copy: # look at every domain value
					# csp_copy.add_assignment(var.name, value)
					if not is_consistent(var.name, value, csp_copy):
						# print("{} != {}".format())
						var.domain.remove(value)
						current_score += 1
						# print('{} domain => {}'.format(var.name, var.domain))
					# csp_copy.remove_assignment(var.name)
		# new_domain_count = 0
		# for var in csp_copy.variables:
			# new_domain_count += len(var.domain)
		val_score[1] = current_score

		# print("[{}] -> LCV_scores = {}".format(val_score[0], value_scores))

	sorted_value_scores = sort_ascending(value_scores)
	# print("Sorted LCV: {}".format(sorted_value_scores))
	sorted_values = []
	for scores in sorted_value_scores:
		sorted_values.append(scores[0])

	print("Domain of {} sorted using LCV as: {}".format(var_name, sorted_values))
	return sorted_values
	# fill in old domain values with current values


	# temporary random assignment until we get LCV working
	# for var in csp.variables:
	# 	if var.name == var_name:
	# 		shuffled_domain = copy.deepcopy(var.domain)
	# 		shuffle(shuffled_domain)
	# 		return shuffled_domain


def is_consistent(var_name, value, csp):
	# All but the deadline constraint
	for constraint in csp.constraints: # loop through each constraint
		if constraint.m1 == var_name:
			if csp.get_assignment(constraint.m2) != '?': # if other is assigned check that spot
				if constraint.matrix[csp.get_index(value)][csp.get_index(csp.get_assignment(constraint.m2))] == 0:
					# print("{}/{} != {}/{}".format(constraint.m1, constraint.m2, value, csp.get_assignment(constraint.m2)))
					return 0
			# else: # if unassigned
			# 	# check for at least one 1 in the row
			# 	one_flag = 0
			# 	for index in range(len(csp.domain)):
			# 		if constraint.matrix[csp.get_index(value)][index] == 1:
			# 			one_flag = 1
			# 	return one_flag
		elif constraint.m2 == var_name:
			if csp.get_assignment(constraint.m1) != '?': # if other is assigned check that spot
				if constraint.matrix[csp.get_index(csp.get_assignment(constraint.m1))][csp.get_index(value)] == 0:
					# print("{}/{} != {}/{}".format(constraint.m1, constraint.m2, csp.get_assignment(constraint.m1), value))
					return 0
			# else: # if unassigned
			# 	# check for at least one 1 in the column
			# 	one_flag = 0
			# 	for index in range(len(csp.domain)):
			# 		if constraint.matrix[index][csp.get_index(value)] == 1:
			# 			one_flag = 1
			# 	return one_flag



	# # All but the deadline constraint
	# for constraint in csp.constraints: # loop through each constraint
	# 	if constraint.m1 == var_name and csp.get_assignment(constraint.m2) != '?':
	# 		# print(csp.get_assignment(constraint.m2))
	# 		# print(csp.get_assignment(constraint.m1)) 
	# 		if constraint.matrix[csp.get_index(value)][csp.get_index(csp.get_assignment(constraint.m2))] == 0:
	# 			# print("{}/{} == {}/{}".format(constraint.m1, constraint.m2, value, csp.get_assignment(constraint.m2)))
	# 			return 0
	# 	elif constraint.m2 == var_name and csp.get_assignment(constraint.m1) != '?': 
	# 		# print(csp.get_assignment(constraint.m2))
	# 		# print(csp.get_assignment(constraint.m1))
	# 		if constraint.matrix[csp.get_index(csp.get_assignment(constraint.m1))][csp.get_index(value)] == 0:
	# 			# print("{}/{} == {}/{}".format(constraint.m1, constraint.m2, csp.get_assignment(constraint.m1), value))
	# 			return 0


	# Deadline constraint
	# Sum the length of each assigned
	proc_times = [[]]

	# Create empty list for each processor
	for proc in csp.domain:
		if len(proc_times[0]) == 0:
			proc_times = [[proc, 0]]
		else:
			proc_times.append([proc, 0])
	# print(proc_times)

	for var in csp.variables:
		if var.assignment != '?':
			for p_t in proc_times:
				# print("{} {}".format(p_t[0], p_t[1]))
				# print(var.length)
				if p_t[0] == var.assignment:
					p_t[1] = p_t[1] + int(var.length)
	# print(proc_times)

	for p_t in proc_times:
		if int(p_t[1]) > int(csp.deadline):
			return 0

	return 1

def backtracking_search(csp):
	if recursive_backtracking(csp): # success
		print("\nSuccess - Solution Found:")
		csp.print_assignments()
	else:
		print("No solution could be found")

def recursive_backtracking(csp):
	if complete_assignment(csp):
		return csp.variables
	var_name = select_unassigned(csp)
	# time.sleep(1)
	for value in order_domain_values(var_name, csp):
		if is_consistent(var_name, value, csp):
			print("{} == {} is consistent, adding to assignment".format(var_name, value))
			csp.add_assignment(var_name, value)
			# csp.print_assignments()
			##### 
			# inferences = inference(csp, variable, value) # AC-3 stuff
			# if inferences != failure:
				# add_inferences(assignment, inferences)
			#####

			result = recursive_backtracking(csp)
			if result:
				return 1
		else:
			print("{} == {} is not consistent".format(var_name, value))

		csp.remove_assignment(var_name)
		#####
		# remove_inferences(inferences, assignment)
		#####
	return 0



'''
def recursive_backtracking(assignment, csp):
	if complete_assignment(csp):
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

# print_constraints('C')

def create_ac_3_queue(csp):
	queue = [[]]
	for constraint in csp.constraints:
		if len(queue[0]) == 0: # initialize
			queue = [[constraint.m1, constraint.m2]]
			queue.append([constraint.m2, constraint.m1])
		else:
			queue.append([constraint.m1, constraint.m2])
			queue.append([constraint.m2, constraint.m1])
	return queue

# print create_ac_3_queue(csp_global)

# print csp_global.get_constraint_val('D', 'C', 'p', 'p')

# Revise
def revise(csp, arc):
	revised = 0
	X_i = arc[0]
	X_j = arc[1]
	satisfy_flag = 0

	# copy just in case because we are deleting while looping
	X_i_copy = copy.deepcopy(csp.get_domain(X_i))

	for x in X_i_copy:
		satisfy_flag = 0
		for y in csp.get_domain(X_j):
			if csp.get_constraint_val(X_i, X_j, x, y):
				satisfy_flag = 1
		if not satisfy_flag:
			csp.get_domain(X_i).remove(x)
			revised = 1
	return revised


#### AC-3 testing
# Arc format is (Xi, Xj) where:
# 	The direction is the effect Xj has on Xi 
#	so, its counterintuitive
def ac_3(csp):
	queue = create_ac_3_queue(csp) # form initial arcs just from names of all constraints and reverse
	# print(queue)
	X_i = 0
	X_j = 0
	while len(queue):
		arc = queue.pop(0) # arc = (Xi, Xj)
		X_i = arc[0]
		X_j = arc[1]
		if revise(csp, arc):
			print("arc ({}, {}) revised domain of {} to {}".format(X_i, X_j, X_i, csp.get_domain(X_i)))
			if len(csp.get_domain(X_i)) == 0: # size of X
				print("Inconsistency: revised domain of {} was reduced to zero".format(X_i))
				return 0
			for constraint in csp.constraints:
				# Neighbors are constraint matrices with Xi
				if constraint.m1 == X_i and constraint.m2 != X_j:
					queue.append([constraint.m2, X_i])
				elif constraint.m2 == X_i and constraint.m1 != X_j:
					queue.append([constraint.m1, X_i])
		else:
			print("arc ({}, {}) did not revise domain of {}".format(X_i, X_j, X_i))

	return 1

print("Initial CSP")
print_csp(csp_global)
print("\nPre-processing AC-3...")
ac_3(csp_global)

print("\nCSP after AC-3")
print_csp(csp_global)

print("\nBeginning Backtracking Search")
backtracking_search(csp_global)
# print_csp(csp_global)
# print_constraints('all')


#### OLD ALGORITHM ####
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





















