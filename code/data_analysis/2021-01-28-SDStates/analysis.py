##--------------------------PREAMBLE------------------------##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#packages 

from stdlib import PlotTemplate, data_loader, TricsDataObject, FitTemplate, full_Rabi, fit_gaussian, fit_constant
##------------------------------PARAMETERS-----------------------##
data_folder = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2021-01-28-SDStates\\"
save_folder = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-01-28-SDStates\\"
pt = PlotTemplate((1,1))
ax = pt.generate_figure()

folders = ['164523/', '164155/', '175112/']
files = ['camera_all.txt', 'PMT1_2.txt']

tdo = data_loader(files, folders, data_folder, 1)[:,:]


##--------------------------AC STARK------------------------------##

# #=============================#
# #ion2



# tdo[0,0].df = tdo[0,0].df.drop([64,65,85,86])
# tdo[0,1].df = tdo[0,1].df.drop([64,65,85,86])

# cycles = tdo[0,1].df.shape[1]
# ion1 = tdo[0,0].df['ion1'].to_numpy()
# ion2 = tdo[0,0].df['ion2'].to_numpy()
# dp_ion1 = tdo[0,1].projection_uncertainty(p = ion1, cycles = cycles)
# dp_ion2 = tdo[0,1].projection_uncertainty(p = ion2, cycles = cycles)


# data_ion2 = tdo[0,0].df['ion2'].to_numpy()

# raman_length = tdo[0,1].df['seq.raman_length'].to_numpy()


# ft = FitTemplate(full_Rabi)

# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 7, vary = False)
# ft.parameters.add('Rabi', 0.119, vary = True)
# ft.parameters.add('phase', 0, vary = False)


# ft.do_minimisation(raman_length, data_ion2[:,np.newaxis])
# param_errors = ft.fit_result_error_dict
# params = ft.get_opt_parameters()
# label_2 = r'$\Omega_{AC}$'+ ': '+ str(round(params['Rabi'],3))+ "(1)MHz" 
# ft.plot_fit(raman_length,data_ion2,errorbars = dp_ion2,ax = ax, label = label_2)
# ft.print_fit_result()


# #=============================#
# #ion1

# data_ion1 = tdo[0,0].df['ion1'].to_numpy()

# ft = FitTemplate(full_Rabi)

# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 7, vary = False)
# ft.parameters.add('Rabi', 0.01, vary = True)
# ft.parameters.add('phase', 0, vary = False)


# ft.do_minimisation(raman_length, data_ion1[:,np.newaxis])
# params = ft.get_opt_parameters()
# param_errors = ft.fit_result_error_dict
# # label_1 = r'$\Omega_{AC}$'+ ': '+ str(round(params['Rabi'],6)) + "(" + str(int(param_errors['Rabi']*100000)) + ")MHz"
# label_1 = ''

# ft.plot_fit(raman_length,data_ion1,errorbars =dp_ion1,ax = ax, colour_index=1, label = label_1)
# ft.print_fit_result()


# plt.title("AC stark flops")
# plt.ylabel('Probability')
# plt.xlabel('Raman length (us)')
# plt.legend()
# #plt.savefig(save_folder + "ACStark.png")
# plt.show()

##----------------------------AOD SCAN----------------------------------## 
# cycles = tdo[1,1].df.shape[1]
# freq = tdo[1,1].df['transitions.AOD.frequency'].to_numpy()/2
# ion1 = tdo[1,0].df['ion1'].to_numpy()
# ion2 = tdo[1,0].df['ion2'].to_numpy()
# dp_ion1 = tdo[1,0].projection_uncertainty(p = ion1, cycles = cycles)
# dp_ion2 = tdo[1,0].projection_uncertainty(p = ion2, cycles = cycles)

# #convert to intensity
# ion1 = np.arcsin(np.sqrt(ion1))/1.1
# ion2 = np.arcsin(np.sqrt(ion2))/1.1
# freq = 3.03*(freq - 259.064987/2)


# ft = FitTemplate(fit_gaussian)
# ft.parameters.add('mean', value = 0, vary = True)
# ft.parameters.add('sigma', value =0.2 , vary= True, max = 2)
# ft.parameters.add('A', value =2 , vary= True)

# ft.do_minimisation(freq, ion2)
# params = ft.get_opt_parameters()
# param_errors = ft.fit_result_error_dict
# ft.print_fit_result()

# labell = r'$\sigma: $' + str(round(params['sigma'],3)) + "(" + str(int(param_errors['sigma']*1000)) + ")MHz"
# ax.scatter(freq, ion1,c = 'm')
# #ax.errorbar(freq, ion1,dp_ion1,ls = 'none',c = 'm',capsize = 3)
# ft.plot_fit(freq, ion2,ax = ax, label = labell, title = "AOD Scan", xlabel="Position (um)", ylabel="Normalised Intensity")
# plt.savefig(save_folder + "AODScan_Intensity.png")
# plt.show()

##----------------------------AOD SCAN PROB----------------------------------## 
cycles = tdo[1,1].df.shape[1]
freq = tdo[1,1].df['transitions.AOD.frequency'].to_numpy()/2
ion1 = tdo[1,0].df['ion1'].to_numpy()
ion2 = tdo[1,0].df['ion2'].to_numpy()
dp_ion1 = tdo[1,0].projection_uncertainty(p = ion1, cycles = cycles)
dp_ion2 = tdo[1,0].projection_uncertainty(p = ion2, cycles = cycles)

freq = 3.03*(freq - 259.064987/2)

ft = FitTemplate(fit_gaussian)
ft.parameters.add('mean', value = 0, vary = True)
ft.parameters.add('sigma', value =0.2 , vary= True, max = 2)
ft.parameters.add('A', value =2 , vary= True)

ft.do_minimisation(freq, ion2)
params = ft.get_opt_parameters()
param_errors = ft.fit_result_error_dict
ft.print_fit_result()

labell = r'$\sigma: $' + str(round(params['sigma'],3)) + "(" + str(int(param_errors['sigma']*1000)) + ")MHz"
ax.scatter(freq, ion1,c = 'm')
#ax.errorbar(freq, ion1,dp_ion1,ls = 'none',c = 'm',capsize = 3)
ft.plot_fit(freq, ion2,ax = ax, label = labell, title = "AOD Scan", xlabel="Position (um)", ylabel="Excitation probability")
plt.savefig(save_folder + "AODScan.png")
plt.show()

##------------------------------POPULATION DUMMY-------------------------------##
# cycles = tdo[2,1].df.shape[1]
# tdo[2,1].df =tdo[2,1].df.drop([27,26])
# tdo[2,0].df =tdo[2,0].df.drop([27,26])

# freq = tdo[2,1].df['channel.Dummy'].to_numpy()
# ion1 = tdo[2,0].df['ion1'].to_numpy()
# ion2 = tdo[2,0].df['ion2'].to_numpy()
# dp_ion1 = tdo[2,0].projection_uncertainty(p = ion1, cycles = cycles)
# dp_ion2 = tdo[2,0].projection_uncertainty(p = ion2, cycles = cycles)
# weight_dp_ion1 = tdo[2,0].projection_uncertainty(p = ion1, cycles = cycles, allow_zero_error = False)
# weight_dp_ion2 = tdo[2,0].projection_uncertainty(p = ion2, cycles = cycles, allow_zero_error = False)
# ##======================##
# #ion2

# ft = FitTemplate(fit_constant)
# ft.parameters.add('C', value = 0.9)

# ft.do_minimisation(freq, ion2, weights= 1/weight_dp_ion2)

# params = ft.get_opt_parameters()
# param_errors = ft.fit_result_error_dict
# ft.print_fit_result()
# lab = r"$P_{ion2}: $" + str(round(params['C'],3)) + "(" + str(int(param_errors['C']*1000)) + ")"
# ft.plot_fit(freq, ion2, ax = ax, errorbars = dp_ion2,label = lab, title = "Populations", xlabel="Dummy", ylabel="Probability")

# ##========================##
# #ion1

# ft = FitTemplate(fit_constant)
# ft.parameters.add('C', value = 0.1)

# ft.do_minimisation(freq, ion1)

# params = ft.get_opt_parameters()
# param_errors = ft.fit_result_error_dict
# ft.print_fit_result()
# lab = r"$P_{ion1}: $" + str(round(params['C'],3)) + "(" + str(int(param_errors['C']*1000)) + ")"
# ft.plot_fit(freq, ion1, ax = ax, errorbars = dp_ion1,label = lab, title = "Populations", xlabel="Dummy", ylabel="Probability", colour_index=1)
# plt.savefig(save_folder + "Populations.png")
# plt.show()