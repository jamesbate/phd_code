##-------------------------------PREAMBLE------------------------------------##
import numpy as np 
from lib import sense_optimal_vectors, sense_echo_times, sense_qubit_rescale, fisher_information, fisher_information
from traps.lib import ionic_oscillation_equation
from scipy.optimize import root
import matplotlib.pyplot as plt
##-------------------------------PARAMETERS------------------------------------##
#Taylor Generator
@np.vectorize
def taylor_generator(n):
    return lambda r: r**n 

ion_number_ar = np.arange(3,20,2)

signal_functions = taylor_generator([0,1,2])
r_0 = 0
r_0_ar = np.linspace(0,100,10)
##----------------------------------MAIN---------------------------------------##

qfi_array = []

def ion_positions(ion_number):
    u = np.linspace(-1,1,ion_number).T
    sol = root(ionic_oscillation_equation, u)
    sol.x[abs(sol.x)<1e-10] = 0 
    return sol.x

for n in ion_number_ar:
    nqubits_array = np.array([1]*n)
    r = ion_positions(n)
    signal_function_vectors = np.array([f(r - r_0) for f in signal_functions]).T
    s = sense_optimal_vectors(signal_function_vectors)
    #Corresponds to Ben's A vector.

    #scale optimal vector magnitude to fit the available qubits
    s_scaled = sense_qubit_rescale(s, nqubits_array)
    # print('\ns_scaled:\n',np.round(s_scaled,3))
    # print('\nQFI:\n', np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled),4))
    qfi_array.append(np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled)[-1,-1],4))

plt.plot(ion_number_ar, np.array(qfi_array)**(0.33))
plt.xlabel('ion number')
plt.ylabel('QFI')
plt.show()

qfi_array = []


# for o in r_0_ar:
#     nqubits_array = np.array([1]*6)
#     r = ion_positions(6)
#     signal_function_vectors = np.array([f(r - o) for f in signal_functions]).T
#     s = sense_optimal_vectors(signal_function_vectors)
#     #Corresponds to Ben's A vector.

#     #scale optimal vector magnitude to fit the available qubits
#     s_scaled = sense_qubit_rescale(s, nqubits_array)
#     # print('\ns_scaled:\n',np.round(s_scaled,3))
#     # print('\nQFI:\n', np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled),4))
#     qfi_array.append(np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled)[-1,-1],4))

# plt.plot(r_0_ar, np.array(qfi_array))
# plt.show()


# for o in ion_number_ar:
#     nqubits_array = np.array([1]*6)
#     r = o*ion_positions(6)
#     signal_function_vectors = np.array([f(r) for f in signal_functions]).T
#     s = sense_optimal_vectors(signal_function_vectors)
#     #Corresponds to Ben's A vector.

#     #scale optimal vector magnitude to fit the available qubits
#     s_scaled = sense_qubit_rescale(s, nqubits_array)
#     # print('\ns_scaled:\n',np.round(s_scaled,3))
#     # print('\nQFI:\n', np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled),4))
#     qfi_array.append(np.round(fisher_information(signal_function_vectors.T, s_scaled, -1*s_scaled)[-1,-1],4))

# plt.plot(ion_number_ar, np.array(qfi_array))
# plt.show()
