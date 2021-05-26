from lib import TricsDataObject, data_loader, plot_error_joint, fit_sinusoid, fit_rabi, PlotTemplate, FitTemplate, full_Rabi
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/'

data_folders = ["2020-12-10/154607/", "2020-12-10/160357/"]
filenames = ["PMT1_2.txt"]

savefiles = ['MSGate.png']


##----------------------------MAIN----------------------------------##

plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure() 

beforepump = data_loader(filenames, data_folders, data_dir_trics)[:,0]

# beforepump[0].plot_data_histogram(nmax = 180, thresholds = [25, 100])
# plt.show() 
# exit()

# pulse_length = beforepump[0].df['seq.MS_pulselength'].to_numpy()
# (probs, dprobs) = beforepump[0].get_mean_exc(nmax = 180, thresholds = [25, 100])
# #For the weightings
# (_, dprobs_weights) = beforepump[0].get_mean_exc(thresholds = [18,70], nmax = 150, allow_zero_error = False)

# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.049, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)
# #free parameters
# fit_temp.parameters.add('n_av', 0, vary = True, min = 0)
# fit_temp.parameters.add('Rabi', 0.66590, vary = True)
# fit_temp.parameters.add('phase', 0, vary = True)

# results = fit_temp.do_minimisation(pulse_length, np.array([probs]).T, errorbars = np.array([dprobs]).T)
# #results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + r"$(1)MHz$"+"\nAmplitude: " + str(round(params['amplitude'],2))+ r"$(1)$"
# fit_temp.plot_fit(pulse_length, np.array([probs]).T, errorbars = np.array([dprobs]).T, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$")
# fit_temp.print_fit_result()
# #plt.savefig(save_dir+'CarrierBadPump.png', dpi = 1000)
# plt.show()

pulse_length = beforepump[1].df['seq.MS_pulselength'].to_numpy()
(probs, dprobs) = beforepump[1].get_mean_exc(nmax = 180, thresholds = [25, 100])
#For the weightings
(_, dprobs_weights) = beforepump[1].get_mean_exc(thresholds = [18,70], nmax = 150, allow_zero_error = False)

fit_temp = FitTemplate(full_Rabi, log_dir=None)

#set parameters 
fit_temp.parameters.add('dicke_factor', 0.049, vary = False)
fit_temp.parameters.add('detuning', 0, vary = False)
fit_temp.parameters.add('amplitude', 1, vary = True)
#free parameters
fit_temp.parameters.add('n_av', 0.2, vary = True, min = 0)
fit_temp.parameters.add('Rabi', 0.66590, vary = True)
fit_temp.parameters.add('phase', 0, vary = True)

results = fit_temp.do_minimisation(pulse_length, np.array([probs]).T, errorbars = np.array([dprobs]).T)
#results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
params = fit_temp.get_opt_parameters()
lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + r"$(1)MHz$"+"\nAmplitude: " + str(round(params['amplitude'],2))+ r"$(1)$"
fit_temp.plot_fit(pulse_length, np.array([probs]).T, errorbars = np.array([dprobs]).T, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$")
fit_temp.print_fit_result()
#plt.savefig(save_dir+'CarrierBadPump.png', dpi = 1000)
plt.show()

