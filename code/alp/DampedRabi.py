"""Plots Lamb Dicke revivals
"""
import numpy as np
import matplotlib.pyplot as plt
from stdlib import full_Rabi

n_av = 1
Rabi_0 = 0.934*2
dicke_factor = 0.06

t = np.linspace(670,710,10000)

plt.title('Dicke Rabi Revivals!')
plt.plot(t, full_Rabi(t, [0.07, n_av, 0, Rabi_0, 0], m = 0))
plt.show()
