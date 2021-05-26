from lib import pseudo_potential_approximation, mathieu_ode
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import odeint

##------------------------APPROXIAMTION---------------------------##

# beta = 0.4
# q = 0.8
# omega_rf = 1

# t = np.linspace(0, 20*omega_rf, 500)

# plt.plot(t, pseudo_potential_approximation(t,omega_rf, q,beta ))
# plt.show()

##-------------------------FULL ODE--------------------------##

t = np.linspace(0,100,1000)

u_0 = [1,1]
u_f = odeint(mathieu_ode, u_0,t, args = (7.5,2.5))

y_f = u_f[:,0]

plt.plot(t, y_f)

plt.show()