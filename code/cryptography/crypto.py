import numpy as np 
from lib import H,H_cond, marginalise, H_joint

p = np.array([[0,1/12],[1/12,0],[0,1/12],[1/12,0],[0,1/12],[1/12,0]])*2

(p_X, p_Y) = marginalise(p)
print(p_X)
print(H(p_X))
print(p_Y)
print(H(p_Y))
print([j for j in p.T])
print([H(j) for j in p.T])
print(H_cond(p))
print(H_joint(p))

