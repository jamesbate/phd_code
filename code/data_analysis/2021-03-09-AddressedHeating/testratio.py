from stdlib import full_Rabi
import numpy as np
import matplotlib.pyplot as plt 

p= {'dicke_factor': 0.069, 'n_av': 1, 'detuning': 0, 'Rabi': 1.1, 'phase': 0, 'amplitude': 1}

x = np.linspace(0,200, 100)

# plt.plot(x, full_Rabi(x, p, m = 1))
# plt.plot(x, full_Rabi(x, p, m = -1))
y_r = full_Rabi(x, p, m = -1)
p['Rabi'] = 1.05
y_b  = full_Rabi(x, p, m = 1)
plt.plot(x, y_r/y_b)
plt.show()