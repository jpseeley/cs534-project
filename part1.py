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
#try:
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
#except:
#	print("Graph file '{}' could not be opened for reading.".format(filepath))
#	print("Please check spelling and location of file.")
#	exit()







'''
# List of nodes - initialied to empty
nodes = []

# Global variables
count = 1
top_half = 1
glob_limit = -1
max_level = 0

# Problem Class
# Contains:
#	initial state: always 'S'
#	goal state: always 'G'
#	knowledge: data structure of graph nodes and their connections
class Problem:
	def __init__(self, initial_state='', goal_state='', knowledge=[]):
		self.initial_state = initial_state
		self.goal_state = goal_state
		self.knowledge = knowledge

	# Tests if given node is the goal state for this problem
	def simple_goal_test(self, node_name):
		if node_name == self.goal_state:
			return True
		else:
			return False

# Node Class
# Contains:
#	name: char name of node
#	distance: estimated distance to goal state for this node
#	adjacents: list of adjacent nodes and their distances (stored as tuples)
class Node:
	def __init__(self, name, distance, adjacents=[]):
		self.name = name
		self.distance = distance
		self.adjacents = adjacents

# Path Class
# Contains:
#	path: list of node names that form a path from 'S' to a node
#	heuristic: search-specific heuristic 
class Path:
	def __init__(self, path=[], heuristic=0):
		self.path = path
		self.heuristic = heuristic

# Function to print out all nodes in nodes list
def print_nodes():
	for node in nodes:
		print("{} {} {}".format(node.name, node.distance, node.adjacents))

# Function to add connection between two nodes
# Adds nodes to the node list if they are not there already
# Note: Connections are stored in ALPHABETICAL order
def add_connection(name, adjacent, path):
	no_name_new_node = 1
	no_adj_new_node = 1

	# Initialize the nodes list
	if len(nodes) == 0:
		new_node = Node(name, 0, [(adjacent, path)])
		nodes.append(new_node)
		new_node = Node(adjacent, 0, [(name, path)])
		nodes.append(new_node)
	else:
		for node in nodes: 
			# If first node exists in list
			# Add adjacent to the class list
			if node.name == name:
				index = 0
				replacement_index = len(node.adjacents)
				for adj_node in node.adjacents:
					if adj_node[0] < adjacent:
						replacement_index = index
						break
					index += 1
				node.adjacents.insert(replacement_index, (adjacent, path))
				no_name_new_node = 0
			else:
				# create new node with distance 0 as placeholder
				new_name_node = Node(name, 0, [(adjacent, path)])
			# Need to also look for adjacent node so each node knows its connections
			if node.name == adjacent:
				index = 0
				replacement_index = len(node.adjacents)
				for adj_node in node.adjacents:
					if adj_node[0] < name:
						replacement_index = index
						break
					index += 1
				node.adjacents.insert(replacement_index, (name, path))
				no_adj_new_node = 0
			else:
				# create new node with distance 0 as placeholder
				new_adj_node = Node(adjacent, 0, [(name, path)])
		if no_adj_new_node:
			nodes.append(new_adj_node)
		if no_name_new_node:
			nodes.append(new_name_node)

# Function to add distance value to Node objects in nodes list
def add_distance(name, distance):
	for node in nodes:
		# Adjust distance for a Node object with given name
		# G won't be updated but by default is 0
		if node.name == name:
			node.distance = float(distance)

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
			if not line_info:
				break

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

			# Read next line
			line = fp.readline()
			count += 1 # count is for debugging and printing 

	fp.close()
except:
	print("Graph file '{}' could not be opened for reading.".format(filepath))
	print("Please check spelling and location of file.")
	exit()

## Graph Created, now we move on to actual searching

# establish problem as search from 'S' to 'G' using knowledge from nodes list
problem = Problem('S', 'G', nodes)

# Function that returns distance estimate for given node name
def get_node_h(node_name):
	for node in nodes:
		if node.name == node_name:
			return node.distance

# Printing out entire nodes data structure for debugging
# print_nodes()
 
# Function that returns the cost between two nodes
def get_node_dist(node_name_from, node_name_to):
	for node in nodes:
		if node.name == node_name_from:
			for adj in node.adjacents:
				if adj[0] == node_name_to:
					return adj[1]

# Function that expands parent node using given node_list knowledge
def expand_node(parent, node_list):
	children = []
	for node in node_list:
		if node.name == parent:
			for child in node.adjacents:
				children.append(child[0]) # get name of child add to child list
	return children

# Checks if given node list is an end node
# Ie. When we expand an end node, it has no children and
# the opened nodes is an empty list
def is_end_node(opened_nodes):
	if not opened_nodes:
		return True
	else:
		return False

# Function to check if given node name is in given list of nodes
#def has_not_visited(child_name, node_name_history):
#	if child_name not in node_name_history:
#		return True
#	else:
#		return False


# Prints queue according to HW1 specifications
# Has special checks for certain search methods, which require 
# extra printing functionality like iterative-deepening, which needs
# to print out the current search level
def compact_queue_print(node_name, counter, queue, search_method):
	global glob_limit
	if search_method == "uniform-cost" or search_method == "greedy" or search_method == "a-star" or search_method == "hill-climbing" or search_method == "beam":
		include_heuristic = 1
	else:
		include_heuristic = 0
	if counter == 0:
		sys.stdout.write("   Expanded		Queue\n")
	if queue[0].path == ['S'] and search_method == "iterative-deepening":
		sys.stdout.write("L={}	{}		[".format(glob_limit+2, node_name))
	else:
		sys.stdout.write("	{}		[".format(node_name))
	space_counter = 0
	for a_path in queue:
		path_str = ",".join(a_path.path)
		if include_heuristic:
			sys.stdout.write("{}<{}>".format(a_path.heuristic, path_str))
		else:
			sys.stdout.write("<{}>".format(path_str))
		if space_counter < (len(queue) - 1):
			sys.stdout.write(" ")
		space_counter += 1
	print("]")


#### The Following 9 functions are used in each search method ####
# They all have on purpose and that is to take the children of an expanded node and put
# them into the queue according to their search method. Children are referred to as 
# "opened_nodes" in these functions. Some methods must edit the queue, like hill-climbing, 
# A*, etc. But they only work on the queue as described in the textbook and in class.
####

# Function to handle depth-first search queue method
# Takes the children and just puts them at the from of the queue
# Notice that the homework required the queue to be the same for each method
# So the heuristic value is NOT used, but to satisfy Python requirement we use 
# a dummy "zero".
def depth_first_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	# If we hit an end node, we just remove it from queue and return
	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]
		for child_name in opened_nodes:
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_q0 = Path(new_path, 0) 
				queue.insert(0, new_q0)

# Function to handle breadth-first search
# Takes children and puts their paths at end of queue
def breadth_first_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		# Notice here that we reverse the list of children,
		# That is because we are putting them at the end of the queue
		# So this way alphabetical order is maintained
		# We know this because we store the children in our data structure in 
		# alphabetical, so don't have to do extra alphabetical sorting in
		# our methods
		copy_opened_nodes = opened_nodes[::-1]
		for child_name in copy_opened_nodes:
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_q0 = Path(new_path, 0)
				queue.append(new_q0)


# Function to handle depth-limited search 
# Same as depth-first search except we only go down to level 2
# This is synonymous with paths of length 3
def depth_limited_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic
	nodes_added = 0 # used to track if we changed queue
	old_queue_length = len(queue) # track old queue length

	if is_end_node(opened_nodes):
		del queue[0]
		nodes_added += 1
	else:
		del queue[0]

		for child_name in opened_nodes:
			if child_name not in curr_path and len(curr_path) < (limit + 2):
				new_path = [child_name] + curr_path
				new_q0 = Path(new_path, 0)
				queue.insert(0, new_q0)
				nodes_added += 1

		# Check to see if we have reached the limit
		if old_queue_length != len(queue):
			nodes_added += 1
		if nodes_added == 0 or not queue:
			return []

# Function to perorm iterative deepening
# Essentially this is just repeated depth-limited
# We adjust the limit by 1 if no solution is found
# We also exit if the our limit becomes greater than the length of any paths in the queue
# This ensures that we will go up to level = infinity, if no solution exists
def iterative_deepening_queue_method(opened_nodes, queue, counter, limit):
	global glob_limit
	global max_level

	depth_limited_queue_method(opened_nodes, queue, counter, glob_limit)

	# Track the max level in queue
	for a_path in queue:
		if len(a_path.path) > max_level:
			max_level = len(a_path.path)

	# When the queue is empty that means we hit an end node for our level
	# ie. There are no more paths to explore, so we increase the limit by 1,
	# set the queue back to the initial state and try again
	if not queue:
		# Check to avoid infinite attempts
		if max_level < glob_limit+2 and max_level != 0:
			return []
		glob_limit += 1
		print("")
		queue.append(Path([problem.initial_state],0))
		max_level = 0

# Funciton to perform uniform queue method
# Uses g(n), the distance from initial state to goal state
# Chooses node with lowest g(n)
def uniform_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		for child_name in opened_nodes:
			insert_counter = 0
			insert_found = 0
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_heur = float(curr_heur) + float(get_node_dist(curr_path[0], child_name))
				new_q0 = Path(new_path, new_heur) # Path to place into queue

				# need to place paths in queue with least as first
				for a_path in queue:
					t_path = a_path
					if float(a_path.heuristic) > float(new_heur):
						insert_found = 1
					if not insert_found:
						insert_counter += 1

				if not insert_found:
					queue.append(new_q0)
				else:
					queue.insert(insert_counter, new_q0)

		# edge case where we have the same value for different paths
		# Paths will automatically be in alphabetical order, but when we 
		# have a path of same cost and same end node, we are required to
		# put the path with the lowest length first
		check_queue = 1 
		while check_queue:
			check_queue = 0
			if len(queue) > 1:
				queue_copy = queue
				for a_path in queue_copy[:-1]:
					curr_index = queue.index(a_path)
					next_index = curr_index + 1
					if a_path.heuristic == queue[next_index].heuristic:
						# We have a side by side same valued heuristic
						# Only change if their end node is the same
						if a_path.path[0] == queue[next_index].path[0]:
							# Two conditions, either the current one is longer and we swap
							# or the second one is longer/same and we do nothing
							if len(a_path.path) > len(queue[next_index].path):
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
						else:
							if a_path.path[0] > queue[next_index].path[0]:
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
			else:
				check_queue = 0


# Function to perform greedy queue
# Uses h(n), the estimated distance to the goal
# Chooses node based solely on that
def greedy_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		for child_name in opened_nodes:
			insert_counter = 0
			insert_found = 0
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_heur = get_node_h(child_name)
				new_q0 = Path(new_path, new_heur) # Path to place into queue

				for a_path in queue:
					t_path = a_path
					if float(a_path.heuristic) >= float(new_heur):
						insert_found = 1
					if not insert_found:
						insert_counter += 1

				if not insert_found:
					queue.append(new_q0)
				else:
					queue.insert(insert_counter, new_q0)

		# edge case where we have the same value for different paths
		# Paths will automatically be in alphabetical order, but when we 
		# have a path of same cost and same end node, we are required to
		# put the path with the lowest length first
		check_queue = 1 
		while check_queue:
			check_queue = 0
			if len(queue) > 1:
				queue_copy = queue
				for a_path in queue_copy[:-1]:
					curr_index = queue.index(a_path)
					next_index = curr_index + 1
					if a_path.heuristic == queue[next_index].heuristic:
						# We have a side by side same valued heuristic
						# Only change if their end node is the same
						if a_path.path[0] == queue[next_index].path[0]:
							# Two conditions, either the current one is longer and we swap
							# or the second one is longer/same and we do nothing
							if len(a_path.path) > len(queue[next_index].path):
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
						else:
							if a_path.path[0] > queue[next_index].path[0]:
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
			else:
				check_queue = 0

# Function to perform A* queue
# Uses function f(n) = h(n) + g(n)
# Note that we only track 1 heuristic for our Path class, we do need 
# to subtract out the parent node's heuristic value to get the true f(n)
def a_star_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		for child_name in opened_nodes:
			insert_counter = 0
			insert_found = 0
			duplicate_child = 0

			new_path = [child_name] + curr_path
			new_heur = float(curr_heur) + float(get_node_dist(curr_path[0], child_name)) + float(get_node_h(child_name)) - float(get_node_h(curr_path[0]))
			new_q0 = Path(new_path, new_heur) # Path to place into queue

			# Here we handle the possibility of a duplicate end node
			# and we delete the lesser node. There is at most 2 duplicate 
			# nodes in the queue, because we check for duplicates every iteration
			# Ex: We are adding a path that ends with K and has cost 26 and
			# the queue has a path that ends with K and has cost 75. We delete
			# the path in the queue and add our new lower cost path in.
			greater_index = -1
			for a_path in queue:
				if child_name == a_path.path[0]:
					duplicate_child += 1
					if a_path.heuristic > new_heur:
						duplicate_child -= 1
						greater_index = queue.index(a_path)

			if greater_index != -1:
				del queue[greater_index]

			if child_name not in curr_path and not duplicate_child:
				for a_path in queue:
					t_path = a_path
					if float(a_path.heuristic) > float(new_heur):
						insert_found = 1
					if not insert_found:
						insert_counter += 1

				if not insert_found:
					queue.append(new_q0)
				else:
					queue.insert(insert_counter, new_q0)

# Function to perform hill-climbing queue
# Uses h(n), but only keeps one path in the queue
def hill_climbing_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		for child_name in opened_nodes:
			insert_counter = 0
			insert_found = 0
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_heur = get_node_h(child_name)
				new_q0 = Path(new_path, new_heur) # Path to place into queue

				for a_path in queue:
					t_path = a_path
					if float(a_path.heuristic) >= float(new_heur):
						insert_found = 1
					if not insert_found:
						insert_counter += 1

				if not insert_found:
					queue.append(new_q0)
				else:
					queue.insert(insert_counter, new_q0)
	
		# edge case where we have the same value for different paths
		# Paths will automatically be in alphabetical order, but when we 
		# have a path of same cost and same end node, we are required to
		# put the path with the lowest length first
		check_queue = 1 
		while check_queue:
			check_queue = 0
			if len(queue) > 1:
				queue_copy = queue
				for a_path in queue_copy[:-1]:
					curr_index = queue.index(a_path)
					next_index = curr_index + 1
					if a_path.heuristic == queue[next_index].heuristic:
						# We have a side by side same valued heuristic
						# Only change if their end node is the same
						if a_path.path[0] == queue[next_index].path[0]:
							# Two conditions, either the current one is longer and we swap
							# or the second one is longer/same and we do nothing
							if len(a_path.path) > len(queue[next_index].path):
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
						else:
							if a_path.path[0] > queue[next_index].path[0]:
								temp_path = a_path
								queue[curr_index] = queue[next_index]
								queue[next_index] = temp_path
								check_queue += 1
			else:
				check_queue = 0			
	
		# We need to delete all but the best option
		delete_counter = 0
		for a_path in queue:
			#print(delete_counter)
			if delete_counter > 0:
				del queue[delete_counter]
			delete_counter += 1

# Function to perform beam queue method
# Same as breadth first method, but only keeps best 2 paths on level change
def beam_queue_method(opened_nodes, queue, counter, limit):
	curr_q0 = queue[0] # This is a Path Object
	curr_path = curr_q0.path
	curr_heur = curr_q0.heuristic

	# The current level is the length of the current path
	# This is true in BFS, not in other methods
	curr_level = len(queue[0].path)
	
	if is_end_node(opened_nodes):
		del queue[0]
	else:
		del queue[0]

		# Again, like in the BFS method, we reverse the list to maintain
		# alphabetical order
		copy_opened_nodes = opened_nodes[::-1]
		for child_name in copy_opened_nodes:
			if child_name not in curr_path:
				new_path = [child_name] + curr_path
				new_heur = get_node_h(child_name)
				new_q0 = Path(new_path, new_heur)
				queue.append(new_q0)

		if not queue:
			return []

		# On a new level, we have to trim the queue down to 2 paths
		if len(queue[0].path) > curr_level:
			# Build list of the heuristic values in queue
			heur_list = []
			for a_path in queue:
				heur_list.append(a_path.heuristic)

			# Sort list in ascending order to find the minimum values
			sort_heur_list = sorted(heur_list, reverse=False)

			# Create list of size 1 or 2 that contains minimum values to keep 
			min_list = []
			if len(sort_heur_list) > 2:
				min_list_counter = 0
				for val in sort_heur_list:
					if min_list_counter < 2:
						min_list.append(val)
					min_list_counter += 1
			else:
				min_list = sort_heur_list

			# Remove values in queue that are not mimimum values
			reverse_queue = queue[::-1]
			removal_index = len(queue) - 1
			for a_path in reverse_queue:
				if a_path.heuristic not in min_list:
					del queue[removal_index]
				removal_index -= 1

# Function set heuristic for a node name
def heuristic(node_name, search_method):
	if search_method == "uniform-cost":
		return 0
	else:
		return get_node_h(node_name)

# Neatly decides which queue method to use (8 total)
# Python interpretation of a C/C++ switch statement
def handle_queue(search_method, node_name, queue, counter, limit):
	result = {
		"depth-first": depth_first_queue_method,
		"breadth-first": breadth_first_queue_method,
		"depth-limited": depth_limited_queue_method,
		"iterative-deepening": iterative_deepening_queue_method,
		"uniform-cost": uniform_queue_method,
		"greedy": greedy_queue_method,
		"a-star": a_star_queue_method,
		"hill-climbing": hill_climbing_queue_method,
		"beam": beam_queue_method
	}
	return result.get(search_method)(node_name, queue, counter, limit)

#### General Search Method ####
# problem: Problem object
# search-method: String specifying search
# 
# returns: Path solution as a list
def General_Search(problem, search_method):
	# Initialize queue to initial state
	queue = [Path([problem.initial_state], heuristic(problem.initial_state, search_method))]
	counter = 0 # Used only for printing
	while 1: 
		# If the queue is empty, then either an initial state couldn't be created or
		# our search method exhausted all possible paths and can go no further
		if not queue:
			if counter > 0:
				print("   A solution could not be found.")
			else:
				print("   An initial state could not be established.")
			return []
		else:
			# Remove front of queue
			node_name = queue[0].path[0]

			# Print out current queue for user
			compact_queue_print(node_name, counter, queue, search_method)

			# Check for goal state
			if problem.simple_goal_test(node_name):
				print("   goal reached!")
				return queue[0].path

			# Open children nodes
			opened_nodes = expand_node(node_name, problem.knowledge)

			# Call queue function which decides how to handle the queue based on the 
			# search method
			handle_queue(search_method, opened_nodes, queue, counter, 1)

			# Increment counter, again, for printing only
			counter += 1 

#### The following are the top-level functions for each search method ####

def Depth_1st_Search(graph_problem):
	print("Depth 1st Search")
	return General_Search(graph_problem, "depth-first")

def Breadth_1st_Search(graph_problem):
	print("Breath 1st Search")
	return General_Search(graph_problem, "breadth-first")

def Depth_Limited_Search(graph_problem):
	print("Depth Limited Search (Limit = 2)")
	return General_Search(graph_problem, "depth-limited")

def Iterative_Deepening_Search(graph_problem):
	print("Iterative Deepening Search (Step = 1)")
	return General_Search(graph_problem, "iterative-deepening")

def Uniform_Cost_Search(graph_problem):
	print("Uniform Cost Search")
	return General_Search(graph_problem, "uniform-cost")

def Greedy_Search(graph_problem):
	print("Greedy Search")
	return General_Search(graph_problem, "greedy")

def A_Star_Search(graph_problem):
	print("A* Search")
	return General_Search(graph_problem, "a-star")

def Hill_Climbing_Search(graph_problem):
	print("Hill Climbing Search")
	return General_Search(graph_problem, "hill-climbing")

def Beam_Search(graph_problem):
	print("Beam Search (w = 2)")
	return General_Search(graph_problem, "beam")

# Calls all search methods, note that the path solution is returned via 
# the general search function as specified in HW1, but the printout does not
# print out the final solution as specified in HW1. This function saves all the final
# results to variables r1-r9 and could be expanded to print all results compactly. 
def All_Search(graph_problem):
	r1 = Depth_1st_Search(graph_problem)
	print("")
	r2 = Breadth_1st_Search(graph_problem)
	print("")
	r3 = Depth_Limited_Search(graph_problem)
	print("")
	r4 = Iterative_Deepening_Search(graph_problem)
	print("")
	r5 = Uniform_Cost_Search(graph_problem)
	print("")
	r6 = Greedy_Search(graph_problem)
	print("")
	r7 = A_Star_Search(graph_problem)
	print("")
	r8 = Hill_Climbing_Search(graph_problem)
	print("")
	r9 = Beam_Search(graph_problem)

# The function call, which prints out all search methods
All_Search(problem)
'''

