"""This file contains functions straight from that stat phys textbook
"""
##-------------------------------PREAMBLE-----------------------------------##
import numpy as np
#external packages

from .physical_constants import PhysicalConstants
#internal dependencies

##-------------------------------PREAMBLE-----------------------------------##

#object of physical constants
pc = PhysicalConstants()

def occ_num_boson(E, T, mu):
    return 1/(np.exp((E - mu)/(pc.k_B*T)) - 1)

def occ_num_fermion(E, T, mu):
    return 1/(np.exp((E - mu)/(pc.k_B*T)) + 1)


def phonon_to_temp(phonons, freq = 1e6, mk = True):
    #inverse of the temp_to_phonon. Frequency not in angular

    l = phonons.size
    #error check
    if np.any(np.logical_not(phonons > 0)):
        raise ValueError('Negative number of phonons is unphysical')
    if l == 0:
        return []

    T = pc.h*freq/(pc.k_B*np.log(1+1/phonons))

    if mk == True:
        return 1e3*T
    return T

def temp_to_phonon(temp, freq = 1e6, mk = True):
    l = temp.size
    #error check
    if np.any(np.logical_not(temp > 0)):
        raise ValueError('Negative temperature is unphysical')
    if l == 0:
        return []

    return occ_num_boson(pc.h*freq, temp, 0)
    #phonon mu is 0

therm_prob = lambda n, n_av: (n_av/(n_av + 1))**n/(n_av + 1)

def allan_variance(time, data, time_bin_index):
    #Assumed time is equally spaced

    time_diff = (time[1] - time[0])*time_bin_index

    total_points = time.size - time_bin_index + 1 

    composite_time = [np.mean(time[i:i+time_bin_index]) for i in range(time.size - time_bin_index)]
    composite_data = [np.mean(data[i:i+time_bin_index]) for i in range(data.size - time_bin_index)]

    al_var = sum([(data[i+2] - 2*data[i+1] + data[i])**2 for i in range(time.size - time_bin_index)])/(2*time_diff**2*(time.size - time_bin_index))

    return al_var, composite_time, composite_data, time_diff

def allan_variance_nooverlap(time, data, time_bin_index):
    #Assumed time is equally spaced

    time_diff = (time[1] - time[0])*time_bin_index

    total_points = time.size - time_bin_index + 1 

    composite_time = [np.mean(time[i:i+time_bin_index]) for i in range(time.size - time_bin_index)]
    composite_data = [np.mean(data[i:i+time_bin_index]) for i in range(data.size - time_bin_index)]

    al_var = sum([(data[i+2] - 2*data[i+1] + data[i])**2 for i in range(time.size - time_bin_index)])/(2*time_diff**2*(time.size - time_bin_index))

    return al_var, composite_time, composite_data, time_diff





