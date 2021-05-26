from lib import TricsDataObject, data_loader, FitTemplate, full_Rabi, fit_constant, plot_error_joint, rabi_flops_LD_red
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
 
savefiles = ['BSB.png', 'RSB.png']



##----------------------------MAIN----------------------------------##

#prepare plot for joint plots
plt.rcParams.update({'font.size': 16})  
fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

colours = ['b','m','c','r','tab:orange', 'tab:pink']

#load in data
data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]

##----------------------------CARRIER PLOTS----------------------------------##

data_objs = data_loader(filenames, data_folders_2, data_dir_trics)[:,0]

bounds = [0.5,2]
k = 2


#prepare plot for joint plots
fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

do = data_objs[k]

pulse_length = do.df['seq.pulse729_length'].to_numpy() 
me, dme = do.get_mean_exc(thresholds = [18,75], nmax = 150, allow_zero_error = True)
#######
(probs, dprobs) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True)
plt.errorbar(pulse_length, probs[:,0], dprobs[:,0])
plt.show()
##########
exit()

fit_temp = FitTemplate(full_Rabi)

#set parameters 
#fit_temp.parameters.add('dicke_factor', 0.175, vary = False)
fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
fit_temp.parameters.add('detuning', 0, vary = False)
fit_temp.parameters.add('amplitude', 0.93, vary = False)

#free parameters
fit_temp.parameters.add('n_av', 2, vary = True)
fit_temp.parameters.add('Rabi', 0.25, vary = True, max = 0.8, min =0)
fit_temp.parameters.add('phase', 0, vary = True)

results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme,m = -1, n_ions = 2)
opt_p = fit_temp.get_opt_parameters()
opt_n = opt_p['n_av']
opt_y = full_Rabi(pulse_length, opt_p, m = -1, n_ions = 2)

#free parameters
fit_temp.parameters.add('n_av', 0.5, vary = False, max = 100, min = 0)

opt_p.update({'n_av': bounds[0]})

lower = full_Rabi(pulse_length, opt_p, m = -1, n_ions = 2)
opt_p.update({'n_av': bounds[1]})
upper = full_Rabi(pulse_length, opt_p, m = -1, n_ions = 2)


lab =  r"$\Omega_0:$" + str(round(opt_p['Rabi'],2)) + "MHz\n" + r"$n_{av}: $" + str(round(opt_n,2)) + " (" + str(bounds[0]) + ", "+ str(bounds[1]) + ")"
plot_error_joint(pulse_length, me, dme,opt_y, lower, upper, fill = False,title = "Blue Sideband Flops", xlabel = r"Pulse length $\mu s$",ylabel = "Mean Excitation",label =lab, color = colours[k], ax = ax)
#plt.plot(pulse_length, rabi_flops_LD_red(pulse_length, 0.6, 0.068/np.sqrt(2), 0.6), '--', c = 'g')
fit_temp.print_fit_result()
#plt.savefig(save_dir+str(k)+savefiles[1], dpi = 1000)
plt.show()
