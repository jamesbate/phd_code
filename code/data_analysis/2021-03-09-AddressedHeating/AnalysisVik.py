##----------------------------PREAMBLE----------------------------------##
from stdlib import TricsDataObject, data_loader, FitTemplate, fit_rabi_twoions, plot_error_joint, rabi_flops_LD_carrier, fit_constant, full_Rabi, full_Rabi_sq, PlotTemplate, full_Rabi_av, full_Rabi_nooptpump, fit_rabi_twoions_nooptpump, full_Rabi_ratio, generalised_Rabi
import matplotlib.pyplot as plt
import numpy as np

##----------------------------PARAMETERS----------------------------------##
data_dir_trics = 'X:\\measurements\\trics_data\\2021-03-09\\'
#choose directory to save stuff
save_dir = 'C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\phd\\images\\2021-03-09-AddressedHeating\\'

#folders containing carrier flops data
data_folders = ["215747/"]
#folders containing BSB flops data
data_folders_BSB = ["213228/", "212643/", "212815/", "213021/", "212435/"]
#folders containing RSB flops data
data_folders_RSB = ["214832/", "215015/", "215144/", "215315/", "215447/"]

filenames = ["PMT1_2.txt", "PMT1_1.txt"]
##----------------------------MAIN----------------------------------##
#loading data into objects. These are actually lists of objects for each folder
data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]
data_objs_BSB = data_loader(filenames, data_folders_BSB, data_dir_trics)[:,0]
data_objs_RSB = data_loader(filenames, data_folders_RSB, data_dir_trics)[:,0]

#create figure for plots
plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure() 

##----------------------------CARRIER----------------------------------##
# #create data object
# do = data_objs[0]

# #Uncomoment this to check PMT histograms
# #do.plot_data_histogram(thresholds = [15],nmax = 100,ax = ax)
# #plt.show()

# #get pulse length data as numpy array
# pulse_length = do.df['seq.probe_729_length'].to_numpy()
# #get mean excitation
# (me, dme) = do.get_mean_exc(thresholds = [15],nmax = 100)
# #For the weightings, where error is forced to be non zero
# (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)

# #Now create fitting object for full_RAbi function
# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)
# fit_temp.parameters.add('n_av', 2, vary = True, min = 0)
# fit_temp.parameters.add('Rabi', 1.04, vary = True)
# fit_temp.parameters.add('phase', 0, vary = True)

# #fit curve to data
# results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme_weights)
# fit_temp.print_fit_result()

# #plot result
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + r"$(1)MHz$"+"\nn_av: " + str(round(params['n_av'],1))+ r"$(1)$"
# fit_temp.plot_fit(pulse_length, me, errorbars = dme, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", error_lines = 'filled', ax = ax)
# plt.savefig(save_dir+'Carrier.png')
# plt.show()
# exit()

##----------------------------BSB----------------------------------##
# #choose folder index from data_folders_BSB list
# i = 0

# do = data_objs_BSB[i]

# #upper/lower limits, set by eye to get errors (I don't trust small errors given by fitting function)
# n_av_lower = 0.1
# n_av_upper = 0.2

# pulse_length = do.df['seq.probe_729_length'].to_numpy() 
# me, dme = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = True)
# #For the weightings
# (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)

# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)
# fit_temp.parameters.add('n_av',0.8, vary = True)
# fit_temp.parameters.add('Rabi', 1.032, vary = False)
# fit_temp.parameters.add('phase', 0, vary = False)

# #do fit. m is the sideband: +1 = BSB, -1 = RSB
# results = fit_temp.do_minimisation(pulse_length, me, m = 1, ax = ax)
# fit_temp.print_fit_result()

# #plot result with shaded error curves
# params = fit_temp.get_opt_parameters()
# params1 = fit_temp.fit_result_params.copy()
# params2= fit_temp.fit_result_params.copy()
# params1.update({'n_av': n_av_lower})
# params2.update({'n_av': n_av_upper})
# args_0 = [fit_temp.fit_result_params, {'m': 1}]
# args_1 = [params1, {'m': 1}]
# args_2 = [params2, {'m': 1}]
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(5)MHz"+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
# fit_temp.plot_fit_errorcurves(pulse_length, me, dme,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "BSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", fill = True, ax = ax)
# plt.savefig(save_dir+str(i)+'BSB.png', dpi = 80)
# plt.show()
# exit()

# ##----------------------------RSB----------------------------------##
# #choose folder index from data_folders_BSB list
# i = 0

# do = data_objs_RSB[i]

# n_av_lower = 2
# n_av_upper = 4

# pulse_length = do.df['seq.probe_729_length'].to_numpy() 
# me, dme = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = True)
# #For the weightings
# (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)


# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)
# fit_temp.parameters.add('n_av',0.55, vary = True)
# fit_temp.parameters.add('Rabi', 1.046, vary = False)
# fit_temp.parameters.add('phase', 0, vary = False)
# results = fit_temp.do_minimisation(pulse_length, me, m = -1, ax = ax)
# fit_temp.print_fit_result()

# #plot result
# params = fit_temp.get_opt_parameters()
# params1 = fit_temp.fit_result_params.copy()
# params2= fit_temp.fit_result_params.copy()
# params1.update({'n_av': n_av_lower})
# params2.update({'n_av': n_av_upper})
# args_0 = [fit_temp.fit_result_params, {'m': -1}]
# args_1 = [params1, {'m': -1}]
# args_2 = [params2, {'m': -1}]
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(6)MHz"+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
# fit_temp.plot_fit_errorcurves(pulse_length, me, dme,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "RSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", fill = True)
# #plt.savefig(save_dir+str(i)+'RSB.png', dpi = 80)
# plt.show()
# exit()

