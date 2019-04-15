# Project Part I
# Justin Seeley and Alex Stylos
# CS 534 - Spring 2019
# Due 3/19/2019 at 10:59AM

# Imports needed
from random import shuffle
import sys
import time
import copy
from data_objects import Constraint_Matrix, Variable, CSP
from constraint_input_reader import ConstrainInputReader

# Path to graph node file
# Must be in same directory as python script
try:
	input_file = sys.argv[1]
except:
	print("Input file not specified.")
	print("Usage:")
	print("> python part1.py <input.txt>")
	exit()

# Global variables for file reading
constraint_list = [] #####
deadline = 0
variable_list = [] ######
domain_list = [] #####
input_sections = 8

# Print out matrix row by row
def print_matrix(matrix):
	for row in matrix:
		print(row)

# Print constraint matrices:
# 	'all': print all constraints
#	'x': matrices with 'x' 
def print_constraints(var):
	for c in constraint_list:
		if var == 'all':
			print("{}/{}".format(c.m1, c.m2))
			print_matrix(c.matrix)
		elif c.m1 == var or c.m2 == var:
			print("{}/{}".format(c.m1, c.m2))
			print_matrix(c.matrix)

# Print CSP variables, current assignment, and current domain
def print_csp(csp):
	print("Constraint Satisfaction Problem Status")
	for var in csp.variables:
		print("{}[{}] 	= {} of domain {} ".format(var.name, var.length, var.assignment, var.domain))

#### DATA IMPORT COMPLETED  ####
#### BEGINNING CSP SOLUTION ####

# Create Constraint Satisfaction Problem with:
# Variables, Domain, & Constraints
csp_global = ConstrainInputReader(input_file, input_sections).get_constrain_problem()

# Return 1 is all variables in csp are assigned, 0 if any are not
def complete_assignment(csp):
	for var in csp.variables:
		if var.assignment == '?':
			return 0
	return 1

# Returns list of sorted in ascending order, the remaining unassigned values in the csp
def get_sorted_remaining_values(csp):
	mrv = [[]] 
	for var in csp.variables:
		if var.assignment == '?': # unassigned variable
			if len(mrv[0]) == 0: # empty
				mrv[0] = [var.name, len(var.domain)]
			else:
				counter = 0
				did_assign = 0
				copy_mrv = copy.deepcopy(mrv)

				# Compare to other values in list to sort in ascending order
				for var_mrv in copy_mrv:
					if var_mrv[1] > len(var.domain) and not did_assign: # 2 elt list
						mrv.insert(counter, [var.name, len(var.domain)])
						## TODO: make this an if/else statement
						did_assign = 1
					counter += 1

				# if we did not insert the new mrv value, it means it is the largest
				if not did_assign:
					mrv.append([var.name, len(var.domain)])
	return mrv

# Returns 1 if the given variable is asssigned, 0 if not
def is_assigned(name, csp):
	for var in csp.variables:
		if var.name == name and var.assignment != '?':
			return 1
	return 0

# Returns number of 0's in given constraint matrix
def has_constraint(cm):
	counter = 0
	for i in range(len(cm.matrix[0])):
		for j in range(len(cm.matrix[0])):
			if cm.matrix[i][j] == 0:
				counter += 1
	return counter

# Given list of variables, returns list of variables with values according to degree heuristic
def get_degree(csp, slice_mrv):
	deg = copy.deepcopy(slice_mrv) # make a copy of it
	# counter the change in degree for each value
	for tie_mrv in slice_mrv:
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

# Sort given list in ascending order
# list1 format: [[a, 3],...,[b, 5]]
def sort_ascending(list1):
	sorted_list = sorted(list1, key=lambda x: x[1])
	return sorted_list

# Select unassigned variables in csp according to minimum-remaining-values heuristic
# Break ties with degree heuristic
def select_unassigned(csp):
	# minimum remaining values heuristic
	mrv = get_sorted_remaining_values(csp)
	# print("### select_unassigned() - {} (mrv's) ###".format(mrv))

	# Solve simple case and create list for degree case
	if len(mrv) == 1:
		print("Selected variable {} because it was the only one left".format(mrv[0][0]))
		return mrv[0][0]	
	elif mrv[0][1] != mrv[1][1]: # singular mrv
		print("Selected variable {} because it had the least mrv (= {})".format(mrv[0][0], mrv[0][1]))
		return mrv[0][0]
	else:
		# We need to break the tie with the degree heuristic
		counter = 0
		slice_index = 0

		# Slice only the ties from mrv 
		for var_mrv in mrv:
			# var_mrv[1] being the current item in the list vs. the first item (mrv[0][1]) in the list
			if var_mrv[1] > mrv[0][1] and slice_index == 0:
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

		# use variable in front (variable with lowest degree)
		print("Selected variable {} because it had the lowest degree heuristic (= {})".format(deg_sorted[0][0], deg_sorted[0][1]))

		return deg_sorted[0][0]

# Orders the domain values for given variable according to
# least-constraining-value heuristic
def order_domain_values(var_name, csp):
	# Using least-constraining-value heuristic
	# We are given a variable
	# 	1. Create a list of it's domain
	#		a. Each of those values will ultimately have a "score"
	#		b. Score is the # of domain elimanations it caused
	# 		c. We want to order them in ascending order to choose LCV
	# 	- Ceate a snapshot (deepcopy) of the current variables
	#		- sum domain change for every variable
	# 	- Iteratively change out the assignment of the current variable to this snapshot (C=p, C=q, etc.)
	#	- Sort list in ascending order

	# An empty domain can be eliminated instantly
	if len(csp.get_domain(var_name)) == 0:
		return []

	# Snapshot of CSP to work with
	csp_copy = copy.deepcopy(csp)

	# Intialize score list for each domain value
	value_scores = [[]]
	for values in csp_copy.get_domain(var_name):
		if len(value_scores[0]) == 0:
			value_scores = [[values, 0]]
		else:
			value_scores.append([values, 0])
	# print("value scores: {}".format(value_scores))

	# for each of our potential values determine the change the domain change
	for val_score in value_scores:
		csp_copy = copy.deepcopy(csp)
		# csp_copy.print_assignments()
		csp_copy.add_assignment(var_name, val_score[0]) # adds our testing assignment to the csp
		# csp_copy.print_assignments()

		# print("GETTING SCORE FOR VALUE {}".format(val_score[0]))
		current_score = 0

		# csp_copy.print_assignments()
		# now we need to enforce consistency to eliminate domain values
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
		val_score[1] = current_score

		# print("[{}] -> LCV_scores = {}".format(val_score[0], value_scores))

	# Sort score list in ascending order
	sorted_value_scores = sort_ascending(value_scores)
	# print("Sorted LCV: {}".format(sorted_value_scores))

	# remove scores from sorted list, only return variables
	sorted_values = []
	for scores in sorted_value_scores:
		sorted_values.append(scores[0])

	print("Domain of {} sorted using LCV as: {}".format(var_name, sorted_values))
	return sorted_values

# Returns 1 if given new variable and value would be consistent with given csp
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

	# Compute the time for each value 
	for var in csp.variables:
		if var.assignment != '?':
			for p_t in proc_times:
				# print("{} {}".format(p_t[0], p_t[1]))
				# print(var.length)
				if p_t[0] == var.assignment:
					p_t[1] = p_t[1] + int(var.length)
		if var.name == var_name: # adding in the new assignment
			for p_t in proc_times:
				# print("{} {}".format(p_t[0], p_t[1]))
				# print(var.length)
				if p_t[0] == value:
					p_t[1] = p_t[1] + int(var.length)
	# print(proc_times)

	# Check if any are greater than deadline
	for p_t in proc_times:
		if int(p_t[1]) > int(csp.deadline):
			return 0

	# If not we return 1
	return 1

# Top-level backtracking search function
def backtracking_search(csp):
	if recursive_backtracking(csp): # success
		print("\nSuccess - Solution Found:")
		csp.print_assignments()
	else:
		print("No solution could be found")

# Recursive backtracking algorithm
def recursive_backtracking(csp):
	# If the assignment is complete return
	if complete_assignment(csp):
		return 1

	# Use MRV heuristic breaking ties with degree heuristic
	var_name = select_unassigned(csp)

	# Order domain of selected value using LCV heuristic
	# Loop through each value in that domain
	for value in order_domain_values(var_name, csp):
		if is_consistent(var_name, value, csp):
			print("{} == {} is consistent, adding to assignment".format(var_name, value))
			csp.add_assignment(var_name, value)
			
			# csp.print_assignments()
			##### AC-3 iterative
			# inferences = inference(csp, variable, value) # AC-3 stuff
			# if inferences != failure:
				# add_inferences(assignment, inferences)
			#####

			# Recursive element
			result = recursive_backtracking(csp)
			if result:
				return 1
		else:
			print("{} == {} is not consistent".format(var_name, value))

		csp.remove_assignment(var_name)
		##### AC-3 iterative
		# remove_inferences(inferences, assignment)
		#####
	print("Backtracking")
	return 0

# Return queue of AC-3 arcs to initialize AC-3
# Given CSP creates arcs for all variables
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


# Revise csp given arc
def revise(csp, arc):
	revised = 0
	X_i = arc[0]
	X_j = arc[1]
	satisfy_flag = 0

	# copy just in case because we are deleting while looping
	X_i_copy = copy.deepcopy(csp.get_domain(X_i))

	# Loop through each domain value y and every x
	# If no value y can satisfy x, revise domain of x
	for x in X_i_copy:
		satisfy_flag = 0
		for y in csp.get_domain(X_j):
			if csp.get_constraint_val(X_i, X_j, x, y):
				satisfy_flag = 1
		if not satisfy_flag:
			csp.get_domain(X_i).remove(x)
			revised = 1
	return revised


# AC-3 algorithm
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

		# If we revised the csp using arc (Xi, Xj)
		# We need to add neighboring arcs to queue
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
























