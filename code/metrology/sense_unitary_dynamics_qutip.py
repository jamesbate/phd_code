"""Find optimal sensing wavefunction for taylor noise, reproducing Bne's code.
I try to use mesolve for unitary dyanmics, but it doesn't seem to work?  
"""
##-------------------------------PREAMBLE------------------------------------##
from qutip import Qobj, ghz_state, sigmax, tensor, qeye, tensor_contract, sigmaz, tensor, mesolve, basis
from lib import sense_optimal_vectors, sense_echo_times, sense_qubit_rescale
import numpy as np
import matplotlib.pyplot as plt
##-------------------------------PARAMETERS------------------------------------##
#Taylor Generator
@np.vectorize
def taylor_generator(n):
    return lambda r: r**n

#positions
#r = np.array([-2.12,-1,0,1,2.12])
r = np.array([-1,0,1])
r_0 = -1.1

signal_functions = taylor_generator([0,1,2])

##------------------------CLASSICAL CALCULATIONS-----------------------------##

#array of how many qubits we have
nqubits_array = np.array([1]*r.size)

#noise signal functions matrix.
signal_function_vectors = np.array([f(r - r_0) for f in signal_functions]).T
nsignals = signal_functions.shape[0]
npositions = r.size

#alphas in paper
signal_strengths = np.array([1]*nsignals)
signal_strengths[1] = 2

#find optimal s vectors for each signal function
#Note, each column vector in the matrix is the optimal s if the signal
#is the corresponding column, and the rest is noise.
s = sense_optimal_vectors(signal_function_vectors)
#Corresponds to Ben's A vector.

#scale optimal vector magnitude to fit the available qubits
s_scaled = sense_qubit_rescale(s, nqubits_array)

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

##------------------------QUANTUM SIMULATION---------------------------##
#I will just take the second signal, this should be generalised
#Firstly, create hamiltonian


#create list of generators
#need to not product fields with respective sigmaz's
#rows: positions, columns: signals
generators = np.empty([npositions, nsignals], dtype = Qobj)
for i in range(nsignals):
    generators[:,i] = np.array([signal_function_vectors[j,i]*sigmaz() for j in range(npositions)], dtype = Qobj)
    print(generators[:,i])

generators_obj = np.array([signal_strengths[i]*tensor(*generators[:,i]) for i in range(nsignals)], dtype = object)
ham = sum(generators_obj)
print(ham)
print(psi_array[2])
times = np.linspace(0,5,3)
result = mesolve(ham/1000, psi_array[0], times, [], [sigmax()], progress_bar = True)
plt.plot(result.times, result.expect[0])
plt.show()
# plt.plot(result.times, result.expect[0])
# plt.show()
