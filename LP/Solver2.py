# This little solver works on LPs of the form
# maximize cx
# subject to: Ax <= b

from sympy import *

def solve(A, b, c, B, verbose):
        '''requires a feasible basis B for the LP'''
        m, n = A.rows, A.cols
        itr = 0
    
        # find vertex corresponding to feasible basis B
        AB = A.extract(B, range(n))
        bB = b.extract(B, [0])
        x = AB.LUsolve(bB)

        ABi = AB.inv()

        while True:
                itr += 1

                # compute lambda
                l = (c.T * ABi).T

                # check for optimality
                if all(e >= 0 for e in l):
                        return x, itr

                # find leaving index B[r]
                r = min(i for i in range(l.rows) if l[i] < 0)

                # compute direction to move int
                d = -ABi[:, r]

                # determine the set K
                K = [i for i in range(m) if (A[i, :] * d)[0] > 0]

                if not K:
                        return 'unbounded', itr

                # find entering index e
                e, v = None, None
                for k in K:
                        w = (b[k] - (A[k, :] * x)[0]) / ((A[k, :] * d)[0])
                        if v is None or w < v:
                                v = w
                                e = k

                # update basis
                B[r] = e
                AB[r, :] = A[e, :]
                bB[r, :] = b[e, :]

                # update inverse
                ABi = AB.inv()

                # move to the new vertex
                x = x + v*d

def simplex(A, b, c, B, verbose=False):
        x, itr = solve(A, b, c, B, verbose)

        if x == 'infeasible':
                print 'LP is infeasible'
        elif x == 'unbounded':
                print 'LP is unbounded'
        else:
                print 'Vertex', x.T, 'is optimal'
                print 'Optimal value is', (c.T * x)[0]
                print 'Found after', itr, 'simplex iterations'

if __name__ == '__main__':
    # example
    A = Matrix([[1, 0, 0, 0],
                [20, 1, 0, 0],
                [200, 20, 1, 0],
                [2000, 200, 20, 1],
                [-1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, -1]])
    b = Matrix([1,100,10000,1000000, 0,0,0,0])
    c = Matrix([1000, 100, 10, 1])
    B = range(4, 8)

    simplex(A, b, c, B, verbose=True)
