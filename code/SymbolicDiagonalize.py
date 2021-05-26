"""Tried to diagonalise complicated hamiltonian for two 
ion BSB flops but didn't work
"""

import sympy 
from sympy import Matrix, symbols, pprint, simplify
import numpy as np

n = symbols('n')

matrix_list = [
    [0, sympy.sqrt(n + 1), sympy.sqrt(n + 1), 0], 
    [-sympy.sqrt(n + 1), 0, 0, sympy.sqrt(n + 2)],
    [-sympy.sqrt(n + 1), 0, 0,  sympy.sqrt(n + 2)], 
    [0,  sympy.sqrt(n + 2),  sympy.sqrt(n + 2), 0]
]

M = Matrix(matrix_list)

v = []

for n,i in enumerate(M.eigenvects()): 
    print(i)
    print('--------------------------------------')
    print(i[2][0])
    if n > 0:
        pprint(i[2][0].applyfunc(simplify))
        v.append(i[2][0])
    else: 
        v.append(i[2][0])
        v.append(i[2][1])
    print('=====================================')


w = [t.norm() for t in v]

s = (sympy.sqrt(n+1)/sympy.sqrt(n+2))*(v[2]/w[2] + v[3]/w[3]) + (sympy.sqrt(n+2)/sympy.sqrt(n+1))*v[1]/w[1]

print(s.applyfunc(simplify))

#something doesn't work