from lib import TricsDataObject, data_loader, FitTemplate, fit_rabi_twoions, plot_error_joint, rabi_flops_LD_carrier, fit_constant, full_Rabi, full_Rabi_sq, PlotTemplate, full_Rabi_av
import matplotlib.pyplot as plt
import numpy as np
import math
##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/temperature_plots_redo_ampfree/'

data_folders = ["2020-11-06/182939/", "2020-11-06/183239/","2020-11-06/180533/" ,"2020-11-06/181019/", "2020-11-06/180634/", "2020-11-06/180747/", "2020-11-06/181122/"]
data_folders_2 = ["2020-11-06/181343/","2020-11-06/182002/","2020-11-06/182100/","2020-11-06/182207/","2020-11-06/182316/"]
data_folder_3 = ['2020-11-06/183628/']
data_folder_4 = ['2020-11-06/182740/']
filenames = ["PMT1_2.txt"]
filenames_3 = ["camera_all.txt"]
 
savefiles = ['blue_temperature_fits.png', 'red_temperature_fits.png']


##----------------------------MAIN----------------------------------##
data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]

#create figure
plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure() 
##----------------------------CARRIERS----------------------------------##
#Before pump
beforepump = data_objs[0]
pulse_length = beforepump.df['seq.pulse729_length'].to_numpy()
(probs, dprobs) = beforepump.get_probs(thresholds = [18,70], nmax = 150)
#For the weightings
(_, dprobs_weights) = beforepump.get_probs(thresholds = [18,70], nmax = 150, allow_zero_error = False)

fit_temp = FitTemplate(full_Rabi_sq, log_dir=None)

#set parameters 
fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
fit_temp.parameters.add('detuning', 0, vary = False)
fit_temp.parameters.add('amplitude', 0.93, vary = True)
#free parameters
fit_temp.parameters.add('n_av', 0, vary = False, min = 0)
fit_temp.parameters.add('Rabi', 0.33446590, vary = True)
fit_temp.parameters.add('phase', 1, vary = True)

print(np.array([probs[:,0]]).T, pulse_length)
exit()

results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
#results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
params = fit_temp.get_opt_parameters()
lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + r"$(1)MHz$"+"\nAmplitude: " + str(round(params['amplitude'],2))+ r"$(1)$"
fit_temp.plot_fit(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$", error_lines = 'filled')
fit_temp.print_fit_result()
print(fit_temp.fit_result_error_dict)
#plt.savefig(save_dir+'CarrierBadPump2.png', dpi = 80)
plt.show()
exit()
##===================================================##
# #AFTERPUMP
# afterpumpobj = data_objs[1]

# pulse_length = afterpumpobj.df['seq.pulse729_length'].to_numpy() 
# (probs, dprobs) = afterpumpobj.get_probs(thresholds = [18,70], nmax = 150)
# #For the weightings
# (_, dprobs_weights) = afterpumpobj.get_probs(thresholds = [18,70], nmax = 150, allow_zero_error = False)

# fit_temp = FitTemplate(full_Rabi_av, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068/np.sqrt(2), vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 4, vary = False)
# # fit_temp.parameters.add('Rabi', 0.3, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)
# fit_temp.parameters.add('Rabi1', 0.31, vary = False)
# fit_temp.parameters.add('Rabi2', 0.32, vary = False)

# results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
# fit_temp.print_fit_result()
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi1'],3))+ ','+str(round(params['Rabi2'],3)) + "MHz\n"+r"$n_{av}$: " + str(int(params['n_av']))
# fit_temp.plot_fit(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$", error_lines = 'filled')
# print(fit_temp.fit_result_error_dict)
# plt.savefig(save_dir+'Carrier60Raman2.png', dpi = 80)
# #plt.plot(pulse_length, rabi_flops_LD_carrier(pulse_length, 0.6, 0.068/np.sqrt(2), 10), ':')
# results.params.add('n_av', 5, vary = False)
# #plt.plot(pulse_length, full_Rabi_sq(pulse_length, results.params.valuesdict()), ':', c = 'r')
# plt.show()
##===================================================##
# #FINAL CARRIER, NOT USED
# beforepump = data_loader(filenames, data_folder_4, data_dir_trics)[0,0]
# pulse_length = beforepump.df['seq.pulse729_length'].to_numpy()
# (probs, dprobs) = beforepump.get_probs(thresholds = [18,70], nmax = 150)
# #For the weightings
# (_, dprobs_weights) = beforepump.get_probs(thresholds = [18,70], nmax = 150, allow_zero_error = False)

# fit_temp = FitTemplate(full_Rabi_sq, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 1, vary = True)
# fit_temp.parameters.add('Rabi', 0.33446590, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T)
# fit_temp.print_fit_result()
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "(2)MHz\n"+r"$n_{av}$: " + str(int(params['n_av']))+ r"$(2)$"
# fit_temp.plot_fit(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, label=lab, colour_index=0, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$", error_lines = 'filled')
# print(fit_temp.fit_result_error_dict)
# #plt.savefig(save_dir+'CarrierFinal.png', dpi = 1000)
# plt.show()
##===================================================##
# #CAMERA 
# camdata = data_loader(filenames_3, data_folder_3, data_dir_trics, 1)[0,0]
# pmtcamdata = data_loader(filenames, data_folder_3, data_dir_trics)[0,0]
# pulse_length = pmtcamdata.df['seq.pulse729_length'].to_numpy()
# probs = camdata.get_data(reshape = False) 
# fit_temp = FitTemplate(full_Rabi, log_dir=save_dir)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068/np.sqrt(2), vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 0.1, vary = True)
# fit_temp.parameters.add('Rabi', 0.31, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + r"$MHz$"
# fit_temp.plot_fit(pulse_length, np.array([probs[:,0]]).T, errorbars = None, ax = ax, label=lab, colour_index=2)
# fit_temp.print_fit_result()
# print(fit_temp.fit_result_error_dict)
# results = fit_temp.do_minimisation(pulse_length[:-1], np.array([probs[:-1,1]]).T)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + r"$MHz$"
# fit_temp.plot_fit(pulse_length[:-1], np.array([probs[:-1,1]]).T, errorbars = None, ax = ax, label=lab, colour_index=3, title = "Carrier Flops - Camera", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow}$")
# fit_temp.print_fit_result()
# print(fit_temp.fit_result_error_dict)
# plt.savefig(save_dir+'CameraFlops2.png', dpi = 80)
# #plt.show()
# exit()
##----------------------------BSB----------------------------------##
# for i in range(4,5):
#     #prepare plot for joint plots
#     do = data_objs[i+2] 

#     n_av_lower =1.2
#     n_av_upper =4

#     #apply filter
#     mask = do.get_post_select_mask(thresholds = [18,75], index = 0, p_upper = 0.8,ignore_indices = [38],nmax =150) 
#     #filter more indices 
#     do.df = do.df.iloc[mask]

#     pulse_length = do.df['seq.pulse729_length'].to_numpy()

#     probs, dprobs = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True)
#     #For the weightings
#     (_, dprobs_weights) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = False)


#     fit_temp = FitTemplate(fit_rabi_twoions, log_dir=None)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 0.74, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av',2, vary = False)
#     fit_temp.parameters.add('Rabi', 0.46, vary = False)
#     fit_temp.parameters.add('phase', 0, vary = False)
#     #results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, errorbars = np.array([dprobs[:,0]]).T, dn = 1, pop_state = 2)
#     results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T, dn = 1, pop_state = 2)#removed errorbars 
#     fit_temp.print_fit_result()
#     params = fit_temp.get_opt_parameters()

#     params0 = fit_temp.fit_result_params
#     params1 = fit_temp.fit_result_params.copy()
#     params2= fit_temp.fit_result_params.copy()
#     params1.update({'n_av': n_av_lower})
#     params2.update({'n_av': n_av_upper})

#     args_0 = [fit_temp.fit_result_params, {'dn': 1, 'pop_state': 2}]
#     args_1 = [params1, {'dn': 1, 'pop_state': 2}]
#     args_2 = [params2, {'dn': 1, 'pop_state': 2}]
#     lab = r"$\Omega_0: $" + str(round(params['Rabi'],3)) + "MHz\n"+"Amplitude: "+str(round(params['amplitude'],2))+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+r")$"
#     fit_temp.plot_fit_errorcurves(pulse_length, np.array([probs[:,0]]).T, np.array([dprobs[:,0]]).T,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "BSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$", fill = True)
#     print(fit_temp.fit_result_error_dict)
#     plt.savefig(save_dir+str(i)+'BSB2.png', dpi = 80)
#     plt.show()
#     exit()

##----------------------------RSB----------------------------------##
# data_objs = data_loader(filenames, data_folders_2, data_dir_trics)[:,0]

# for i in range(3,5):
#     #prepare plot for joint plots
#     do = data_objs[i] 
    
#     n_av_lower = 0.8
#     n_av_upper = 2.5

#     #apply filter
#     mask = do.get_post_select_mask(thresholds = [18,75], index = 0,p_upper = 0.8,nmax =150) 
#     #filter more indices 
#     do.df = do.df.iloc[mask]

#     pulse_length = do.df['seq.pulse729_length'].to_numpy() 
#     probs, dprobs = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True)
#     #For the weightings
#     (_, dprobs_weights) = do.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = False)


#     fit_temp = FitTemplate(fit_rabi_twoions, log_dir=None)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor', 0.069, vary = False)
#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 0.74, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av', 1.5, vary = False, min = 0)
#     fit_temp.parameters.add('Rabi', 0.46, vary = False)
#     fit_temp.parameters.add('phase', 0, vary = True)
#     results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, weights = 1/np.array([dprobs_weights[:,0]]).T, dn = -1, pop_state = 2)
#     fit_temp.print_fit_result()
#     params = fit_temp.get_opt_parameters()

#     params0 = fit_temp.fit_result_params
#     params1 = fit_temp.fit_result_params.copy()
#     params2= fit_temp.fit_result_params.copy()
#     params1.update({'n_av': n_av_lower})
#     params2.update({'n_av': n_av_upper})

#     args_0 = [fit_temp.fit_result_params, {'dn': -1, 'pop_state': 2}]
#     args_1 = [params1, {'dn': -1, 'pop_state': 2}]
#     args_2 = [params2, {'dn': -1, 'pop_state': 2}]
#     print(fit_temp.fit_result_error_dict)
#     lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + "MHz\n"+"Amplitude: "+str(round(params['amplitude'],2))+"\n"+r"$n_{av}$: " + str(round(params['n_av'],2))+ r"$("+str(n_av_lower)+', '+str(n_av_upper)+")$"
#     fit_temp.plot_fit_errorcurves(pulse_length, np.array([probs[:,0]]).T, np.array([dprobs[:,0]]).T,args_0, args_1, args_2, color = plot_template.colours[i], label=lab, title = "RSB Flops", xlabel = r"Pulse length $\mu s$", ylabel = r"$P_{\uparrow\uparrow}$", fill = True)
    
#     plt.savefig(save_dir+str(i)+'RSB2.png', dpi = 80)
#     plt.show()
#     exit()

##----------------------------RATIO PLOTS----------------------------------##

#10, 10*2, 20, 40, 60
rsb_data_objs = data_loader(filenames, data_folders_2, data_dir_trics)[:,0]
#0, 20, 10, 2*10, 40
bsb_data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]

folder_indices = [(0,2),(1,3),(2,1),(3,4)]



for k in range(3,4):

    (i,j) = folder_indices[k]

    rsb_data = rsb_data_objs[i]
    bsb_data = bsb_data_objs[j+2]

    rows_max = min(rsb_data.df['seq.pulse729_length'].count(), bsb_data.df['seq.pulse729_length'].count())
    rsb_data.df = rsb_data.df.iloc[0:rows_max]
    bsb_data.df = bsb_data.df.iloc[0:rows_max]
    

    for p in range(2):
        #post select unphysical data and remove



        rsb_pulse_length = rsb_data.df['seq.pulse729_length'].to_numpy() 
        bsb_pulse_length = bsb_data.df['seq.pulse729_length'].to_numpy() 


        #find mean excitation for each sideband 
        rsb_probs, rsb_dprobs = rsb_data.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True)
        rsb_probs = rsb_probs[:,0]
        rsb_dprobs = rsb_dprobs[:,0]
        bsb_probs, bsb_dprobs = bsb_data.get_probs(thresholds = [18,75], nmax = 150, allow_zero_error = True)
        bsb_probs = bsb_probs[:,0]
        bsb_dprobs = bsb_dprobs[:,0]
        #do fit 
        fit_temp = FitTemplate(fit_constant)
        fit_temp.parameters.add('C', 0.5)

        #########################################################
        #attempted error propagation
        frac_error_rsb_me = rsb_dprobs/rsb_probs
        frac_error_bsb_me = bsb_dprobs/bsb_probs
        #get nan's when probs are zero. replace them 
        frac_error_rsb_me[np.isnan(frac_error_rsb_me)] = 0
        frac_error_bsb_me[np.isnan(frac_error_bsb_me)] = 0

        final_frac_error = np.sqrt(frac_error_rsb_me**2 + frac_error_bsb_me**2)
        final_error = final_frac_error*rsb_probs/bsb_probs
        

        #mean_error = np.mean(final_error)

        mean_error = np.std(rsb_probs/bsb_probs)/np.sqrt(len(rsb_pulse_length))
        #mean_error = np.std(rsb_probs/bsb_probs)/1
        #propagate this error to n_av

        n_av = np.sqrt(rsb_probs/bsb_probs)/(1 - np.sqrt(rsb_probs/bsb_probs))
        #error_n = np.std(n_av)/2
        error_n = np.std(n_av)/np.sqrt(len(rsb_pulse_length))
        #break
        #Now find unphysical data
        mask1 = rsb_probs/bsb_probs<1
        mask2 = final_error < (rsb_probs/bsb_probs + 0.001)
        mask = np.logical_and(mask1, mask2)
        mask3 = final_error + rsb_probs/bsb_probs < (1 + 0.001 + 0*final_error)
        mask = np.logical_and(mask, mask3)
        ############################################################
        #print(frac_error_rsb_me, frac_error_bsb_me)
        print(rsb_probs, bsb_probs)

        print(final_error, rsb_probs/bsb_probs, mask)
        # exit()
        indices = np.where(mask)[0]
        

        rsb_data.df = rsb_data.df.iloc[indices]
        bsb_data.df = bsb_data.df.iloc[indices]
    # final_error[np.isnan(final_error)] = 0
    # final_error_weight = final_error.copy()
    # final_error_weight[final_error == 0] = np.mean(final_error[final_error != 0])
    #rsb_result = fit_temp.do_minimisation(rsb_pulse_length, rsb_probs/bsb_probs, weights = 1/final_error_weight)
    rsb_result = fit_temp.do_minimisation(rsb_pulse_length, rsb_probs/bsb_probs)
    params = fit_temp.get_opt_parameters()

    m = np.mean(rsb_probs/bsb_probs, axis = 0)
    print('mean:', np.sqrt(m)/(1-np.sqrt(m)))
    
    n_av_str = str(round(np.sqrt(params['C'])/(1-np.sqrt(params['C'])),1))
    # fit_temp.plot_fit_errorcurves(rsb_pulse_length, rsb_probs/bsb_probs, final_error,[{'C': params['C']}, {}], [{'C': params['C']+mean_error}, {}], [{'C': params['C']-mean_error}, {}], ax = ax, title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB}P_{\uparrow\uparrow}}{\mathrm{BSB}P_{\uparrow\uparrow}}$",label = "n_av: " + n_av_str+'({})'.format(round(error_n,1)), color=plot_template.colours[5], fill = True)
    #plot_error_joint(rsb_pulse_length, rsb_me/bsb_me, final_error,rsb_pulse_length*0 + params['C'], rsb_pulse_length*0 + params['C']+mean_error, rsb_pulse_length*0 + params['C']-mean_error, fill = True,title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB Mean Excitation}}{\mathrm{RSB Mean Excitation}}$",label = "n_av: " + str(round(params['C']/(1-params['C']),2)) + r"$\pm$" + str(round(mean_error,2)), color = colours[k] )
    #fit_temp.plot_fit_errorcurves(rsb_pulse_length, rsb_probs/bsb_probs, final_error,[{'C': params['C']}, {}], [{'C': params['C']+mean_error}, {}], [{'C': params['C']-mean_error}, {}], ax = ax, title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB}P_{\uparrow\uparrow}}{\mathrm{BSB}P_{\uparrow\uparrow}}$",label = "n_av: " + n_av_str+'({})'.format(round(error_n,1)), color=plot_template.colours[5], fill = True)
    n_av_str = str(round(np.sqrt(m)/(1-np.sqrt(m)),1))

    plot_error_joint(rsb_pulse_length,rsb_probs/bsb_probs, final_error, 0*rsb_pulse_length + m, 0*rsb_pulse_length + m-mean_error, 0*rsb_pulse_length + m+mean_error, ax = ax, title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB}P_{\uparrow\uparrow}}{\mathrm{BSB}P_{\uparrow\uparrow}}$",label = "n_av: " + n_av_str+'({})'.format(round(error_n,1)), color=plot_template.colours[5], fill = True)


    fit_temp.print_fit_result()

    print("n_av: ", (np.sqrt(params['C'])/(1-np.sqrt(params['C']))))

    plt.savefig(save_dir+'RatioPlot_noerror_postselect_err_mean'+str(k)+'.png', dpi = 80)
    plt.ylim(ymin = 0, ymax = 1.2)
    exit()
