"""Plotting population dynamics of MS gate
"""

import numpy as np 
import matplotlib.pyplot as plt 

def Phi(t, omega, delta, eta):
    return (eta/2)**2*(omega/delta)**2*(delta*t - np.sin(delta*t))

def alpha(t, omega, delta, eta):
    return (eta/2)*complex(0,1)*(omega/delta)*(1 - np.exp(complex(0,1)*delta*t))


@np.vectorize
def MS_pop(t, omega, delta, n_av,eta, pop = 0):
    #0 -> upup, 1 -> up down, 2 -> downdown
    _alpha = alpha(t, omega, delta, eta)
    _Phi = Phi(t, omega, delta, eta)
    if pop == 0:
        return (1/8)*(3 + np.exp(-4*abs(_alpha)**2*(n_av + 0.5)) - 4*np.cos(_Phi)*np.exp(-abs(_alpha)**2*(n_av + 0.5) ))
    elif pop == 1:
        return (1/4)*(1-np.exp(-4*abs(_alpha)**2*(n_av + 0.5)))
    elif pop == 2:
        return 1  - (1/8)*(3 + np.exp(-4*abs(_alpha)**2*(n_av + 0.5)) - 4*np.cos(_Phi)*np.exp(-abs(_alpha)**2*(n_av + 0.5) )) - (1/4)*(1 - np.exp(-4*abs(_alpha)**2*(n_av + 0.5)))

t = np.linspace(0,200e-6, 1000)

# n_av = 0.8
# omega = 1
# delta = 1.98

n_av = 0.000001
omega = 0.5e5
delta = 1e5
eta = 1

plt.plot(t, MS_pop(t, omega, delta, n_av,eta, pop = 0), label = 'P0')
plt.plot(t, MS_pop(t, omega, delta, n_av, eta,pop = 1), label = 'P1')
plt.plot(t, MS_pop(t, omega, delta, n_av,eta, pop = 2), label = 'P2')
plt.legend()
plt.show()