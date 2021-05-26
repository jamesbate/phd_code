from scipy.optimize import root 
import numpy as np 
from numpy.linalg import eig 
from stdlib import PhysicalConstants

ion_number = 5
pc = PhysicalConstants()
u = np.linspace(-1,1,ion_number).T

def length_scale(frequency, nucleon_number = 40):
    #returned in micrometers
    return 1e6*((pc.q_e)**2/(4*np.pi*pc.epsilon_0*(2*np.pi*frequency)**2*nucleon_number*pc.m_p))**(1/3)

def ionic_oscillation_equation(u):
    N = u.size 
    r = np.empty((N,),dtype = float)
    for i in range(N):
        r[i] = u[i]
        for j in range(N):
            if j < i: 
                r[i] -= 1/(u[i] - u[j])**2 
            if j > i: 
                r[i] += 1/(u[i] - u[j])**2 
    return r 

sol = root(ionic_oscillation_equation, u)

def A_matrix(u):
    N = u.size
    A = np.empty((N,N), dtype = float)
    for i in range(N):
        for j in range(N):
            if i == j: 
                A[i,j] = 1 
                for k in range(N):
                    if k != j:
                        A[i,j] += 2/abs(u[i] - u[k])**3
            else:
                A[i,j] = -2/abs(u[i] - u[j])**3
    #zero threshold
    return A

A = A_matrix(sol.x)

evals, evecs = eig(A)



def s_matrix(evecs, evals):
    N = evals.size
    s = np.empty(evecs.shape, dtype = float)
    for m,(col,val) in enumerate(zip(evecs.T, evals)):
        s[:,m] = np.sqrt(N)*col.T/val**0.25
    return s 

if __name__ == "__main.py":
    print(sol.x)
    print(A)
    print(evals)
    print(evecs)
    print(s_matrix(evecs, evals))