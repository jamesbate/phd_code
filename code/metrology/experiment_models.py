import qutip as qt
import numpy as np

s_vec = np.array([1,1,1])
phase_sense = np.pi/4
measurement_phase = 0
n_measurements = 100

def create_intial_state(s_vec):
    obj_dict = {1:qt.basis(2,0), -1:qt.basis(2,1)}

    #create initial state
    initial_state = qt.tensor([obj_dict[k] for k in s_vec])
    return initial_state


def create_final_state(s_vec, phase_sense):

    #generate initial superposition
    initial_state = create_intial_state(s_vec)
    initial_state_flipped = create_intial_state(-1*s_vec)

    #generate phase
    final_state = (np.exp(-complex(0,1)*phase_sense)*initial_state + np.exp(complex(0,1)*phase_sense)*initial_state_flipped)/np.sqrt(2)

    return final_state 

def create_measurement_bases(s_vec, phase_measure):

    initial_state = create_intial_state(s_vec)
    initial_state_flipped = create_intial_state(-1*s_vec)

    #measurement state
    measure_state_1 = (np.exp(-complex(0,1)*phase_measure)*initial_state + np.exp(complex(0,1)*phase_measure)*initial_state_flipped)/np.sqrt(2)
    measure_state_2 = (np.exp(-complex(0,1)*phase_measure)*initial_state - np.exp(complex(0,1)*phase_measure)*initial_state_flipped)/np.sqrt(2)

    return (measure_state_1, measure_state_2)

def get_measurement_probabilities(s_vec, measurement_phase, state):

    #create measure states
    (measure_state_1, measure_state_2) = create_measurement_bases(s_vec, measurement_phase)
    return (abs(state.overlap(measure_state_1))**2, abs(state.overlap(measure_state_2))**2)



state = create_final_state(s_vec, phase_sense)
print(get_measurement_probabilities(s_vec, measurement_phase, state))