import qutip 
import matplotlib.pyplot as plt
import numpy as np

from metrology.lib import MetrologyExperimentSimulation

def create_intial_state(s_vec):
    obj_dict = {1:qutip.basis(2,0), -1:qutip.basis(2,1)}

    #create initial state
    initial_state = qutip.tensor([obj_dict[k] for k in s_vec])
    return initial_state

def create_initial_superposition_state(s_vec):
    #generate initial superposition
    initial_state = create_intial_state(s_vec)
    initial_state_flipped = create_intial_state(-1*s_vec)
    return (initial_state + initial_state_flipped)/np.sqrt(2)

total_time = 20
time_step = 0.1

ions = 6

initial_state = create_initial_superposition_state(np.array([1]*ions))

initial_dm = initial_state*initial_state.dag()

unit = [qutip.qeye(2)]*ions

ham = 0

for k in range(ions):
    unit[k] = qutip.sigmaz() 
    ham += qutip.tensor(unit)
    unit[k] = qutip.qeye(2)

exp = [qutip.tensor([qutip.sigmax()]*ions)]

mse = MetrologyExperimentSimulation(initial_dm)
mse.add_hamiltonian(ham)
mse.add_expectations(exp)

echo_times_dict = {}
for k in range(ions):
    echo_times_dict.update({k: (k+1)*total_time/(ions+1)})

(times,results) = mse.evolve_with_echoes(echo_times_dict,total_time, time_step)

mse.plot_expectations_with_echoes(times, results)
plt.show()