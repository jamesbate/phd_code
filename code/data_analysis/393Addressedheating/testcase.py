from lib import TricsDataObject, data_loader, FitTemplate, full_Rabi, fit_constant, plot_error_joint, rabi_flops_LD_carrier
import matplotlib.pyplot as plt
import numpy as np

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/temperature_plots_new/'

data_folders = ["2020-11-06/182939/", "2020-11-06/183239/","2020-11-06/180533/" ,"2020-11-06/181019/", "2020-11-06/180634/", "2020-11-06/180747/", "2020-11-06/181122/"]
data_folders_2 = ["2020-11-06/181343/","2020-11-06/182002/","2020-11-06/182100/","2020-11-06/182207/","2020-11-06/182316/"]
data_folder_3 = ['2020-11-06/183628/']
data_folder_4 = ['2020-11-06/182740/']
filenames = ["PMT1_2.txt"]
filenames_3 = ["camera_all.txt"]
 
savefiles = ['blue_temperature_fits_attempt2.png', 'red_temperature_fits_attempt2.png']


##----------------------------MAIN----------------------------------##

#prepare plot for joint plots
plt.rcParams.update({'font.size': 16})  
fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

colours = ['b','m','c','r','tab:orange', 'tab:pink']

#load in data
data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]

##----------------------------CARRIER PLOTS----------------------------------##

afterpumpobj = data_objs[2]
pulse_length = afterpumpobj.df['seq.pulse729_length'].to_numpy() 
(probs, dprobs) = afterpumpobj.get_probs(thresholds = [18,70], allow_zero_error = True)
me, dme = afterpumpobj.get_mean_exc(thresholds = [18,70], nmax= 150)


(probs, dprobs) = afterpumpobj.get_probs(thresholds = [18,70], nmax= 150)

# #plt.plot(pulse_length, probs)
# for i in [0,1,2]:
#     plt.errorbar(pulse_length, probs[:,i], dprobs[:,i], c = colours[i])
#     plt.scatter(pulse_length, probs[:,i], c = colours[i], label = 'p_'+str(i))
# plt.legend()
# #plt.savefig(save_dir+'test1.png', dpi = 1000)
# plt.show() 

plt.errorbar(pulse_length, me, dme)
#plt.savefig(save_dir+'test2.png', dpi = 1000)
plt.plot(pulse_length, afterpumpobj.df['MeanExc'].to_numpy() )
plt.show()


fit_temp = FitTemplate(full_Rabi, log_dir=None)

#set parameters 
fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
fit_temp.parameters.add('detuning', 0, vary = False)
fit_temp.parameters.add('amplitude', 1, vary = False)

#free parameters
fit_temp.parameters.add('n_av', 5, vary = True)
fit_temp.parameters.add('Rabi', 0.3, vary = True)
fit_temp.parameters.add('phase', 1, vary = True)

results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme, n_ions = 2)
fit_temp.print_fit_result()
params = fit_temp.get_opt_parameters()
lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + "MHz\n"+r"$n_{av}$: " + str(round(params['n_av'],1))+ r"$(5, 12))$"
fit_temp.plot_fit(pulse_length, me, errorbars = dme, label=lab, colour_index=1, n_ions = 2, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation")
#plt.savefig(save_dir+'Carrier60Raman.png', dpi = 1000)
#plt.plot(pulse_length, rabi_flops_LD_carrier(pulse_length, 0.6, 0.068/np.sqrt(2), 10), ':')
plt.show()