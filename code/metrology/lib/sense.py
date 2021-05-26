"""This file contains functions useful for quantum sensing
"""
##----------------------------PREAMBLE----------------------------------##
import numpy as np
from stdlib import sub_gram_schmidt, gram_schmidt_columns
import qutip

##------------------------FUCNTION DEFINITIONS------------------------------##

def sense_echo_times(s_scaled_array, nqubits_array):
    """calculate when to flip states given s array
    """
    #return fraction of sensing time
    echoes_array = np.empty(s_scaled_array.shape)
    initial_state_array = -1*np.ones(s_scaled_array.shape)

    i = 0
    for s_scaled, initial_state in zip(s_scaled_array.T, initial_state_array.T):
        echoes = echoes_array.T[i]
        echoes = 0.5*(1 - s_scaled/nqubits_array)
        for n in range(s_scaled.size):
            if echoes[n] > 0.5:
                echoes[n] = 1 - echoes[n]
                initial_state[n] = 1
            if abs(echoes[n]) < 10**-10:
                echoes[n] = 0
        echoes_array.T[i] = echoes
        i+=1
    return (echoes_array, initial_state_array)


def sense_optimal_vectors(x):
    """calculates s_opt using gram schmidt
    """
    if x.shape[0] < x.shape[1]:
        raise ValueError('Not enough sensors!')
    opt_vectors = np.zeros(x.shape)
    for i in range(x.shape[1]):
        opt_vectors[:,i, np.newaxis] = sub_gram_schmidt(x[:,i, np.newaxis], np.delete(x,i,axis = 1))
    return opt_vectors


def sense_qubit_rescale(s, nqubits_array):
    """works out how to scale spin normalisation
    """
    s_max = np.amax(abs(s),axis=0)
    s_scaled = (s/s_max)*nqubits_array[:,np.newaxis]
    return s_scaled

def fisher_information(f_kj, s1, s2):
    #note, this is f_kj, i.e. columns are positions, rows are signals (opposite to what I make)
    #f_kj*s_jl
    r =  (f_kj.dot(s2 - s1))**2
    r[r<1e-10] = 0
    return r

def create_generators(signal_function_vectors):
    n_sensors = len(signal_function_vectors[:,0])
    n_signals = len(signal_function_vectors[0])

    unit_list = [qutip.qeye(2) for j in range(n_sensors)]

    generator_list = []

    for k in range(n_signals):
        G = 0
        for j in range(n_sensors):
            unit_list[j] = qutip.sigmaz()
            G += signal_function_vectors[j,k]*qutip.tensor(unit_list)
            unit_list[j] = qutip.qeye(2)#revert back
        generator_list.append(G)
    
    return generator_list

def create_dissipators_amplitude(strength_list):
    ion_number = len(strength_list)

    unit_list = [qutip.qeye(2) for k in range(ion_number)]
    diss = []
    for k in range(ion_number):
        unit_list[k] = qutip.Qobj([[0,1],[0,0]])
        diss.append(strength_list[k]*qutip.tensor(unit_list))
        unit_list[k] = qutip.qeye(2)
    
    return diss


def create_initial_state(s_vec):
    #converts vector to state
    obj_dict = {1:qutip.basis(2,0), -1:qutip.basis(2,1)}

    #create initial state
    initial_state = qutip.tensor([obj_dict[k] for k in s_vec])
    return initial_state

def create_initial_superposition_state(s_vec):
    #generate initial GHZ superposition from vector
    initial_state = create_initial_state(s_vec)
    initial_state_flipped = create_initial_state(-1*s_vec)
    return (initial_state + initial_state_flipped)/np.sqrt(2)

def create_final_state(s_vec, phase_sense):#for testing, add phase manually
    initial_state = create_initial_state(s_vec)
    initial_state_flipped = create_initial_state(-1*s_vec)
    return (np.exp(-complex(0,1)*phase_sense)*initial_state + np.exp(complex(0,1)*phase_sense)*initial_state_flipped)/np.sqrt(2)
