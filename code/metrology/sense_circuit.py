##-------------------------------PREAMBLE------------------------------------##
from qutip import Qobj, ghz_state, sigmax, tensor, qeye, tensor_contract
from lib import sense_optimal_vectors, sense_echo_times, sense_qubit_rescale, fisher_information
import numpy as np

from traps.lib import ionic_oscillation_equation, length_scale
from scipy.optimize import root
##-------------------------------PARAMETERS------------------------------------##
#Taylor Generator
@np.vectorize
def taylor_generator(n):
    return lambda r: r**n

#positions, take ion postition in paul trap in dimensionless units
#r = np.array([-2.12,-1,0,1,2.12])
#r = np.array([-2,-1,0,1,2])
ion_number = 3
u = np.linspace(-1,1,ion_number).T
sol = root(ionic_oscillation_equation, u)
sol.x[abs(sol.x)<1e-10] = 0
r = sol.x
r = np.round(r,3) 
r_0 = 0

signal_functions = taylor_generator([0,1,2])

##------------------------CLASSICAL CALCULATIONS-----------------------------##

print('Dimesionless Ion Positions:\t', r)
print('Absolute Positions:\t', length_scale(869e3)*r, 'um')

#array of how many qubits we have
nqubits_array = np.array([1]*r.size)

#noise signal functions matrix.
signal_function_vectors = np.array([f(r - r_0) for f in signal_functions]).T
nsignals = signal_functions.shape[0]
npositions = r.size
ndimensions_free = npositions - nsignals 
#this is redundant now 

print('f_jk: \n{}\n'.format(np.round(signal_function_vectors,2)))

#find optimal s vectors for each signal function
#Note, each column vector in the matrix is the optimal s if the signal
#is the corresponding column, and the rest is noise.
s = sense_optimal_vectors(signal_function_vectors)
#Corresponds to Ben's A vector.


#scale optimal vector magnitude to fit the available qubits
s_scaled = sense_qubit_rescale(s, nqubits_array)
print('\ns_scaled:\n',np.round(s_scaled,3))
print('\nQFI:\n', np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled),4))

#Given the s vectors, figure out what spin echo times are required to
#achieve this effect spin value
(echo_times, initial_state_array) = sense_echo_times(s_scaled, nqubits_array)
print('\ninitial state vector:\n',initial_state_array)
print('\nspin echo times:\n',echo_times)

##------------------------QUANTUM STATE PREPARATION---------------------------##

#Prepare GHZ state. Again, each column is the state when the corresponding
#column of the fucntion array is a signal
psi_initial = ghz_state(r.size)
psi_initial_array = np.array([psi_initial]*nsignals, dtype = object).T


#initial flips, needed to get yourself into s state
preparation_gates = np.empty((npositions,nsignals), dtype = object)

for i,initial_state in enumerate(initial_state_array.T):
    for j in range(npositions):
        if initial_state[j] == 0:
            preparation_gates[j,i] = qeye(2)
        elif initial_state[j] == 1:
            preparation_gates[j,i] = sigmax()

        else:
            raise ValueError('Unrecognised initial state vector')

#create full multipartite tensor operator
preparation_gates_obj = [tensor(p) for p in preparation_gates.T]

#create full multipartite state
psi_array = np.empty(nsignals, dtype = object)
for i in range(nsignals):
    psi = preparation_gates_obj[i]*psi_initial_array[i]
    psi_array[i] = psi
    print('\npsivec', i,':\n', psi.full())
