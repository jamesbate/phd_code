"""reproduces BSB two flops from thesis
"""


from lib import fit_rabi_twoions, rabi_LD_twoions
import matplotlib.pyplot as plt
import numpy as np

#prepare figure
plt.rcParams.update({'font.size': 16})
colours = ['b','m','c','r','tab:orange', 'tab:pink']
fig, axes = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))
plt.grid()

t = np.linspace(0,500,1000)
#in microseconds

params_dict = {
    'Rabi': 2*np.pi*0.15,
    'dicke_factor': 0.0413,
    'n_av': 0,
    'detuning': 0,
    'phase': 0, 
    'amplitude': 1
}

plt.plot(t, fit_rabi_twoions(t, params_dict, dn = 1, pop_state = 2), color = 'b', label = r"$P_2n_{av} = 0$")
params_dict.update({'n_av': 0.5})
plt.plot(t, fit_rabi_twoions(t, params_dict, dn = 1, pop_state = 2), color = 'g', label = r"$P_2n_{av}=0.5$")
params_dict.update({'n_av': 3})
plt.plot(t, fit_rabi_twoions(t, params_dict, dn = 1, pop_state = 2), color = 'r', label = r"$P_2n_{av}=3$")
#plt.plot(t, fit_rabi_twoions(t, params_dict, dn = -1, pop_state = 1), color = 'g', label = r"$P_1$")
#plt.plot(t, fit_rabi_twoions(t, params_dict, dn = -1, pop_state = 2), color = 'r', label = r"$P_2$")
plt.ylabel(r'$P_{\uparrow\uparrow}$')
plt.xlabel('Pulse Length (us)')
plt.title('BSB flops')
plt.legend()
plt.show()