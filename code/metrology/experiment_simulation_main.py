"""Main file to run simulation experiments from.
"""
##---------------------------PREAMBLE-------------------------##
import qutip 
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import root
#packages 

from stdlib import PlotTemplate
from metrology.experiment_simulation import experiment_simulation
from traps.lib import ionic_oscillation_equation
from metrology.lib import create_dissipators_amplitude
#internal dependencies

##-------------------------------PARAMETERS------------------------------------##
#Taylor Generator
@np.vectorize
def taylor_generator(n):
    return lambda r: r**n

#=====================#
#find positions ions take in trap
ion_number = 3

#guess
u = np.linspace(-1,1,ion_number).T

#solve
sol = root(ionic_oscillation_equation, u)
sol.x[abs(sol.x)<1e-10] = 0
r = sol.x
r = np.round(r,3) 
#centre of expansion
r_0 = 0

print("Ion positions: {}\nOrigin: {}".format(r, r_0))

signal_functions = taylor_generator([0,1,2])

#signal functions matrix.
signal_function_vectors = np.array([f(r - r_0) for f in signal_functions]).T

#=========================#

sense_signal_index = 2#choose quadratic to sense 



#create dissipator, all same stregnth for now.. maybe make this a function like the 
#generator function?
diss_strength_array = [0.5]*ion_number
diss = create_dissipators_amplitude(diss_strength_array)

#OUTSOURCE FUNCTION FOR PHASE DECAY CHANNEL
# diss = [
#     global_diss_strength*qutip.tensor(qutip.Qobj([[0,1],[0,0]]), qutip.qeye(2), qutip.qeye(2)),
#     global_diss_strength*qutip.tensor(qutip.qeye(2), qutip.Qobj([[0,1],[0,0]]), qutip.qeye(2)),
#     global_diss_strength*qutip.tensor(qutip.qeye(2), qutip.qeye(2), qutip.Qobj([[0,1],[0,0]]))
# ]
# diss = [
#     global_diss_strength*qutip.tensor(qutip.Qobj([[1,0],[0,0]]), qutip.qeye(2), qutip.qeye(2)),
#     global_diss_strength*qutip.tensor(qutip.Qobj([[0,0],[0,1]]), qutip.qeye(2), qutip.qeye(2)),

#     global_diss_strength*qutip.tensor(qutip.qeye(2), qutip.Qobj([[1,0],[0,0]]), qutip.qeye(2)),
#     global_diss_strength*qutip.tensor(qutip.qeye(2),qutip.Qobj([[0,0],[0,1]]),  qutip.qeye(2)),

#     global_diss_strength*qutip.tensor(qutip.qeye(2), qutip.qeye(2), qutip.Qobj([[1,0],[0,0]])),
#     global_diss_strength*qutip.tensor(qutip.qeye(2), qutip.qeye(2), qutip.Qobj([[0,0],[0,1]]))
# ]

exp_list = [qutip.tensor([qutip.sigmax()]*ion_number)]

#evolve with echoes
#total_time = 1
time_step = 0.001
total_time = np.linspace(1,10,20)

#sensing strengths
alpha_list = np.array([1]*ion_number, dtype = float)
alpha_variation = np.arange(1,2,0.05)

results = []
for t in total_time:
    # results.append(experiment_simulation(signal_function_vectors, sense_signal_index, alpha_list,t, time_step, exp_list, diss))
    if t == total_time[-1]:
        results.append(experiment_simulation(signal_function_vectors, sense_signal_index, alpha_list,t, time_step, exp_list,diss, plot_list = [0]))
    else:
        results.append(experiment_simulation(signal_function_vectors, sense_signal_index, alpha_list,t, time_step, exp_list,diss))


# exp_value = []

# for a in alpha_variation:
#     t = 10
#     alpha_list[sense_signal_index] = a
#     #phi_list = t**alpha_list
#     r = experiment_simulation(signal_function_vectors, sense_signal_index, alpha_list,t, time_step, exp_list)
#     results.append(r)
#     #results.append(experiment_simulation(signal_function_vectors, sense_signal_index, phi_list,t, time_step, exp_list, diss))

#     exp_value.append(r[2][0].expect[0][-1])


pc = PlotTemplate((1,1))
ax  = pc.generate_figure()

QFI_list = [k[1] for k in results]
print(QFI_list)
ax.plot(total_time, QFI_list)
# plt.title('Expectation against signal strength')
# plt.xlabel(r'$\alpha_{sense}$')
# plt.ylabel(r'$\langle\sigma_x\otimes\sigma_x\otimes\sigma_x\rangle$')
plt.title('QFI against time with amplitude damping')
plt.xlabel('time')
plt.ylabel('QFI')
plt.show()

