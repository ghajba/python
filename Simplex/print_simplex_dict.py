# simple function to print a simplex dictionary into text representation to the console

# basic: the list of basic indices, m integers
# non_basic: the list of non-basic indices, n integers
# b: m floating point numbers
# A_matrix: the A matrix, n columns m rows
# z: z0 c1 .. cn (objective coefficients (n+1 floating point numbers)) 

# def print_simplex_dict(b, A_matrix, z, basic, non_basic):
def print_simplex_dict():
    """ This method prints the simplex dictionary to the console.
        By default it uses global variables defined above to handle as the dictionary.
        However you can use the declaration of the method as above, providing every information as a method parameter.
        For large dictionaries the console output would become unreadable so it is preferred to redirect the output into a file."""
    for i in range(len(basic)):
        line_text = "x_{0} = {1:.3f}".format(basic[i],b[i])
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
            line_text = line_text + " - {0:.3f}x_{1}".format(z[i+1]*-1,non_basic[i])
        else:
            line_text = line_text + " + {0:.3f}x_{1}".format(z[i+1],non_basic[i])
    print line_text



# a sample random dictionary to have a look on the printing function
m = 3
n = 4
basic = [1,5,6]
non_basic = [3,4,2,7]
b = [4.0,5.0,0.0]
A_matrix = [[2.0,-3.0,1.0,1.0],[-1.0,3.0,-1.0,-2.0],[0.0,-1.0,1.0,3.0]]
z = [10.0,-1.0,1.0,-1.0,0.0]

print_simplex_dict()
