
# Input file description
#[Line 1] m n
#[Line 2] B1 B2 ... Bm [the list of basic indices m integers]
#[Line 3] N1 N2 ... Nn [the list of non-basic indices n integers]
#[Line 4] b1 .. bm (m floating point numbers)
#[Line 5] a11 ... a1n (first row of A matrix)
#....
#[Line m+4] am1 ... amn (mth row of A matrix)
#[Line m+5] z0 c1 .. cn (objective coefficients (n+1 floating point numbers)) 

import sys


class InvalidInputError(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Invalid input length. Expected {0} lines but got {1}".format(self.expected, self.got)

# global variables
#m = 3
#n = 4
#basic = [1,3,6]
#non_basic = [2,4,5,7]
#b = [1.0,3.0,0.0]
#A_matrix = [[0.0,0.0,-1.0,-2.0],[1.0,-1.0,0.0,-1.0],[-1.0,0.0,-2.0,0.0]]
#z = [1.0,-1.0,2.0,3.0,1.0]

n = 0
m = 0
A_matrix=[]
basic = []
non_basic = []
b = []
z = []
z_original = []
non_basic_original = []


def init(file_location):
    """ This method initializes the variables with the data from the file """
    global n, m, b, z, basic, non_basic, A_matrix
    input_data_file = open(file_location, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()

    lines = input_data.split('\n')
    if len(lines) < 6:
        raise InvalidInputError(6, len(lines))

    m = int((lines[0].split())[0])
    n = int((lines[0].split())[1])
    basic = map(int, lines[1].split())
    non_basic = map(int, lines[2].split())
    b = map(float, lines[3].split())
    A_matrix = []
    for i in range(4, m+4):
        A_matrix.append(map(float, lines[i].split()))
    z = map(float, lines[m+4].split())


def final_dictionary():
    """ Based on the objective line this method looks up if the dictionary is final or not. """
    return sum(1 for zi in z[1:] if zi > 0) == 0


def find_entering():
    """ This method looks up the entering variable using Bland's Rule: selects the variable
        with the least index if more possible entering variables exist. """
    actual = None
    for i in range(1, len(z)):
        if z[i] > 0 and (non_basic[i-1] < actual or actual is None):
            actual = non_basic[i-1]
    return actual


def find_leaving(e_idx):
    """ Based on the index of the entering variable (e_idx) this method looks up the leaving variable
        using Bland's Rule: selects the variable with the least index if more possible leaving variables exist. """
    actual = None
    bound = None
    for i in range(0, len(A_matrix)):
        if A_matrix[i][e_idx] < 0 and (-1*b[i]/A_matrix[i][e_idx] <= bound or bound is None):
            if actual is None:
                actual = basic[i]
            elif -1*b[i]/A_matrix[i][e_idx] == bound and actual > basic[i]:
                actual = basic[i]
            elif -1*b[i]/A_matrix[i][e_idx] < bound:
                actual = basic[i]
            bound = -1*b[i]/A_matrix[i][e_idx]
    return actual


def get_objective_value(e_idx, l_idx):
    """ Based on the index of the entering variable (e_idx) and on the index of the leaving variable (l_idx)
        this method calculates the objective value of the dictionary """
    return z[0]+((b[l_idx]/(-1*A_matrix[l_idx][e_idx]))*z[e_idx+1])


def recalculate_dictionary(e_idx, l_idx):
    """ Based on the index of the entering variable (e_idx) and on the index of the leaving variable (l_idx)
        this method rearranges the dictionary, making the entering variable enter, the leaving variable leave """
    global basic, non_basic, z, b, A_matrix
    
    obj_val = get_objective_value(e_idx, l_idx)
    
    # 0. secure the value of the entering variable and the objective value
    # 1. swap places: entering and leaving
    # 2. divide new line with value of entering variable
    # 3. rearrange other lines of A_matrix (except the leaving): replace the entering variable with the new line (of the leaving)
    # 4. recalculate b (except the leaving): add the b value from the new line
    # 5. recalculate z: replace entering variable with the leaving one

    # 0.
    entering_val = A_matrix[l_idx][e_idx]*-1

    # 1.
    entering = non_basic[e_idx]
    non_basic[e_idx] = basic[l_idx]
    basic[l_idx] = entering

    A_matrix[l_idx][e_idx] = -1.0  # the leaving variable has to be -1.0 as entering
    
    # 2.
    A_matrix[l_idx] = [i/entering_val for i in A_matrix[l_idx]]
    b[l_idx] /= entering_val

    # 3.
    for i in range(len(basic)):
        c_i = A_matrix[i][e_idx]
        if i != l_idx:
            b[i] += c_i*b[l_idx] # 4.
            for j in range(len(A_matrix[i])):
                if j != e_idx:
                    A_matrix[i][j] += c_i*A_matrix[l_idx][j]
                else:
                    A_matrix[i][j] = c_i*A_matrix[l_idx][j]

    # 5.
    z[0] = obj_val
    coeff = z[e_idx+1]
    for i in range(1, len(z)):
        if i != (e_idx+1):
            z[i] += (coeff*A_matrix[l_idx][i-1])
        else:
            z[i] = (coeff*A_matrix[l_idx][i-1])


def do_magic_step():
    """ This method does the magic step for the initialization phase:
        0. save the original problem, the original set of non-basic variables
        1. change all values of the objective function to 0, then append -1 for x_0
        2. add x_0 to the non-basic variables
        3. add +1 to each line of the A_matrix representing x_0
        4. recalculate the dictionary with x_0 as entering variable, 
            and the line containing the minimum value of the b vector as leaving variable"""
    global z_original, z, non_basic_original, non_basic
    z_original = list(z)
    z = [0]*len(z)
    z.append(-1)
    non_basic_original = list(non_basic)
    non_basic.append(0)
    for r in A_matrix:
        r.append(1)
    recalculate_dictionary(len(non_basic)-1, b.index(min(b)))
        
            
def initialize_simplex():
    """ This method initializes the Simplex dictionary to a possible feasible solution.
        This includes the magic step with the x_0 variable and the initial pivoting.
        The method returns "True" if the initialization succeeded, "False" if the problem is infeasible."""
    do_magic_step()
    leaving = None
    while leaving != 0 and not final_dictionary():
        entering = find_entering()
        e_idx = non_basic.index(entering)
        leaving = find_leaving(e_idx)
        if leaving is not None:
            l_idx = basic.index(leaving)
        else:
            return False
        recalculate_dictionary(e_idx, l_idx)
    return True
       
       
def rearrange_initial_feasible_dictionary():
    """ This method rearranges the initialized dictionary with the original objective value for pivoting."""
    print "Currently not implemented"
    pass
       
       
def pivot_dictionary():
    pivoting_steps = 0
    while not final_dictionary():
        entering = find_entering()
        e_idx = non_basic.index(entering)
        leaving = find_leaving(e_idx)
        if leaving is not None:
            l_idx = basic.index(leaving)
        else:
            print "UNBOUNDED"
            return -1
        recalculate_dictionary(e_idx, l_idx)
        pivoting_steps += 1
    return pivoting_steps
       
       
def solve_problem():
    """ This method solves the problem initialized from the input data """
    if sum(1 for bi in b if bi < 0) != 0:
        if not initialize_simplex() or z[0] != 0:
            print "INFEASIBLE"
            return
        rearrange_initial_feasible_dictionary()
    pivoting_steps = pivot_dictionary()    
    print "Objective Value: {0:.5f} \nPivoting Steps: {1}".format(z[0], pivoting_steps)


def print_simplex_dict():
    """ This method prints the simplex dictionary to the console.
        By default it uses global variables defined above to handle as the dictionary.
        However you can use the declaration of the method as above, providing every information as a method parameter.
        For large dictionaries the console output would become unreadable
        so it is preferred to redirect the output into a file."""
    for i in range(len(basic)):
        line_text = "x_{0} = {1:.3f}".format(basic[i], b[i])
        for j in range(len(non_basic)):
            if A_matrix[i][j] < 0:
                line_text = line_text+" - {0:.3f}x_{1}".format(A_matrix[i][j]*-1, non_basic[j])
            else:
                line_text = line_text+" + {0:.3f}x_{1}".format(A_matrix[i][j], non_basic[j])
        print line_text
    print "_______________________________________________________"
    line_text = " z  = {0:.3f}".format(z[0])
    for i in range(len(non_basic)):
        if z[i+1] < 0:
            line_text = line_text + " - {0:.3f}x_{1}".format(z[i+1]*-1, non_basic[i])
        else:
            line_text = line_text + " + {0:.3f}x_{1}".format(z[i+1], non_basic[i])
    print line_text


def write_output(objective_value):
    """ This method writes the output to a file with the name of the input file --
        adding a '.sol' at the end of the file name. """
    output = open(filename+".sol", 'w')
    output.write("{0:.5f}\n".format(objective_value))
    output.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1].strip()
        init(filename)
        solve_problem()
    else:
        print 'This test requires an input file.  Please select one from the data directory. ' \
              '(i.e. python Simplex.py ./data/part1.dict)'
