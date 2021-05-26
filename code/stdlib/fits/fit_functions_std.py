"""Since parameters are passed by a dictionary, 
default values must be implemented manually 
"""
##-------------------------------PREAMBLE-----------------------------------##

import numpy as np 
import matplotlib.pyplot as plt  
from scipy.special import factorial
##---------------------------FITTING FUNCTIONS-------------------------------##

def fit_sinusoid(x, parameters_dict):
    """function: A*np.cos(B*x + C) + D
    default A: 1 
    default C: 0
    default D: 0
    """
    #necessary
    B = parameters_dict['B']

    #defaulted
    if 'A' in parameters_dict:
        A = parameters_dict['A']
    else: 
        A = 1
    if 'C' in parameters_dict:
        C = parameters_dict['C']
    else: 
        C = 0
    if 'D' in parameters_dict:
        D = parameters_dict['D']
    else: 
        D = 0

    #function
    return (A*np.cos(B*x + C) + D)[:,np.newaxis]

def fit_poissonian(x,parameters_dict):
    """function: A*(mean**x*np.exp(-mean))/(factorial(x))
    default A: 1
    """
    #necessary
    mean = parameters_dict['mean']

    #defaulted
    if 'A' in parameters_dict:
        A = parameters_dict['A']
    else: 
        A = 1
    #function
    return A*(mean**x*np.exp(-mean))/(factorial(x))

def fit_lorentzian(x,parameters_dict ):
    """function (A/np.pi)*(Gamma/2)/((x-x_0)**2 + (Gamma/2)**2)
    default x_0: 0
    default  A: 1
    """
    if 'x_0' in parameters_dict:
        x_0 = parameters_dict['x_0']
    else:
        x_0 = 0 
    if 'A' in parameters_dict:
        A = parameters_dict['A']
    else:
        A = 0 
    Gamma = parameters_dict['Gamma']

    return (A/np.pi)*(Gamma/2)/((x-x_0)**2 + (Gamma/2)**2)




def fit_constant(x, parameters_dict):
    """function: C
    """
    C = parameters_dict['C']
    return 0*x + C  
    #Easy way of making array
def fit_linear(x, parameters_dict):
    """function: A*x + B
    """
    A = parameters_dict['A']
    B = parameters_dict['B']
    return A*x + B  

def fit_gaussian(x,parameters_dict):
    #function A(1/(2*np.pi*sigma**2))**0.5*np.exp(-(x - mean)**2/(2*sigma**2))
    #default mean: 0
    #default  sigma: 1
    #default  A: 1
    if 'mean' in parameters_dict:
        mean = parameters_dict['mean']
    else:
        mean = 0 
    if 'sigma' in parameters_dict:
        sigma = parameters_dict['sigma']
    else:
        sigma = 1 
    if 'A' in parameters_dict:
        A = parameters_dict['A']
    else:
        A = 1 


    return A*1/(2*np.pi*sigma**2)**0.5*np.exp(-(x - mean)**2/(2*sigma**2))
