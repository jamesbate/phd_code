"""Only consider motional phase space, not qubit
only consider axial dimension. Only COM. Only set scatter event
Cavity ignored
"""
##---------------------------------PREAMBLE------------------------------------------##
from qutip import qeye, sigmax, basis, Qobj, displace, num, plot_fock_distribution, wigner, coherent
import numpy as np
import matplotlib.pyplot as plt 
from stdlib import PhysicalConstants, PlotTemplate
from random import random
import copy
##---------------------------------PARAMETERS------------------------------------------##

k_397 = 2*np.pi/397e-9
k_393 = 2*np.pi/393e-9
k_854 = 2*np.pi/854e-9

freq_trap = 1e6
#trap frequency

phonon_levels = 200
#number of phonon levels to consider (system is finite). Make sure the 
#system doesn't saturate and exhibit periodic effects.

scatters = 200
#number of kick events
random_repeats = 50
#repeating random events

##---------------------------------CLASS DEFINTION------------------------------------------##

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

class MotionalState(Qobj):#not sure I've used inheritance properly here
    def __init__(self, qobj_init, trap_freq, ions =1):
        self.qobj = qobj_init
        self.trap_freq = trap_freq
        self.phonon_levels = self.qobj.dims[0][0]
        self.ions = ions
        self.alpha = 0

        self.alpha_list = [0]
        self.n_av_list = [0]

        self.pc = PhysicalConstants()

    def apply_kick_directed(self, angle, k, update_alpha = False):
        """Directed laser, random time (i.e. random phase)
        angle: angle wrt axial
        k: momentum of kick
        """
        energy = (self.pc.h_bar*k)**2/(2*self.ions*self.pc.m_calc)
        lamb_dicke = np.sqrt(energy/(self.pc.h*self.trap_freq))*np.cos(angle)
        kick_phase = 2*np.pi*random()

        #apply displacement operator of set length lamb_dicke at random angle in phase space
        self.qobj = displace(self.phonon_levels, lamb_dicke*complex(np.cos(kick_phase),np.sin(kick_phase)))*self.qobj 

        if update_alpha:
            alpha = self.find_alpha(np.linspace(-3,3,200))
            self.alpha = complex(alpha[0], alpha[1])

    def apply_kick_random(self, k, update_alpha = False):
        """Spontaneous emission, random time and phase
        k: momentum of kick
        """
        #random angle with z axis, sampled from 3d sphere
        angle = self.generate_zangle_random_3D()

        #random kick phase (uniform)
        kick_phase = 2*np.pi*random()

        energy = (self.pc.h_bar*k)**2/(2*self.ions*self.pc.m_calc)
        lamb_dicke = np.sqrt(energy/(self.pc.h*self.trap_freq))*np.cos(angle)#equivalent to random uniform random length factor?

        #apply displacement operator of set length lamb_dicke at random angle in phase space
        self.qobj = displace(self.phonon_levels, lamb_dicke*complex(np.cos(kick_phase),np.sin(kick_phase)))*self.qobj 

        if update_alpha:
            alpha = self.find_alpha(np.linspace(-3,3,200))
            self.alpha = complex(alpha[0], alpha[1])


    def generate_zangle_random_3D(self):
        """sample z angle form uniform sphere
        """
        r = 2*random() - 1
        angle = np.arccos(r)
        return angle
    
    def mean_number(self):
        """Calculate expectation of number operator
        """
        return num(self.phonon_levels).matrix_element(self.qobj, self.qobj)
    
    def find_alpha(self, xyrange):
        print('finding')
        W_coherent = wigner(self.qobj, xyrange, xyrange)
        res = xyrange[-1] - xyrange[-2]
        result = res*(np.array(np.unravel_index(W_coherent.argmax(), W_coherent.shape)) - xyrange.size/2)
        print('done')
        print(result)
        return [result[1], result[0]]
    
    def record_state_properties(self):
        self.alpha_list.append(self.alpha)
        self.n_av_list.append(self.mean_number().real)
    
    def plot_n_av(self, ax):

        ax.plot(np.arange(0,len(self.n_av_list), 1), [k.real for k in self.n_av_list], label = 'Random kicks (1 sample)')

        plt.xlabel('Loop Number')
        plt.ylabel(r'$\langle n \rangle$')
        plt.legend()
    
    def plot_alpha(self, ax):
        real_part = [k.real for k in self.alpha_list]
        im_part = [k.imag for k in self.alpha_list]
        print(real_part, im_part)
        ax.plot(real_part, im_part, 'r')

    def plot_wigner(self, plot_range,ax):
        W_coherent = wigner(self.qobj, plot_range, plot_range)
        ax.contourf(plot_range, plot_range, W_coherent, 100)


##-----------------------------------BICHROLOOP----------------------------------##

# scattering_events = np.arange(0,scatters + 1,1)
# mean_n = np.zeros((scatters+1, random_repeats))

# for j in range(random_repeats):

#     print('Run ',j)

#     #initially ground state cooled
#     state= MotionalState(Qobj(coherent(phonon_levels, 0)), freq_trap, ions = 2) 


#     for n in range(scatters):
#         #scatter loop

#         #spontaneous decay
#         state.apply_kick_random(k_393)
#         state.record_state_properties()

#         # plot_fock_distribution(state.qobj)
#         # plt.show()

#     if j == 0:
#         state.plot_n_av(ax)
#     if j == 2:
#         state.plot_n_av(ax)

#     mean_n[:,j] = np.array(state.n_av_list)

# mean_n = np.mean(mean_n, axis = 1)

# ax.plot(scattering_events, mean_n, label = 'Random kicks ({} samples)'.format(random_repeats))

# plt.xlabel('Loop Number')
# plt.ylabel(r'$\langle n \rangle$')
# plt.title('Heating of COM mode of two ions due to scattering events (1MHz trap frequency):\nrandom 393nm emission ({} repeats)'.format(random_repeats))
# plt.legend()
# plt.show()

# state.plot_alpha(ax)
# plot_range = np.linspace(-2,2,200)
# state.plot_wigner(plot_range, ax)
# plt.show()
# exit()

##-----------------------------------BICHROLOOP WITH PHASE PLOT----------------------------------##


# #initially ground state cooled
# state= MotionalState(Qobj(coherent(phonon_levels, 0)), freq_trap, ions = 2) 


# for n in range(scatters):
#     #scatter loop

#     #spontaneous decay
#     state.apply_kick_random(k_393, update_alpha = True)
#     state.record_state_properties()

#     # plot_fock_distribution(state.qobj)
#     # plt.show()

# state.plot_alpha(ax)
# plot_range = np.linspace(-2,2,200)
# state.plot_wigner(plot_range, ax)
# plt.show()
# exit()

##-----------------------------------OPTPUMPLOOP----------------------------------##

scattering_events = np.arange(0,scatters + 1,1)
mean_n = np.zeros((scatters+1, random_repeats))

for j in range(random_repeats):

    print('Run ',j)

    #initially ground state cooled
    state= MotionalState(Qobj(basis(phonon_levels, 0)), freq_trap, ions = 2) 


    for n in range(scatters):

        #scatter loop
        state.apply_kick_directed(np.pi/4, k_397)
        state.apply_kick_random(k_397)
        state.record_state_properties()

        # plot_fock_distribution(state.qobj)
        # plt.show()

    if j == 0:
        state.plot_n_av(ax)
    if j == 2:
        state.plot_n_av(ax)

    mean_n[:,j] = state.n_av_list

mean_n = np.mean(mean_n, axis = 1)

ax.plot(scattering_events, mean_n, '--',label = 'Random kicks ({} samples)'.format(random_repeats))

plt.xlabel('Loops')
plt.ylabel(r'$\langle n \rangle$')
plt.title('Heating of COM mode of two ions due to optical pumping (1MHz trap frequency):\n45deg 397nm absorption and random emission ({} repeats)'.format(random_repeats))
plt.legend()
plt.show()

##-----------------------------------OPTPUMPLOOP WITH PHASE PLOT----------------------------------##

# #initially ground state cooled
# state= MotionalState(Qobj(coherent(phonon_levels, 0)), freq_trap, ions = 2) 


# for n in range(scatters):
#     #scatter loop
#     print("Scatter ", n)
#     state.apply_kick_directed(np.pi/4, k_397)
#     state.apply_kick_random(k_397, update_alpha = True)
#     state.record_state_properties()

#     # plot_fock_distribution(state.qobj)
#     # plt.show()

# plot_range = np.linspace(-2,2,200)
# state.plot_wigner(plot_range, ax)
# state.plot_alpha(ax)
# plt.show()