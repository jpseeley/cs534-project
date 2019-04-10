import copy
from data_objects import Constraint_Matrix, CSP, Variable

# Return difference between two lists
def list_diff(list_1, list_2):
    return list(set(list_1).symmetric_difference(set(list_2)))

def get_constrain_problem(filepath):
    file_section_count = 0
    variable_list = []
    var_name_list = []
    domain_list = []
    constraint_list = []

    # Loop to read graph data from .txt file and to store it in our CSP
    # Uses file_section_count to determine how to parse file data
    with open(filepath) as fp:
        line = fp.readline() # read first line
        while line:
            line_info = line.split() # parse line by spaces

            # increment file section counter for each ##### seen
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
                    domain_list.append(line_info[0])
                elif file_section_count == 3: # deadline constraint
                    deadline = line_info[0]
                    # take the time to create a constraint matrix for all N constraints
                    # in total N choose 2 are created
                    for variable in variable_list:
                        adj_list = copy.deepcopy(var_name_list)
                        adj_list.remove(variable.name)
                        # print(adj_list)
                        # print(variable.name)
                        # print(var_name_list)
                        for var in adj_list:
                            copy_c_list = copy.deepcopy(constraint_list)
                            already_inside = 0
                            for constraint in copy_c_list:
                                if constraint.m1 == var or constraint.m1 == var:
                                    already_inside = 1
                            if not already_inside:
                                constraint_list.append(Constraint_Matrix(variable.name, var, variable.domain, len(variable.domain)))
                elif file_section_count == 4: # unary inclusive
                    complement_set = list_diff(line_info[1:len(line_info)], domain_list)
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
            # Read next line
            line = fp.readline()
            #file_line_count += 1 # count is for debugging
    fp.close()

    # Clean up all unspecified matrices values
    for constraint in constraint_list:
        constraint.cleanup()
    
    return CSP(variable_list, domain_list, constraint_list, deadline)