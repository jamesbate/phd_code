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

# #AFTERPUMP

# afterpumpobj = data_objs[1]

# pulse_length = afterpumpobj.df['seq.pulse729_length'].to_numpy() 
# (probs, dprobs) = afterpumpobj.get_probs(thresholds = [18,70])
# me, dme = afterpumpobj.get_mean_exc(thresholds = [18,70], nmax= 150)

# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 5, vary = True)
# fit_temp.parameters.add('Rabi', 0.3, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme, n_ions = 2)
# fit_temp.print_fit_result()
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + "MHz\n"+r"$n_{av}$: " + str(round(params['n_av'],1))+ r"$(5, 12))$"
# fit_temp.plot_fit(pulse_length, me, errorbars = dme, label=lab, colour_index=1, n_ions = 2, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation")
# plt.savefig(save_dir+'Carrier60Raman.png', dpi = 1000)
# #plt.plot(pulse_length, rabi_flops_LD_carrier(pulse_length, 0.6, 0.068/np.sqrt(2), 10), ':')
# plt.show()

# #BEFORE PUMP??

# beforepump = data_objs[0]
# pulse_length = beforepump.df['seq.pulse729_length'].to_numpy()
# (probs, dprobs) = beforepump.get_probs(thresholds = [18,70], nmax = 150)
# me, dme = beforepump.get_mean_exc(thresholds = [18,70], nmax = 150)

# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 0.93, vary = True)
# #free parameters
# fit_temp.parameters.add('n_av', 0, vary = True, min = 0)
# fit_temp.parameters.add('Rabi', 0.33446590, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# # me = np.array([probs[:,0]]).T
# # dme = np.array([dprobs[:,0]]).T

# results = fit_temp.do_minimisation(pulse_length, me, n_ions = 2)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + r"$\pm 0.16MHz$"+"\nAmplitude: " + str(round(params['amplitude'],2))+ r"$\pm 0.01$"
# fit_temp.plot_fit(pulse_length, me, errorbars = dme, label=lab, colour_index=0, n_ions = 2, title = "Carrier Flops", xlabel = r"Pulse length $\mu s$", ylabel = "Mean Excitation")
# fit_temp.print_fit_result()
# #plt.savefig(save_dir+'CarrierBadPump.png', dpi = 1000)
# plt.show()



# #FINAL CARRIER
# beforepump = data_loader(filenames, data_folder_4, data_dir_trics)[0,0]
# pulse_length = beforepump.df['seq.pulse729_length'].to_numpy()
# me, dme = beforepump.get_mean_exc(thresholds = [18,70], nmax = 150, allow_zero_error = False)
# fit_temp = FitTemplate(full_Rabi)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 0, vary = True)
# fit_temp.parameters.add('Rabi', 0.33446590, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme, n_ions = 2)
# fit_temp.plot_fit(pulse_length, me, errorbars = dme, ax = ax, label='Weighted', colour_index=2, n_ions = 2)
# fit_temp.print_fit_result()
# plt.show()

# #CAMERA 
# camdata = data_loader(filenames_3, data_folder_3, data_dir_trics, 1)[0,0]
# pmtcamdata = data_loader(filenames, data_folder_3, data_dir_trics)[0,0]
# pulse_length = pmtcamdata.df['seq.pulse729_length'].to_numpy()
# probs = camdata.get_data(reshape = False) 
# fit_temp = FitTemplate(full_Rabi, log_dir=None)

# #set parameters 
# fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
# fit_temp.parameters.add('detuning', 0, vary = False)
# fit_temp.parameters.add('amplitude', 1, vary = False)

# #free parameters
# fit_temp.parameters.add('n_av', 5, vary = True)
# fit_temp.parameters.add('Rabi', 0.31, vary = True)
# fit_temp.parameters.add('phase', 1, vary = True)

# results = fit_temp.do_minimisation(pulse_length, np.array([probs[:,0]]).T, n_ions = 2)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + r"$MHz$"
# fit_temp.plot_fit(pulse_length, np.array([probs[:,0]]).T, errorbars = None, ax = ax, label=lab, colour_index=2, n_ions = 2)
# fit_temp.print_fit_result()
# results = fit_temp.do_minimisation(pulse_length[:-1], np.array([probs[:-1,1]]).T, n_ions = 2)
# params = fit_temp.get_opt_parameters()
# lab = r"$\Omega_0: $" + str(round(params['Rabi'],2)) + r"$MHz$"
# fit_temp.plot_fit(pulse_length[:-1], np.array([probs[:-1,1]]).T, errorbars = None, ax = ax, label=lab, colour_index=3, n_ions = 2, title = "Carrier Flops - Camera", xlabel = r"Pulse length $\mu s$", ylabel = "Excitation Probability")
# fit_temp.print_fit_result()
# plt.savefig(save_dir+'CameraFlops.png', dpi = 1000)
# plt.show()


##----------------------------RSB----------------------------------##

# data_objs = data_loader(filenames, data_folders_2, data_dir_trics)[:,0]

# for i in range(1,5):


#     #prepare plot for joint plots
#     fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

#     do = data_objs[i]

#     pulse_length = do.df['seq.pulse729_length'].to_numpy() 
#     me, dme = do.get_mean_exc(thresholds = [18,75], nmax = 150, allow_zero_error = False)

#     fit_temp = FitTemplate(full_Rabi)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor', 0.17, vary = False)
#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 0.92, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av', 0.3, vary = True, max = 100, min = 0)
#     fit_temp.parameters.add('Rabi', 0.3, vary = True)
#     fit_temp.parameters.add('phase', 0, vary = False)

#     results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme,m = -1, n_ions = 2)
#     fit_temp.plot_fit(pulse_length, me, errorbars = dme, ax = ax, label='No weights', colour_index=2, m = -1, n_ions = 2)

#     #lab =  "n_av: " + str(round(params['C']/(1-params['C']),2)) + r"$\pm$" + str(round(mean_error,2))
#     #plot_error_joint(pulse_length, me, dme,rsb_pulse_length*0 + params['C'], rsb_pulse_length*0 + params['C']+mean_error, rsb_pulse_length*0 + params['C']-mean_error, fill = False,title = "Red Sideband Flops", xlabel = r"Pulse length $\mu s$",ylabel = "Mean Excitation",label =lab, color = colours[k] )

#     fit_temp.print_fit_result()
#     plt.show()
#     exit()


##----------------------------BSB----------------------------------##

# for i in range(5):
#     #prepare plot for joint plots
#     fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

#     do = data_objs[i+2] 

#     pulse_length = do.df['seq.pulse729_length'].to_numpy() 
#     me, dme = do.get_mean_exc(thresholds = [18,75], nmax = 150, allow_zero_error = False)

#     fit_temp = FitTemplate(full_Rabi)

#     #set parameters 
#     fit_temp.parameters.add('dicke_factor', 0.068, vary = False)
#     fit_temp.parameters.add('detuning', 0, vary = False)
#     fit_temp.parameters.add('amplitude', 0.92, vary = False)

#     #free parameters
#     fit_temp.parameters.add('n_av', 0.14, vary = True, max = 100, min = 0)
#     fit_temp.parameters.add('Rabi', 0.5, vary = True)
#     fit_temp.parameters.add('phase', 0, vary = True)

#     results = fit_temp.do_minimisation(pulse_length, me, weights = 1/dme,m = 1, n_ions = 2)
#     fit_temp.plot_fit(pulse_length, me, errorbars = dme, ax = ax, label='No weights', colour_index=2, m = 1, n_ions = 2)
#     fit_temp.print_fit_result()
#     plt.show()
#     exit()

##----------------------------RATIO PLOTS----------------------------------##

#10, 10*2, 20, 40, 60
rsb_data_objs = data_loader(filenames, data_folders_2, data_dir_trics)[:,0]
#0, 20, 10, 2*10, 40
bsb_data_objs = data_loader(filenames, data_folders, data_dir_trics)[:,0]

folder_indices = [(0,2),(1,3),(2,1),(3,4)]



for k in range(4):

    (i,j) = folder_indices[k]


    #prepare plot for joint plots
    fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))

    rsb_data = rsb_data_objs[i]
    bsb_data = bsb_data_objs[j+2]

    rows_max = min(rsb_data.df['seq.pulse729_length'].count(), bsb_data.df['seq.pulse729_length'].count())

    rsb_data.df = rsb_data.df.iloc[1:rows_max]
    bsb_data.df = bsb_data.df.iloc[1:rows_max]

    rsb_pulse_length = rsb_data.df['seq.pulse729_length'].to_numpy() 
    bsb_pulse_length = bsb_data.df['seq.pulse729_length'].to_numpy() 


    #find mean excitation for each sideband 
    rsb_me, rsb_dme = rsb_data.get_mean_exc(thresholds = [18,75], nmax = 150, allow_zero_error = False)
    bsb_me, bsb_dme = bsb_data.get_mean_exc(thresholds = [18,75], nmax = 150, allow_zero_error = False)
    #do fit 
    fit_temp = FitTemplate(fit_constant)
    fit_temp.parameters.add('C', 0.5)

    frac_error_rsb_me = rsb_dme/rsb_me
    frac_error_bsb_me = bsb_dme/bsb_me

    final_frac_error = frac_error_rsb_me + frac_error_bsb_me
    final_error = final_frac_error*rsb_me/bsb_me

    mean_error = np.mean(final_error)

    #

    rsb_result = fit_temp.do_minimisation(rsb_pulse_length, rsb_me/bsb_me, weights = mean_error)
    params = fit_temp.get_opt_parameters()
    fit_temp.plot_fit(rsb_pulse_length, rsb_me/bsb_me, errorbars = final_error, title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB Mean Excitation}}{\mathrm{RSB Mean Excitation}}$",label = "n_av: " + str(round(params['C']/(1-params['C']),2)), colour_index=k)
    #plot_error_joint(rsb_pulse_length, rsb_me/bsb_me, final_error,rsb_pulse_length*0 + params['C'], rsb_pulse_length*0 + params['C']+mean_error, rsb_pulse_length*0 + params['C']-mean_error, fill = True,title = "RSB/BSB Ratio Plot", xlabel = r"Pulse length $\mu s$",ylabel = r"$\frac{\mathrm{RSB Mean Excitation}}{\mathrm{RSB Mean Excitation}}$",label = "n_av: " + str(round(params['C']/(1-params['C']),2)) + r"$\pm$" + str(round(mean_error,2)), color = colours[k] )
    fit_temp.print_fit_result()

    print("n_av: ", params['C']/(1-params['C']))

    #plt.savefig(save_dir+'RatioPlot_noerror_'+str(k)+'.png', dpi = 1000)

    plt.show()  

    exit()