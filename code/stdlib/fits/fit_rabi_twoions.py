"""Desciption
"""
##-------------------------------PREAMBLE-----------------------------------##
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq, minimize
import numpy as np
from scipy.special import eval_genlaguerre, factorial
#external packages

import math
#stdlib imports

from stdlib import PhysicalConstants, therm_prob
#internal imports
##-------------------------------PARAMETERS-----------------------------------##

def rabi_LD_twoions(Rabi, n, dicke_factor, dn):
    #dn should be 1 for BSB and -1 for RSB

    #dicke factor reduced due increased effetive mass in COM mode 
    dicke_factor /= np.sqrt(2)

    if dn == 1: 
        #BSB
        g = dicke_factor*np.sqrt(2*(2*n + 3))
        return g*Rabi
        
    elif dn == -1: 
        #RSB
        if n == 0:
            return 0
        g =  dicke_factor*np.sqrt(2*(2*n - 1))
        return g*Rabi
    else: 
        raise ValueError('dn can only be +1 for BSB and -1 for RSB!')

def fit_rabi_twoions(t, parameters_dict, **kwargs):
    #pop_state should be 0 for ground, 1 for .. , and 2 for .. 

    sum_limit = 100 
    dn = kwargs['dn']
    pop_state = kwargs['pop_state']

    Rabi = parameters_dict['Rabi']
    n_av = parameters_dict['n_av']
    dicke_factor = parameters_dict['dicke_factor']
    amplitude = parameters_dict['amplitude']

    
    ret = 0
    if dn == -1:
        #RSB

        for n in range(2,sum_limit):

            if pop_state == 0: 
                #SS
                ret += amplitude*therm_prob(n, n_av)*(1 - (n)/(2*n - 1)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))))**2
            
            elif pop_state == 1: 
                #SD, DS
                ret += 2*amplitude*therm_prob(n, n_av)*n/(2*(2*n - 1))*np.sin(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))**2

            elif pop_state == 2:
                #DD
                ret += amplitude*therm_prob(n, n_av)*(n*(n-1))/((2*n - 1)**2)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn)))**2

    elif dn == 1:
        #BSB
        for n in range(0,sum_limit):
            if pop_state == 0: 
                #SS
                ret += amplitude*therm_prob(n, n_av)*(1 - (n+1)/(2*n + 3)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))))**2
            
            elif pop_state == 1: 
                #SD, DS
                ret += 2*amplitude*therm_prob(n, n_av)*(n+1)/(2*(2*n + 3))*np.sin(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))**2

            elif pop_state == 2:
                #DD
                ret += amplitude*therm_prob(n, n_av)*(n+1)*(n+2)/(2*n+3)**2*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn)))**2


    return np.array([ret]).T

def fit_rabi_twoions_nooptpump(t, parameters_dict, **kwargs):
    #pop_state should be 0 for ground, 1 for .. , and 2 for .. 

    sum_limit = 100 
    dn = kwargs['dn']
    pop_state = kwargs['pop_state']

    Rabi = parameters_dict['Rabi']
    n_av = parameters_dict['n_av']
    dicke_factor = parameters_dict['dicke_factor']
    amplitude = parameters_dict['amplitude']

    
    ret = 0
    if dn == -1:
        #RSB

        for n in range(0,sum_limit):

            if pop_state == 0: 
                #SS
                if n == 0:
                    ret +=therm_prob(n, n_av)
                else:
                    ret += amplitude*therm_prob(n, n_av)*(1 - (n)/(2*n - 1)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))))**2
            
            elif pop_state == 1: 
                #SD, DS
                ret += 2*amplitude*therm_prob(n, n_av)*n/(2*(2*n - 1))*np.sin(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))**2

            elif pop_state == 2:
                #DD
                ret += amplitude*therm_prob(n, n_av)*(n*(n-1))/((2*n - 1)**2)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn)))**2

    elif dn == 1:
        #BSB
        for n in range(0,sum_limit):
            if pop_state == 0: 
                #SS
                ret += therm_prob(n, n_av)*(1 - (n+1)/(2*n + 3)*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))))**2
            
            elif pop_state == 1: 
                #SD, DS
                ret += 2*amplitude*therm_prob(n, n_av)*(n+1)/(2*(2*n + 3))*np.sin(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn))**2

            elif pop_state == 2:
                #DD
                ret += amplitude*therm_prob(n, n_av)*(n+1)*(n+2)/(2*n+3)**2*(1 - np.cos(0.5*t*rabi_LD_twoions(Rabi, n, dicke_factor, dn)))**2

    if pop_state == 0:
        ret = np.sqrt(ret)*(1-amplitude) + amplitude*ret
    return np.array([ret]).T

