"""First attempt at GHZ states with Viktor
"""
##------------------PREAMBLE-------------------##
from stdlib import data_loader
#data handling

from stdlib import FitTemplate, full_Rabi, fit_sinusoid
#fitting 

from stdlib import PlotTemplate, plot_error_joint
#plotting

import numpy as np 
import matplotlib.pyplot as plt
#packages

##------------------PARAMETERS--------------------##

data_dir = "X:\\measurements\\trics_data\\2021-02-25\\"
save_dir = "C:\\Users\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-02-25-GHZ\\"

folders = ["140645/", "141419/", "115222/", "162156/", "162927/", "164723/", "164534/", "164314/", "164031/"]
filenames = ["PMT1_2.txt"]

data_objects = data_loader(filenames, folders, data_dir)
#PMT data objects

filenames_cam = ["camera_all.txt", "camera_ion1.txt", "camera_ion2.txt", "camera_ion3.txt"]
folders_cam = ["140645/", "141419/", "115222/", "162156/", "162927/", "164723/", "164534/", "164314/", "164031/"]

data_objects_cam = data_loader(filenames_cam, folders_cam, data_dir, data_column=1)
#Camera data objects

pt = PlotTemplate((1,1))
ax = pt.generate_figure()
##------------------ANALYSIS--------------------##

# ##========================##
# #Sideband cooled Rabi

# do = data_objects_cam[2][0]
# do_singleion = data_objects_cam[2][1]
# do_pmt = data_objects[2][0]
# #PMT thresholds: nmax = 300, thresholds = [25, 110, 175]

# do.df.drop(range(52,60), inplace = True)
# do_singleion.df.drop(range(52,60), inplace = True)
# do_pmt.df.drop(range(52,60), inplace = True)

# probs = do.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do_pmt.df.shape[1] 
# pulselength = do_pmt.df['seq.probe_729_length'].to_numpy()
# dp = do.projection_uncertainty(probs, cycles)


# for j in range(3):

#     ft = FitTemplate(full_Rabi)
#     #set parameters 
#     ft.parameters.add('dicke_factor', 0.042, vary = False)
#     ft.parameters.add('detuning', 0, vary = False)
#     ft.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     ft.parameters.add('n_av',13, vary = False)
#     ft.parameters.add('Rabi', 1.5, vary = True)
#     ft.parameters.add('phase', 0, vary = True)

#     ft.do_minimisation(pulselength, probs[:,j])
#     ft.print_fit_result()

#     params = ft.get_opt_parameters()
#     params_err = ft.fit_result_error_dict

#     lab = r"$\Omega: {}$".format(round(params['Rabi'],2))+"\n" + r"$\langle n\rangle: {}$".format(round(params['n_av'],1))

#     ft.plot_fit(pulselength, probs[:,j], errorbars = dp[:,j], ax = ax, colour_index=j, title = "Camera Rabi Flops", xlabel = "Time (us)", ylabel = "Probability", label = lab)

# #plt.savefig(save_dir + "CameraSidebandCooledFlops.png")
# plt.show()

# exit()  

##=========================##
#Bichro flops 

# do_BSB = data_objects[0][0]
# do_BSB.df.drop(range(19,23), axis = 0, inplace = True)#filter
# #thresholds = [25,105,175] from histograms
# probs,dprobs = do_BSB.get_probs(thresholds = [25, 105, 176], nmax = 400)
# me_BSB, dme_BSB = do_BSB.get_mean_exc(thresholds = [25, 105, 176], nmax = 400)
# pulselength = do_BSB.df['seq.MS_pulselength'].to_numpy()

# #fit 
# ft = FitTemplate(full_Rabi)

# ft.parameters.add('dicke_factor', 0.042, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 15, vary = True)
# ft.parameters.add('Rabi', 0.6, vary = True)
# ft.parameters.add('phase', -0.8, vary = True)

# ft.do_minimisation(pulselength, me_BSB)
# ft.print_fit_result()
# ft.plot_fit(pulselength, me_BSB, errorbars = dme_BSB, ax = ax, colour_index=0, label = r"$\Omega: {}MHz$".format("0.634(3)"))

# #Now RSB 

# do_RSB = data_objects[1][0]
# #do_RSB.plot_data_histogram(thresholds = [25,105,175],nmax = 400, ax = ax)
# #thresholds = [25,105,175] from histograms

# probs,dprobs = do_RSB.get_probs(thresholds = [25, 105, 176], nmax = 400)
# me_RSB, dme_RSB = do_RSB.get_mean_exc(thresholds = [25, 105, 176], nmax = 400)
# pulselength = do_RSB.df['seq.MS_pulselength'].to_numpy()
# #fit 
# ft = FitTemplate(full_Rabi)

# ft.parameters.add('dicke_factor', 0.042, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 15, vary = True)
# ft.parameters.add('Rabi', 0.6, vary = True)
# ft.parameters.add('phase', -0.8, vary = True)

# ft.do_minimisation(pulselength, me_RSB)
# ft.print_fit_result()
# ft.plot_fit(pulselength, me_RSB, errorbars = dme_RSB, ax = ax, colour_index = 1, label = r"$\Omega: {}MHz$".format("0.629(4)"), title = "Bichro Rabi Flops", xlabel = "Pulse Length (us)", ylabel = "Mean Excitation")
# #plt.savefig(save_dir + "BichroFlops.png")
# plt.show()

# exit()

##=======================##
#MS Gate 

# do = data_objects[3][0]

# do.df.drop(range(5,10), inplace = True, axis = 0)
# do.df.drop([18, 19, 20], inplace = True, axis = 0)
# #filter

# #thresholds = [25,125,210],nmax = 400
# pulselength = do.df['seq.MS_pulselength'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,125,210], nmax = 400)
# for k in range(4):
#     ax.errorbar(pulselength, probs[:,k], dprobs[:,k], label = r"$p_{"+str(k)+"}$", capsize = 3, fmt = ".", linestyle = "-")
# plt.title("MS Gate pulse length scan")
# plt.xlabel("Pulse length (us)")
# plt.ylabel("Probability")
# plt.legend()
# #plt.savefig(save_dir + "MSPulselength.png")
# plt.show() 



##========================##
#Parity 

# do = data_objects[6][0]

# #do.plot_data_histogram(thresholds = [25,125,210],nmax = 400, ax = ax)
# #thresholds = [25,125,210],nmax = 400

# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,125,210],nmax = 400)
# parity, dparity = do.get_parity(probs, dprobs)

# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 20, vary = True)
# ft.parameters.add("C",  0, vary = True)
# ft.parameters.add("D",  0, vary = True)

# ft.do_minimisation(pulselength, parity, weights = 1/dparity)
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# label = "Amplitude: {}0({})\nFrequency: {}".format(round(params['A'],2), int(params_error['A']*100),round(params['B']/(np.pi),2))
# ft.plot_fit(pulselength, parity, errorbars = dparity, ax = ax, label = label, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity")
# #plt.savefig(save_dir + "Parity.png")
# plt.show() 

##========================##
#Population 

# do = data_objects[5][0]

# # do.df.drop([348], inplace = True, axis = 0)
# # do.df.drop(range(240,250), inplace = True, axis = 0)
# # do.df.drop(range(70,82), inplace = True, axis = 0)
# # do.df.drop(range(40,61), inplace = True, axis = 0)
# # #filter

# #do.plot_data_histogram(thresholds = [25,125,200],nmax = 400, ax = ax)
# #thresholds = [25,125,20],nmax = 400 from histograms

# probs_1, dprobs_1 = do.get_probs(thresholds = [25,125,200],nmax = 400)
# dummy1 = np.array(range(probs_1[:,0].size))
# # for k in range(4):
# #     ax.errorbar(range(probs[:,k].size),probs[:,k], dprobs[:,k], ls = 'none',marker = '.',capsize = 3, label = r"$p_{"+str(k)+r"}$")
# # plt.title("Long Population Scan")
# # plt.xlabel("Dummy")
# # plt.ylabel("Probability")

# # do.df = do.df.iloc[:245]
# # probs, dprobs = do.get_probs(thresholds = [25,100,160],nmax = 400)
# # dummy = np.array(range(probs[:,0].size))

# means = np.mean(probs_1, axis = 0)
# std = np.std(probs_1, axis = 0)/np.sqrt(probs_1[:,0].size)

# print(means, std)

# for k in range(4):
#     lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
#     plot_error_joint(dummy1, probs_1[:,k], dprobs_1[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Long Population Scan", xlabel = "Dummy", ylabel = "Probability", label = lab)

# #def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
# plt.legend()
# #plt.savefig(save_dir + "ShitPopScan.png")
# plt.show()

##========================##
#MS Phase

# do = data_objects[7][0]
# #do.plot_data_histogram(thresholds = [25,125,210],nmax = 400, ax = ax)
# #thresholds = [25,125,210],nmax = 400 from histograms
# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,125,210],nmax = 400)
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(1.2, c = 'k', linestyle = ':', label = "Chosen MS phase: 1.2")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSPhase.png")
# plt.show()

##========================##
#Finding pi/2 time

# do = data_objects[8][0]
# pithalftime = do.df['seq.pihalftime_carrier'].to_numpy()
# # probs, dprobs = do.get_probs(thresholds = [25,125,210],nmax = 400)
# # for k in range(4):
# #     ax.errorbar(pithalftime, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# me, dme = do.get_mean_exc(thresholds = [25,125,210],nmax = 400)
# ax.errorbar(pithalftime, me, dme, linestyle = '-', capsize = 3)
# #ax.axvline(1.2, c = 'k', linestyle = ':', label = "Chosen MS phase: 1.2")
# plt.title("pi/2 time scan")
# plt.xlabel("pi/2 time")
# plt.ylabel("Mean Excitation")
# plt.legend()
# plt.savefig(save_dir + "pihalftime.png")
# plt.show()

##========================##
#115027 -> we were actually detuned