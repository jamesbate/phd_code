"""Simulation class to handle simulation of sensing experiment
"""
##---------------------------PREAMBLE-------------------------##
import qutip 
from qutip.solver import Options
import numpy as np 
import matplotlib.pyplot as plt
from collections import OrderedDict
#packages 

from stdlib import PlotTemplate
#internal dependencies
##-----------------------CLASS DEFINITION------------------------##

class MetrologyExperimentSimulation: 
    """For now, everything has top be added 
    as a qutip object
    """

    def __init__(self, initial_state):
        """Object to handle simulating sensing experiments. In current implementation, there must be some unitary evolution, which 
        is added wtih the add_hamiltonian method. In order to then plot results, you must also use the add_expectations method
        so the object knows what to plot. There is also included functionality for dynamic decoupling, where spin echoes can be 
        applied at points between the evolution. 
        Parameters 
        ----------
        initial_state: qobj
            intial probe state, must be density matrix
    
        Methods
        -------
        add_hamiltonian(self, ham)
            Add unitary evolution
        
        add_dissipator(self, diss)
            Add dissipation i.e. damping channel. See Linblad master equation
        
        evolve(self, times) -> (list, qutip.result)
            evolve under linblad master equation using qutip.mesolve. Returns 
            times that were evaluated (although this is a bit pointless) and the 
            qutip result object

        evolve_with_echoes(self, echo_dict, time_final, time_step_size) -> (list, qutip.result)
            splits to total time into sections. Applied self.evolve function for each section, and 
            applied appropriate echo on qubits, as required for sensing experiment. 

        plot_expectations(self, times,result,indices = False, ax = None)
            plots qutip.result object. Plots each expectation, or a specified list, separately on 
            a figure

        plot_expectations_with_echoes(self, times_list,results_list,indices = False, ax = None)
            applies plot_expectation for a list of qutip.result object i.e. the output of the sensing 
            experiment.

        evaluate_quantum_fischer_information(self, generator) -> int 
            Evaluates the quantum fisher information of the hamiltonian given the final density matrix 
            after evolution (relavent for estimation schemes)
        """
        self.initial_state = initial_state
        #In current implementation, assumed each sensor is a qubit
        self.qubits = len(initial_state.dims[0])
        #plots 
        self.pc = PlotTemplate((1,1))

        #initialising

        #stores final result
        self.final_state = None
        #unitary evolution
        self.hamiltonian = None
        #damping channels 
        self.dissipator = None
        #expectations to plot
        self.expectations_list = []
        #needed for QFI calculation
        self.total_sensing_time = None

    def add_hamiltonian(self, ham):
        self.hamiltonian = ham

    def add_dissipator(self, diss):
        self.dissipator = diss
    
    def add_expectations(self,exp_list):
        self.expectations_list = exp_list

    def evolve(self, times):
        if self.hamiltonian is None: 
            raise ValueError('No Hamiltonian! Current implementation requires unitary evolution.')
        if self.expectations_list == []:
            raise ValueError('No expectations operators to evaluate!')

        result = qutip.mesolve(self.hamiltonian, self.initial_state, times, self.dissipator, e_ops = self.expectations_list, progress_bar = True, options = Options(store_final_state = True, store_states=True))
        self.final_state = result.states[-1]
        return (times, result)
    
    def evolve_with_echoes(self, echo_dict, time_final, time_step_size):
        """Master equation evoluation with intermittent echoes.  
        Parameters
        ----------
        echo_dict: dict 
            dictionary of echo times for each qubit. Echo times that differ 
            by an amount smaller than time_step_size are treated as simultaneous. 
            keys -> qubits, values -> times

        time_final: int 
            final time master equation should evolve until 
        
        time_step_size: int 
            time steps numerical solver should take

        Return
        ------
        (times_list, results_list)
            times_list is a list of the times evaluated for each section 
            results_list is a list fo the qutip.result object after master equation 
            evolution for each section
        """
        #create sorted dictionary, opposite ordering, keys -> time, values -> qubits list
        self.total_sensing_time = time_final
        items = echo_dict.items()
        sorted_items = sorted(items, key = lambda x: x[1])#sort by time
        qubits = np.array(list(echo_dict.keys()))
        echo_dict_sorted = OrderedDict()
        #qubits should be numbered 0 to n-1
        if np.logical_or(np.any(qubits >= self.qubits), np.any(qubits < 0)):
            raise ValueError('Incorrect qubit numbering!')
        
        #lists accumulate simultaneous echoes
        t_list = []
        qu_list = []
        for qu, t in sorted_items:
            t_list.append(t)
            qu_list.append(qu)
            if len(t_list) == 1:
                continue #need to compare two times

            if abs(t_list[-1] - t_list[-2]) < time_step_size:#equal within resolution
                continue
            #this time they are not equal, so dict should include up to last one
            echo_dict_sorted[t_list[0]] = qu_list[:-1]

            #now reset lists to compare next 
            t_list = [t_list[-1]]
            qu_list = [qu_list[-1]]

        #final time should be added also
        echo_dict_sorted[t_list[0]] = qu_list

        #useful to create operators for general dimensions
        unit_list =[qutip.qeye(2) for k in range(self.qubits)]

        #keys -> qubits, values -> operator
        echo_operator_dict = {}
        for q in qubits:
            unit_list[q] = qutip.sigmax()
            echo_operator_dict[q] = qutip.tensor(unit_list)
            unit_list[q] = qutip.qeye(2)#revert back

        #store to return 
        times_list = []
        results_list = []
        #keep track of how long has passed
        total_time = 0

        for (time_echo, qubit_list) in echo_dict_sorted.items():
            #loop over echoes
            print("Initial State: {}".format(self.initial_state))
            #calculate timesteps, added one step to overlap properly
            time_steps = np.arange(0, time_echo - total_time, time_step_size)#goes as far as it can up to echo time within quantisation (always underestimates)

            if time_steps != []:
                #sometimes have echo at t_inital or t_final so no evolution required
                times_list.append(time_steps + total_time)
                #evolve
                (_times, _result) = self.evolve(time_steps)
                #save result
                results_list.append(_result)
                #reset initial state for next evolution section
                self.initial_state = _result.states[-1]
                total_time += time_steps[-1]#not time_echo because of quantisation errors
            
            print("Final State: {}".format(self.initial_state))
            
            print('##------------ECHO: QUBITS {}, TIME {}--------------##'.format(qubit_list, time_echo))
            #apply echo operator
            echo_operator = qutip.tensor(unit_list) 
            for q in qubit_list:
                echo_operator *= echo_operator_dict[q]
            self.initial_state = echo_operator*self.initial_state*echo_operator.dag()
        
        print("Initial State: {}".format(self.initial_state))
        time_steps = np.arange(0, time_final - total_time, time_step_size)
        #final evolution
        (_, _result) = self.evolve(time_steps)
        times_list.append(time_steps + total_time)
        results_list.append(_result)
        #store final state
        self.final_state = _result.states[-1]
        return (times_list, results_list)

    def plot_expectations(self, times,result,indices = False, ax = None):
        if indices == False:
            nplots = len(self.expectations_list)
            indices = range(nplots)
        else:
            nplots = len(indices)

        if ax is None:
            #get axes 
            pc = PlotTemplate((nplots,1))
            ax = pc.generate_figure()

        #plot
        if nplots > 1:
            for n,k in enumerate(indices,0):
                ax[n].plot(times, result.expect[k])
        else:
            ax.plot(times, result.expect[0])

    def plot_expectations_with_echoes(self, times_list,results_list,indices = False, ax = None):
        if len(self.expectations_list) == 0:
            raise ValueError('No expectations to plot!!')
        if indices == False:
            nplots = len(self.expectations_list)
            indices = range(nplots)
        else:
            nplots = len(indices)
        
        if ax is None:
            #get axes 
            pc = PlotTemplate((nplots,1))
            ax = pc.generate_figure()

        for (t, res) in zip(times_list, results_list):
            
            self.plot_expectations(t,res, indices = indices, ax = ax)
        
        # plt.title('Ramsey Experiment')
        # plt.xlabel('Time')
        # plt.ylabel(r'$\langle S_x\rangle$')

    def evaluate_quantum_fischer_information(self, generator):
        (eig_energies, eig_states) = self.final_state.eigenstates()
        generator_diag = (self.total_sensing_time*generator).transform(eig_states)#notice t factor here, G' = Gt as Alfie said
        F = 0
        for j in range(2**(self.qubits)):
            for k in range(2**(self.qubits)):
                if abs(eig_energies[j] - eig_energies[k]) < 1e-10:
                    continue
                F += 2*(eig_energies[j] - eig_energies[k])**2/(eig_energies[j] + eig_energies[k])*abs(generator_diag.full()[j,k])**2 
        return F


if __name__ == "__main__":

    
    
    ham = qutip.sigmax()  
    diss = 0.5*qutip.Qobj([[0,1],[0,0]])
    initial_state = qutip.basis(2,1)

    #initialise
    mse = MetrologyExperimentSimulation(initial_state)

    mse.add_hamiltonian(ham)
    mse.add_dissipator(diss)
    mse.add_expectations([qutip.sigmaz(), qutip.sigmay(), qutip.sigmax()])

    echo_times = OrderedDict()
    echo_times[0] = 0.1
    (times,results) = mse.evolve_with_echoes(echo_times,0.5,0.01)


    # #evolve
    # mse.evolve(np.linspace(0,20,200))

    print(mse.final_state)


    #plot
    mse.plot_expectations_with_echoes(times, results, indices = [0,2])
    plt.show()