import numpy as np 

def pseudo_potential_approximation(t, omega_rf, q, beta):
    return np.cos(0.5*beta*omega_rf*t)*(1 - 0.5*q*np.cos(omega_rf*t))

def mathieu_ode(u, t, a, q):
    return (u[1], u[0]*(2*q*np.cos(2*t) - a))