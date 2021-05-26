##----------------------------PREAMBLE----------------------------------##
from stdlib import TricsDataObject, data_loader, FitTemplate, fit_rabi_twoions, plot_error_joint, rabi_flops_LD_carrier, fit_constant, full_Rabi, full_Rabi_sq, PlotTemplate, full_Rabi_av, full_Rabi_nooptpump, fit_rabi_twoions_nooptpump, full_Rabi_ratio, generalised_Rabi
import matplotlib.pyplot as plt
import numpy as np

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'X:\\measurements\\trics_data\\2021-03-09\\'
save_dir = 'C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\phd\\images\\2021-03-09-AddressedHeating\\'

data_folders = ["215747/"]
data_folders_BSB = ["213228/", "212643/", "212815/", "213021/", "212435/"]
data_folders_RSB = ["214832/", "215015/", "215144/", "215315/", "215447/"]
filenames = ["PMT1_2.txt", "PMT1_1.txt"]
 

##----------------------------MAIN----------------------------------##
data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]
data_objs_BSB = data_loader(filenames, data_folders_BSB, data_dir_trics)[:,0]
data_objs_RSB = data_loader(filenames, data_folders_RSB, data_dir_trics)[:,0]


#create figure
plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure() 

##----------------------------CARRIER----------------------------------##
# do = data_objs[0]

# #thresholds = [15],nmax = 100
# #do.plot_data_histogram(thresholds = [15],nmax = 100,ax = ax)

# pulse_length = do.df['seq.probe_729_length'].to_numpy()
# (me, dme) = do.get_mean_exc(thresholds = [15],nmax = 100)
# #For the weightings
# (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)

# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)
# #free parameters
# fit_temp.parameters.add('n_av', 2, vary = True, min = 0)
# fit_temp.parameters.add('Rabi', 1.04, vary = True)
# fit_temp.parameters.add('phase', 0, vary = True)

# #results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
# results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme_weights)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + r"$(1)MHz$"+"\nn_av: " + str(round(params['n_av'],1))+ r"$(1)$"
# fit_temp.plot_fit(pulse_length, me, errorbars = dme, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", error_lines = 'filled', ax = ax)
# fit_temp.print_fit_result()
# print(fit_temp.fit_result_error_dict)
# plt.savefig(save_dir+'Carrier.png')
# plt.show()
# exit()

##----------------------------BSB----------------------------------##
# for i in range(4,5):
#     #prepare plot for joint plots
#     do = data_objs_BSB[i]

#     n_av_lower = 0.1
#     n_av_upper = 0.2

#     pulse_length = do.df['seq.probe_729_length'].to_numpy() 
#     me, dme = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = True)
#     #For the weightings
#     (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)


#     # #filter
#     # mask = probs[:,2]>0.1
#     # indices = np.where(mask)[0]
#     # probs, dprobs = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True, indices = indices)
#     # #For the weightings
#     # (_, dprobs_weights) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = False, indices = indices)
#     # pulse_length = pulse_length[mask]

#     fit_temp = FitTemplate(full_Rabi, log_dir=None)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av',0.8, vary = True)
#     fit_temp.parameters.add('Rabi', 1.032, vary = False)
#     fit_temp.parameters.add('phase', 0, vary = False)
#     results = fit_temp.do_minimisation(pulse_length, me, m = 1, ax = ax)
#     fit_temp.print_fit_result()
#     params = fit_temp.get_opt_parameters()

#     params0 = fit_temp.fit_result_params
#     params1 = fit_temp.fit_result_params.copy()
#     params2= fit_temp.fit_result_params.copy()
#     params1.update({'n_av': n_av_lower})
#     params2.update({'n_av': n_av_upper})

#     args_0 = [fit_temp.fit_result_params, {'m': 1}]
#     args_1 = [params1, {'m': 1}]
#     args_2 = [params2, {'m': 1}]
#     lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(5)MHz"+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
#     fit_temp.plot_fit_errorcurves(pulse_length, me, dme,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "BSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", fill = True, ax = ax)
#     print(fit_temp.fit_result_error_dict)
#     plt.savefig(save_dir+str(i)+'BSB.png', dpi = 80)
#     plt.show()
#     exit()
##----------------------------RSB2----------------------------------##
# for i in range(3,5):
#     #prepare plot for joint plots
#     do = data_objs_RSB[i]

#     n_av_lower = 2
#     n_av_upper = 4

#     pulse_length = do.df['seq.probe_729_length'].to_numpy() 
#     me, dme = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = True)
#     #For the weightings
#     (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)


#     # #filter
#     # mask = probs[:,2]>0.1
#     # indices = np.where(mask)[0]
#     # probs, dprobs = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True, indices = indices)
#     # #For the weightings
#     # (_, dprobs_weights) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = False, indices = indices)
#     # pulse_length = pulse_length[mask]

#     fit_temp = FitTemplate(generalised_Rabi, log_dir=None)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor_0', 0.069, vary = False)
#     fit_temp.parameters.add('n_av_0',0.55, vary = True)
#     fit_temp.parameters.add('dicke_factor_1', 0.047, vary = False)
#     fit_temp.parameters.add('n_av_1',0.55, vary = True, min =0)
#     fit_temp.parameters.add('dicke_factor_2', 0.047, vary = False)
#     fit_temp.parameters.add('n_av_2',0.55, vary = True,  expr = "n_av_1")


#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 1, vary = False)
#     # fit_temp.parameters.add('n_av',0.55, vary = True)
#     # fit_temp.parameters.add('Rabi', 1.046, vary = False)
#     fit_temp.parameters.add('Rabi', 1.046, vary = False)
#     fit_temp.parameters.add('phase', 0, vary = False)
#     results = fit_temp.do_minimisation(pulse_length, me, m = [-1,0], ax = ax)
#     fit_temp.print_fit_result()
#     params = fit_temp.get_opt_parameters()

#     params0 = fit_temp.fit_result_params
#     params1 = fit_temp.fit_result_params.copy()
#     params2= fit_temp.fit_result_params.copy()
#     params1.update({'n_av_0': n_av_lower})
#     params2.update({'n_av_0': n_av_upper})

#     args_0 = [fit_temp.fit_result_params, {'m': [-1,0]}]
#     args_1 = [params1, {'m': [-1,0]}]
#     args_2 = [params2, {'m': [-1,0]}]
#     lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(6)MHz"+"\n"+r"$n_{av}$: " + str(round(params['n_av_0'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
#     fit_temp.plot_fit_errorcurves(pulse_length, me, dme,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "RSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", fill = True)
#     print(fit_temp.fit_result_error_dict)
#     #plt.savefig(save_dir+str(i)+'RSB.png', dpi = 80)
#     plt.show()
#     exit()
# ##----------------------------RSB----------------------------------##
for i in range(3,5):
    #prepare plot for joint plots
    do = data_objs_RSB[i]

    n_av_lower = 2
    n_av_upper = 4

    pulse_length = do.df['seq.probe_729_length'].to_numpy() 
    me, dme = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = True)
    #For the weightings
    (_, dme_weights) = do.get_mean_exc(thresholds = [15],nmax = 100, allow_zero_error = False)


    # #filter
    # mask = probs[:,2]>0.1
    # indices = np.where(mask)[0]
    # probs, dprobs = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True, indices = indices)
    # #For the weightings
    # (_, dprobs_weights) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = False, indices = indices)
    # pulse_length = pulse_length[mask]

    fit_temp = FitTemplate(full_Rabi, log_dir=None)

    #set parameters 
    fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
    fit_temp.parameters.add('detuning', 0, vary = False)
    fit_temp.parameters.add('amplitude', 1, vary = False)

    #free parameters
    fit_temp.parameters.add('n_av',0.55, vary = False)
    # fit_temp.parameters.add('Rabi', 1.046, vary = False)
    fit_temp.parameters.add('Rabi', 0.86, vary = False)
    fit_temp.parameters.add('phase', 0, vary = False)
    results = fit_temp.do_minimisation(pulse_length, me, m = -1, ax = ax)
    fit_temp.print_fit_result()
    params = fit_temp.get_opt_parameters()

    params0 = fit_temp.fit_result_params
    params1 = fit_temp.fit_result_params.copy()
    params2= fit_temp.fit_result_params.copy()
    params1.update({'n_av': n_av_lower})
    params2.update({'n_av': n_av_upper})

    args_0 = [fit_temp.fit_result_params, {'m': -1}]
    args_1 = [params1, {'m': -1}]
    args_2 = [params2, {'m': -1}]
    lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(6)MHz"+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
    fit_temp.plot_fit_errorcurves(pulse_length, me, dme,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "RSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation", fill = True)
    print(fit_temp.fit_result_error_dict)
    #plt.savefig(save_dir+str(i)+'RSB.png', dpi = 80)
    plt.show()
    exit()

##----------------------------RATIO PLOTS----------------------------------##

# for k in range(0,4):

#     (i,j) = (k, k+1)
#     rsb_data = data_objs_RSB[j]
#     bsb_data = data_objs_BSB[i]

#     #cut to have same number of points
#     rows_max = min(rsb_data.df['seq.probe_729_length'].count(), bsb_data.df['seq.probe_729_length'].count())
#     rsb_data.df = rsb_data.df.iloc[0:rows_max]
#     bsb_data.df = bsb_data.df.iloc[0:rows_max]

#     for p in range(2):

#         rsb_pulse_length = rsb_data.df['seq.probe_729_length'].to_numpy() 
#         bsb_pulse_length = bsb_data.df['seq.probe_729_length'].to_numpy() 

#         #find mean excitation for each sideband 
#         rsb_me, rsb_dme = rsb_data.get_mean_exc(thresholds = [15],nmax = 100)
#         bsb_me, bsb_dme = bsb_data.get_mean_exc(thresholds = [15],nmax = 100)

#         #attempted error propagation
#         frac_error_rsb_me = rsb_dme/rsb_me
#         frac_error_bsb_me = bsb_dme/bsb_me
#         final_frac_error = frac_error_rsb_me + frac_error_bsb_me
#         final_error = final_frac_error*rsb_me/bsb_me

#         mean_error = np.std(rsb_dme/rsb_me)

#         #calculate n_av error from std, removed sqrts?
#         n_av = rsb_me/bsb_me/(1 - rsb_me/bsb_me)
#         error_n = np.std(n_av)
#         print(error_n)

#         #Now find unphysical data
#         mask1 = rsb_me/bsb_me<1
#         mask2 = final_error < rsb_me/bsb_me
#         mask = np.logical_and(mask1, mask2)
#         mask3 = final_error + rsb_me/bsb_me < 1 + 0*final_error
#         mask = np.logical_and(mask, mask3)

#         print(final_error, rsb_me/bsb_me, mask)
#         indices = np.where(mask)[0]


#         rsb_data.df = rsb_data.df.iloc[indices]
#         bsb_data.df = bsb_data.df.iloc[indices]

#     m = np.mean(rsb_me/bsb_me, axis = 0)
#     n_av_mean = m/(1-m)

#     plot_error_joint(rsb_pulse_length, rsb_me/bsb_me, final_error,rsb_pulse_length*0 + m, rsb_pulse_length*0 + m+mean_error, rsb_pulse_length*0 + m-mean_error, fill = True,title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB Mean Excitation}}{\mathrm{RSB Mean Excitation}}$", label = "n_av: {}({})".format(round(n_av_mean,1), int(error_n*10)),color = plot_template.colours[k] )

#     plt.savefig(save_dir+'RatioPlot'+str(k)+'.png', dpi = 1000)


##----------------------------RATIO PLOTS RABI MISMATCH FIT----------------------------------##

# for k in range(0,4):

#     (i,j) = (k, k+1)
#     rsb_data = data_objs_RSB[j]
#     bsb_data = data_objs_BSB[i]

#     #cut to have same number of points
#     rows_max = min(rsb_data.df['seq.probe_729_length'].count(), bsb_data.df['seq.probe_729_length'].count())
#     rsb_data.df = rsb_data.df.iloc[0:rows_max]
#     bsb_data.df = bsb_data.df.iloc[0:rows_max]

#     for p in range(2):

#         rsb_pulse_length = rsb_data.df['seq.probe_729_length'].to_numpy() 
#         bsb_pulse_length = bsb_data.df['seq.probe_729_length'].to_numpy() 

#         #find mean excitation for each sideband 
#         rsb_me, rsb_dme = rsb_data.get_mean_exc(thresholds = [15],nmax = 100)
#         bsb_me, bsb_dme = bsb_data.get_mean_exc(thresholds = [15],nmax = 100)

#         #attempted error propagation
#         frac_error_rsb_me = rsb_dme/rsb_me
#         frac_error_bsb_me = bsb_dme/bsb_me
#         final_frac_error = frac_error_rsb_me + frac_error_bsb_me
#         final_error = final_frac_error*rsb_me/bsb_me

#         mean_error = np.std(rsb_dme/rsb_me)

#         #calculate n_av error from std, removed sqrts?
#         n_av = rsb_me/bsb_me/(1 - rsb_me/bsb_me)
#         error_n = np.std(n_av)
#         #print(error_n)

#         #Now find unphysical data
#         mask1 = rsb_me/bsb_me<1
#         mask2 = final_error < rsb_me/bsb_me
#         mask = np.logical_and(mask1, mask2)
#         mask3 = final_error + rsb_me/bsb_me < 1 + 0*final_error
#         mask = np.logical_and(mask, mask3)

#         #print(final_error, rsb_me/bsb_me, mask)
#         indices = np.where(mask)[0]


#         # rsb_data.df = rsb_data.df.iloc[indices]
#         # bsb_data.df = bsb_data.df.iloc[indices]

#     fit_temp = FitTemplate(full_Rabi_ratio, log_dir=None)

#     #==========#

#     fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
#     fit_temp.parameters.add('detuning', 0.05, vary = True)
#     fit_temp.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av',0.6, vary = False)
#     fit_temp.parameters.add('Rabi', 1.04, vary = False)
#     fit_temp.parameters.add('phase', 0, vary = False)

#     #=========#


#     fit_temp.parameters.add('dicke_factor_2', 0.069, vary = False)
#     fit_temp.parameters.add('detuning_2',0.2, vary = True)
#     fit_temp.parameters.add('amplitude_2', 1, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av_2',0.6, vary = False, expr = 'n_av')
#     fit_temp.parameters.add('Rabi_2', 1.03, vary = False)
#     fit_temp.parameters.add('phase_2', 0, vary = False)

#     m = [1,-1]

#     results = fit_temp.do_minimisation(rsb_pulse_length, rsb_me/bsb_me,m = m, ax = ax)

#     fit_temp.print_fit_result()

#     fit_temp.plot_fit(rsb_pulse_length, rsb_me/bsb_me, errorbars =final_error ,m = m, ax = ax)
#     plt.show()
#     exit()



#     # m = np.mean(rsb_me/bsb_me, axis = 0)
#     # n_av_mean = m/(1-m)

#     # plot_error_joint(rsb_pulse_length, rsb_me/bsb_me, final_error,rsb_pulse_length*0 + m, rsb_pulse_length*0 + m+mean_error, rsb_pulse_length*0 + m-mean_error, fill = True,title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB Mean Excitation}}{\mathrm{RSB Mean Excitation}}$", label = "n_av: {}({})".format(round(n_av_mean,1), int(error_n*10)),color = plot_template.colours[k] )

#     #plt.savefig(save_dir+'RatioPlotDetuned'+str(k)+'.png', dpi = 1000)

