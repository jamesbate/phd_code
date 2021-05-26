"""qutip simulation of our sensing experiment. This is the function 
which enacts the experiment for a given set of parameters
"""
##---------------------PREAMBLE--------------------##
from lib import MetrologyExperimentSimulation, sense_optimal_vectors, sense_qubit_rescale, sense_echo_times, create_generators, create_initial_state, create_initial_superposition_state, create_final_state
#internal dependencies

import qutip 
import numpy as np 
import matplotlib.pyplot as plt 
from collections import OrderedDict
#packages 

##--------------------FUNCTION DEFINITION------------------## 

def experiment_simulation(signal_function_vectors, sense_signal_index, alpha_list,total_time, time_step, exp_list, diss = None, plot_list = False):

    #calculate ion number
    ion_number = signal_function_vectors.shape[1]

    nqubits_array = np.array([1]*ion_number)#hardcoded qubits for now, in principle can extend to qudits

    print('Signal vectors: \n{}'.format(signal_function_vectors))

    #find s_vec
    s = sense_optimal_vectors(signal_function_vectors)
    #scale optimal vector magnitude to fit the available qubits
    s_scaled = sense_qubit_rescale(s, nqubits_array)

    print("Optimal states: \n{}".format(s_scaled))

    (echo_times, initial_state_array) = sense_echo_times(s_scaled, nqubits_array)
    print("Echoes array: \n{}".format(echo_times))
    print("Initial State: \n{}".format(initial_state_array))
    print("Sensing signal index {}...".format(sense_signal_index))

    #pick sense signal
    initial_state_sense = initial_state_array[:,sense_signal_index]
    echo_times_sense = echo_times[:,sense_signal_index]

    initial_state = create_initial_superposition_state(initial_state_sense)

    print("Initial state vector: {}".format(initial_state))


    ##=============================##
    #Create generator (for each signal)
    generator_list = create_generators(signal_function_vectors)

    ##=============================##
    #Evolve

    #define evolution operators
    ham = sum([alpha_list[k]*generator_list[k] for k in range(ion_number)])
    
    #create simulation object 
    initial_dm = initial_state*initial_state.dag()
    mse = MetrologyExperimentSimulation(initial_dm)
    mse.add_hamiltonian(ham)

    if diss is not None:
        mse.add_dissipator(diss)
    
    mse.add_expectations(exp_list)

    echo_times_dict = {}
    for n,ech in enumerate(echo_times_sense):#convert sensing times into dict
        echo_times_dict[n] = ech*total_time#echoes are fraction of total time
    print("Total time: {}\nTimestep: {}".format(total_time, time_step))
    print("Echo times: {}".format(echo_times_dict))
    print("\nStarting simulation...\n")
    (times,results) = mse.evolve_with_echoes(echo_times_dict,total_time, time_step)
    print("\nFinished simulation")
    #plot 
    if plot_list:
        if not isinstance(plot_list, list):
            raise ValueError('plot_list should be of list type!')
        else:
            mse.plot_expectations_with_echoes(times, results, indices = plot_list)

    QFI = mse.evaluate_quantum_fischer_information(ham)
    return (mse.final_state, QFI, results)