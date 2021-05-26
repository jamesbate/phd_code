from lib import fit_rabi_twoions, rabi_LD_twoions
import matplotlib.pyplot as plt
import numpy as np
from lib import rabi_flops_LD_blue, rabi_flops_LD_red, rabi_flops_LD_carrier

#prepare figure
plt.rcParams.update({'font.size': 16})
colours = ['b','m','c','r','tab:orange', 'tab:pink']
fig, axes = plt.subplots(1	,2, constrained_layout=True, figsize=(18, 9))
plt.grid()

t = np.linspace(0,1000,1000)
#in microseconds

#Now let out pi time be 30us (i.e. how well you can identify the carrier)
Rabi = 5*np.pi/50
#Rabi now in MHz

#corresponds to axial frequency of 1MHz
eta = 0.068

n_av = 20

params_dict = {
    'Rabi': Rabi,
    'dicke_factor': 0.068,
    'n_av': 20,
    'detuning': 0,
    'phase': 0, 
    'amplitude': 1
}

#These are the plots in the lambe dicke regime (up to 2nd order)
# axes[0].plot(t, rabi_flops_LD_blue(t, Rabi, eta, n_av), ':', c = colours[0])
# axes[0].plot(t, rabi_flops_LD_red(t, Rabi, eta, n_av), ':', c = colours[1])
# axes[0].plot(t, rabi_flops_LD_carrier(t, Rabi, eta, n_av), ':', c = colours[2])

#This is the full solution
axes[0].plot(fit_rabi_twoions(t, params_dict , dn = 1, pop_state = 0), c = colours[0], label = "BSB")
axes[0].plot(fit_rabi_twoions(t, params_dict , dn = 1, pop_state = 1), c = colours[0], label = "BSB")
axes[0].plot(fit_rabi_twoions(t, params_dict , dn = 1, pop_state = 2), c = colours[0], label = "BSB")
#axes[0].plot(fit_rabi_twoions(t, params_dict , m = 0), c = colours[2], label = "Carrier")
axes[0].plot(fit_rabi_twoions(t, params_dict , dn = -1, pop_state = 0), c = colours[1], label = "RSB")

axes[0].set_title("$n_{av} = 20$")

n_av = 0.5
params_dict.update({'n_av': 0.5})

#These are the plots in the lambe dicke regime (up to 2nd order)
# axes[1].plot(t, rabi_flops_LD_blue(t, Rabi, eta, n_av), ':', c = colours[0])
# axes[1].plot(t, rabi_flops_LD_red(t, Rabi, eta, n_av), ':', c = colours[1])
# axes[1].plot(t, rabi_flops_LD_carrier(t, Rabi, eta, n_av), ':', c = colours[2])

#This is the full solution
axes[1].plot(fit_rabi_twoions(t, params_dict , dn = 1, pop_state = 0), c = colours[0], label = "BSB")
#axes[1].plot(fit_rabi_twoions(t, params_dict , m = 0), c = colours[2], label = "Carrier")
axes[1].plot(fit_rabi_twoions(t, params_dict, dn = -1, pop_state = 0), c = colours[1], label = "RSB")

axes[1].set_title("$n_{av} = 0.5$")

plt.legend()
#plt.savefig('C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/dickevsfabiflops.png', dpi = 1000)
plt.show()
