"""This function plots SINGLE ION rabi flops with error bars, not LD approximation
"""
##-------------------------------PREAMBLE-----------------------------------##
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq, minimize
import numpy as np
from scipy.special import eval_genlaguerre, factorial
import itertools
#external packages

import math
#stdlib imports

from stdlib import PhysicalConstants, therm_prob
#internal imports
##-------------------------------PARAMETERS-----------------------------------##

#Let our ion be in some thermal state

#Modification for laser detuning
detuned_rabi_factor = lambda rabi_dicke, detuning: rabi_dicke/np.sqrt(rabi_dicke**2 + detuning**2)
#object to store physical constants
pc = PhysicalConstants()

def full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions):
    """Returns coupling stregnth for any motional sideband. Full expression, 
    not LD regime. 

    Parameters
    ----------

    n: int
        The sideband from which the transition starts 

    m: int
        The change in sideband number. Transition is from n -> n + m

    dicke_factor: float
        The single ion lambe dicke factor for given laser/axial frequency
    
    Rabi: float
        0th order Rabi. The Rabi frequency if no coupling to motional sidebands was present
    
    n_ions: int
        NEEDS CHANGING, THIS IS NOT GENERALLY APPLICABLE
    """

	#cannot couple below motional 0 state, introduces asymmetry
    if n + m < 0:
	    return 0

    #n_2 is defined to be the larger n, n_1 is defined to be the smaller n
    if m > 0:
        n_2 = n + m
        n_1 = n
    else:
        n_2 = n
        n_1 = n + m

    pf = 1/partial_factorial(n_2, n_1)
    dicke_factor = dicke_factor/np.sqrt(n_ions)#dicke factor given is single ion. Needs to be adjusted for multiple ions...... NOT GENERAL, NEED TO FIX
    return abs(Rabi*np.exp(-dicke_factor**2/2)*dicke_factor**(abs(m))*eval_genlaguerre(n_1, abs(m), dicke_factor**2)*(pf)**(1/2))

def generalised_Rabi_reader(parameters_dict):
    #must have form dicke_factor_1 etc
    #assumed 0,1,2,...

    ld_id = "dicke_factor_"
    n_id = "n_av_"

    keys = parameters_dict.keys()
    mask_ld = [ld_id in x for x in keys]
    mask_n = [n_id in x for x in keys]

    ld_param_array = np.zeros((sum(mask_ld),1))
    n_param_array = np.zeros((sum(mask_n),1))


    keys_ld = np.array(list(keys))[mask_ld]
    keys_n = np.array(list(keys))[mask_n]

    for n,ld in zip(keys_n, keys_ld):
        n_param_array[int(n.replace(n_id, ''))] = parameters_dict[n]
        ld_param_array[int(ld.replace(ld_id, ''))] = parameters_dict[ld]

    return n_param_array, ld_param_array

def generalised_Rabi(t, parameters_dict, total_modes, n_start_index, ld_start_index,**kwargs):
    #SINGLE ION, arbitrary other modes

    m = [0,0]#[dn, mode_index] 
    sum_limit = 100 
    #defaulting parameters: 
    if 'm' in kwargs.keys():
        m = kwargs['m']
    if 'sum_limit' in kwargs.keys():
        sum_limit = kwargs['sum_limit']
    
    m = np.array(m)

    tuple_list = list(parameters_dict.values())

    n_param_array = tuple_list[n_start_index:n_start_index + total_modes]
    ld_param_array = tuple_list[ld_start_index:ld_start_index + total_modes]


    if m[0] > 3:
        raise ValueError('fix full_rabi_dicke before m > 3')

    #unpack parameters 
    # dicke_factor = parameters_dict['dicke_factor']#should be list
    # n_av = parameters_dict['n_av']#should be list
    detuning = parameters_dict['detuning']
    Rabi = parameters_dict['Rabi']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']

    shape = [sum_limit]*len(n_param_array)

    ret = 0
    for idx in itertools.product(*[range(s) for s in shape]):
        break_flag = False
        rabi_fac = Rabi
        therm_fac = 1
        for i in range(len(n_param_array)):
            _n_av = n_param_array[i]
            _n = idx[i]
            if i == m[1]:
                _m = m[0]
            else:
                _m = 0
            _dicke_factor = ld_param_array[i]
            if full_rabi_dicke(_n, _m, _dicke_factor, Rabi, 1) == 0:
                break_flag = True
                break

            rabi_fac *= full_rabi_dicke(_n, _m, _dicke_factor, Rabi, 1)/Rabi

            therm_fac *= therm_prob(_n, _n_av)
            

        if break_flag == False:
            det_fac = detuned_rabi_factor(rabi_fac, detuning)
            ret += amplitude*therm_fac*det_fac**2*np.sin(phase + 0.5*t*rabi_fac/det_fac)**2

    return np.array([ret]).T



def full_Rabi_wrad(t, p, sum_limit = 100, p_fix = [None,None,None,None,None, None, None], m = [0,0]):
	#m represents sideband, DO NOT USE ABOVE 3. Assumes thermal distribution
	# if m > 3:
	# 	raise ValueError('fix full_rabi_dicke before m > 3')
    n_ions = 1

    if 'n_ions' in kwargs.keys():
        n_ions = kwargs['n_ions']


    #unpack parameters 
    dicke_factor_r = parameters_dict['dicke_factor_r']
    dicke_factor_a = parameters_dict['dicke_factor_a']
    n_av_a = parameters_dict['n_av_a']
    n_av_r = parameters_dict['n_av_r']
    detuning = parameters_dict['detuning']
    Rabi = parameters_dict['Rabi']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']



	#and now calculate function
    ret = 0
    for n_1 in range(0,sum_limit):
    	for n_2 in range(0,sum_limit):
            dicke = full_rabi_dicke(n_1, m[0], dicke_factor_a, Rabi)
            dicke *= full_rabi_dicke(n_2, m[1], dicke_factor_r, Rabi)**2/Rabi**2

            if dicke == 0:
                continue
            det_fac = detuned_rabi_factor(dicke, detuning)
            ret += amplitude*therm_prob(n_1, n_av_a)*therm_prob(n_2, n_av_r)*det_fac**2*np.sin(phase + 0.5*t*dicke/det_fac)**2/np.sqrt(n_ions)
    return np.array([ret]).T

def full_Rabi(t, parameters_dict, **kwargs):
    """Say stuff about this function 
    Note: m represents sideband, DO NOT USE ABOVE 3. Assumes thermal distribution
    """
    m = 0 
    sum_limit = 100 
    n_ions = 1
    #defaulting parameters: 
    if 'm' in kwargs.keys():
        m = kwargs['m']
    if 'sum_limit' in kwargs.keys():
        sum_limit = kwargs['sum_limit']
    if 'n_ions' in kwargs.keys():
        n_ions = kwargs['n_ions']

    if m > 3:
        raise ValueError('fix full_rabi_dicke before m > 3')

    #unpack parameters 
    dicke_factor = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    detuning = parameters_dict['detuning']
    Rabi = parameters_dict['Rabi']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']

    ret = 0
    for n in range(0,sum_limit):
        if full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions) == 0:
            continue
        det_fac = detuned_rabi_factor(full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions), detuning)
        ret += amplitude*therm_prob(n, n_av)*det_fac**2*np.sin(phase + 0.5*t*full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions)/det_fac)**2

    return np.array([ret]).T

def full_Rabi_ratio(t, parameters_dict, **kwargs):
    """Do ratio of two different instances of the full Rabi plot 
    with different parameters. For each parameters in full Rabi 
    function, asdd "_2" for the second instance. All kwards should 
    also be given as an list of length 2. 
    """
    #unpack parameters for first instance
    dicke_factor = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    detuning = parameters_dict['detuning']
    Rabi = parameters_dict['Rabi']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']

    params1 = {'dicke_factor': dicke_factor, 'n_av': n_av, 'detuning': detuning, 'Rabi': Rabi, 'phase': phase, 'amplitude': amplitude}

    m = [0,0] 
    sum_limit = [100,100] 
    n_ions = [1,1]
    #defaulting parameters: 
    if 'm' in kwargs.keys():
        m = kwargs['m']
    if 'sum_limit' in kwargs.keys():
        sum_limit = kwargs['sum_limit']
    if 'n_ions' in kwargs.keys():
        n_ions = kwargs['n_ions']
    kwargs1 = {'m': m[0], 'sum_limit': sum_limit[0], 'n_ions': n_ions[0]}

    y_1 = full_Rabi(t, params1, **kwargs1)

    #unpack parameters for second instance
    dicke_factor = parameters_dict['dicke_factor_2']
    n_av = parameters_dict['n_av_2']
    detuning = parameters_dict['detuning_2']
    Rabi = parameters_dict['Rabi_2']
    phase = parameters_dict['phase_2']
    amplitude = parameters_dict['amplitude_2']
    
    params2 = {'dicke_factor': dicke_factor, 'n_av': n_av, 'detuning': detuning, 'Rabi': Rabi, 'phase': phase, 'amplitude': amplitude}
    kwargs2 = {'m': m[1], 'sum_limit': sum_limit[1], 'n_ions': n_ions[1]}

    y_2 = full_Rabi(t, params2, **kwargs2)

    return y_2/y_1


def full_Rabi_nooptpump(t, parameters_dict, **kwargs):
    """Say stuff about this function 
    Note: m represents sideband, DO NOT USE ABOVE 3. Assumes thermal distribution
    """
    m = 0 
    sum_limit = 100 
    n_ions = 1
    pop_state = 'DD'
    #defaulting parameters: 
    if 'm' in kwargs.keys():
        m = kwargs['m']
    if 'sum_limit' in kwargs.keys():
        sum_limit = kwargs['sum_limit']
    if 'n_ions' in kwargs.keys():
        n_ions = kwargs['n_ions']
    if 'pop_state' in kwargs.keys():
        pop_state = kwargs['pop_state']

    if m > 3:
        raise ValueError('fix full_rabi_dicke before m > 3')

    #unpack parameters 
    dicke_factor = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    detuning = parameters_dict['detuning']
    Rabi = parameters_dict['Rabi']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']

    ret = 0
    for n in range(0,sum_limit):
        if full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions) == 0:
            continue
        det_fac = detuned_rabi_factor(full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions), detuning)
        ret += therm_prob(n, n_av)*det_fac**2*np.sin(phase + 0.5*t*full_rabi_dicke(n, m, dicke_factor, Rabi, n_ions)/det_fac)**2
    
    if pop_state == 'DD':
        ret = amplitude*ret 
    elif pop_state == 'SS':
        ret = amplitude*ret + (1-amplitude)*ret**2
    else:
        raise ValueError("Unrecognised pop_state!")

    return np.array([ret]).T

def lamb_dicke(k, theta, mode_freq, mode_mass):
    #general lanb-dicke, trap freq in angular units, mode freq calculated from trap freq
    return k*np.cos(theta)*np.sqrt(pc.h_bar/(2*2*np.pi*mode_mass*mode_freq))

def partial_factorial(n,m):
    #not including m
    tot = 1
    for i in range(0, n-m):
        tot *= n-i
    return tot

def COM_freq(lamb_dicke):
	#assuming our experimental configuration
	#factor of 2 in denom from angle
	k = ((2*np.pi)/729e-9)
	return (pc.h_bar*k**2/(2*np.pi*2*2*pc.m_calc*lamb_dicke**2))

sum_limit = 100

def rabi_flops_LD_red(t, parameters_dict):
    rabi = parameters_dict['Rabi']
    eta = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']
    r = 0
    for n in range(sum_limit):
        r += amplitude*((n_av)/(n_av + 1))**(n+1)*(np.sin(phase + rabi*eta*t*np.sqrt(n + 1)/2)**2)/(n_av + 1)
    return r

def rabi_flops_LD_blue(t, parameters_dict):
    rabi = parameters_dict['Rabi']
    eta = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']
    r = 0
    for n in range(sum_limit):
        r += amplitude*((n_av)/(n_av + 1))**(n)*(np.sin(phase + rabi*eta*t*np.sqrt(n + 1)/2)**2)/(n_av + 1)
    return r

def rabi_flops_LD_carrier(t, parameters_dict):
    rabi = parameters_dict['Rabi']
    eta = parameters_dict['dicke_factor']
    n_av = parameters_dict['n_av']
    phase = parameters_dict['phase']
    amplitude = parameters_dict['amplitude']
    r = 0
    for n in range(sum_limit):
        r += amplitude*((n_av)/(n_av + 1))**(n)*(np.sin(phase + rabi*t*(1 - n*eta**2)/2)**2)/(n_av + 1)
    return r

def full_Rabi_sq(t, parameters_dict, **kwargs):
    return full_Rabi(t, parameters_dict, **kwargs)**2/parameters_dict['amplitude']
    #divide by amp so it isn't double counted

def full_Rabi_av(t, parameters_dict, **kwargs):
    params1 = parameters_dict.copy() 
    params2 = parameters_dict.copy() 
    params1.update({'Rabi': params1['Rabi1']})
    params2.update({'Rabi': params1['Rabi2']})
    return full_Rabi(t, params1, **kwargs)*full_Rabi(t, params2, **kwargs)/parameters_dict['amplitude']
    #divide by amp so it isn't double counted