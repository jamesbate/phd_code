"""Tried to implement automatic wavepacket fitter,
but never seemed to optimise properly
"""

import matplotlib.pyplot as plt
from stdlib import CavipyPlotter
from stdlib import PhotonObject, PlotTemplate
from lmfit import minimize, Parameters, fit_report
import numpy as np


def fit_wavepacket(cp, photon_object, roi, init_values,ax = None):
    #right now actually does plot, maybe later just return optimum parameters

    if ax is None:
        pt = PlotTemplate((1,1))
        ax = pt.generate_figure()

    #optimised placement

    def residuals(parameters, region_of_interest):
        #Assumed there exists the same times in each set of data!!
        parameters_dict = parameters.valuesdict()
        amplitude = parameters_dict['amplitude']
        displace_time = parameters_dict['displace_time']
        #get nearest multiple of 0.2 (hack)
        x = displace_time//0.2
        displace_time = 0.2*x

        times_data, probs_data, _  = photon_object.get_normalised_wavepacket(0, 6, 2e6, region_of_interest)
        times, probs= cp.get_wavepacket_single(amplitude, displace_time)
        res = 0
        times = times.to_numpy()
        probs = probs.to_numpy()
        for n,t in enumerate(times_data):
            
            t_index = np.where(times == t)[0]
            p_data = probs_data[n]
            if t_index:
                p_fit = probs[t_index]
                res += (p_fit - p_data)**2

        return res

    parameters = Parameters()
    parameters.add('amplitude', value = init_values[0], vary = True)
    parameters.add('displace_time', value = init_values[1], vary = True)

    fit_result = minimize(residuals, parameters, args = ([roi]),method = 'nelder', nan_policy = 'propagate')
    print(fit_report(fit_result))

    params = fit_result.params.valuesdict()

    cp.plot_wavepacket_single(ax = ax, amplitude = params['amplitude'], displace_time = params['displace_time'])