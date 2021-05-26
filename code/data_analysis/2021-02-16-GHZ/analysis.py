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

data_dir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2021-02-16-GHZ\\"

folders = ["124851/","125706/","122219/", "184326/", "191049/", "193448/", "155644/", "155916/", "182516/", "184532/", "190929/", "194454/", "154117/"]
filenames = ["PMT1_2.txt"]

data_objects = data_loader(filenames, folders, data_dir)
#PMT data objects

filenames_cam = ["camera_all.txt", "camera_ion1.txt", "camera_ion2.txt", "camera_ion3.txt"]
folders_cam = ["122219/"]

data_objects_cam = data_loader(filenames_cam, folders_cam, data_dir, data_column=1)
#Camera data objects

pt = PlotTemplate((1,1))
ax = pt.generate_figure()
##------------------ANALYSIS--------------------##

##========================##
#Camera Data

# do = data_objects_cam[0][0]
# do_singleion = data_objects_cam[0][1]
# do_pmt = data_objects[2][0]
# #data objects 
# do.df = do.df.drop(range(60,75))
# do_singleion.df = do_singleion.df.drop(range(60,75))
# do_pmt.df = do_pmt.df.drop(range(60,75))

# do.df = do.df.drop(range(15,18))
# do_singleion.df = do_singleion.df.drop(range(15,18))
# do_pmt.df = do_pmt.df.drop(range(15,18))
# #filter

# probs = do.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do_singleion.df.shape[1] - 3 #three non data columns
# pulselength = do_pmt.df['seq.probe_729_length'].to_numpy()
# dp = do.projection_uncertainty(probs, cycles)

# for j in range(3):

#     ft = FitTemplate(full_Rabi)
#     #set parameters 
#     ft.parameters.add('dicke_factor', 0.042, vary = False)
#     ft.parameters.add('detuning', 0, vary = False)
#     ft.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     ft.parameters.add('n_av', 9, vary = False)
#     ft.parameters.add('Rabi', 1.04, vary = True)
#     ft.parameters.add('phase', 0, vary = False)

#     ft.do_minimisation(pulselength, probs[:,j])
#     ft.print_fit_result()

#     lab = r"$\Omega: {}$".format("1.07(1)MHz")+"\n"+r"$\langle n \rangle: {}$".format("9")

#     ft.plot_fit(pulselength, probs[:,j], errorbars = dp[:,j], ax = ax, colour_index=j, title = "Camera Rabi Flops", xlabel = "Time (us)", ylabel = "Probability", label = lab)

# plt.show()



##=========================##
#Bichro flops 

do_BSB = data_objects[0][0]
do_BSB.df.drop(range(19,23), axis = 0, inplace = True)#filter
#do_BSB.plot_data_histogram(thresholds = [25,105,175],nmax = 400, ax = ax)
#thresholds = [25,105,175] from histograms
probs,dprobs = do_BSB.get_probs(thresholds = [25, 105, 176], nmax = 400)
me_BSB, dme_BSB = do_BSB.get_mean_exc(thresholds = [25, 105, 176], nmax = 400)
pulselength = do_BSB.df['seq.MS_pulselength'].to_numpy()

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
# ft.plot_fit(pulselength, me_BSB, errorbars = dme_BSB, ax = ax, colour_index=0, label = r"$\Omega: {}MHz$".format("0.625(2)"))
##############
ft = FitTemplate(fit_sinusoid)

ft.parameters.add('A', 0.5, vary = False)
ft.parameters.add('B', 0.6, vary = True)
ft.parameters.add('C', 1.40477761, vary = False)
ft.parameters.add('D', 0.5, vary = False)

ft.do_minimisation(pulselength, me_BSB)
ft.print_fit_result()
ft.plot_fit(pulselength, me_BSB, errorbars = dme_BSB, ax = ax, colour_index=0, label = r"$\Omega: {}MHz$".format("0.625(2)"))
plt.show() 
exit()
##############
#Now RSB 

do_RSB = data_objects[1][0]
#do_RSB.plot_data_histogram(thresholds = [25,105,175],nmax = 400, ax = ax)
#thresholds = [25,105,175] from histograms

probs,dprobs = do_RSB.get_probs(thresholds = [25, 105, 176], nmax = 400)
me_RSB, dme_RSB = do_RSB.get_mean_exc(thresholds = [25, 105, 176], nmax = 400)
pulselength = do_RSB.df['seq.MS_pulselength'].to_numpy()
#fit 
ft = FitTemplate(full_Rabi)

ft.parameters.add('dicke_factor', 0.042, vary = False)
ft.parameters.add('detuning', 0, vary = False)
ft.parameters.add('amplitude', 1, vary = False)

#free parameters
ft.parameters.add('n_av', 15, vary = True)
ft.parameters.add('Rabi', 0.6, vary = True)
ft.parameters.add('phase', -0.8, vary = True)

ft.do_minimisation(pulselength, me_RSB)
ft.print_fit_result()
ft.plot_fit(pulselength, me_RSB, errorbars = dme_RSB, ax = ax, colour_index = 1, label = r"$\Omega: {}MHz$".format("0.630(2)"), title = "Bichro Rabi Flops", xlabel = "Pulse Length (us)", ylabel = "Mean Excitation")
plt.show()
exit()

##=======================##
#MS Gate 

# do = data_objects[3][0]

# do.df.drop(range(32,39), inplace = True, axis = 0)
# #filter

# #do.plot_data_histogram(thresholds = [25,105,160],nmax = 400, ax = ax)
# #thresholds = [25,105,160] from histograms
# pulselength = do.df['seq.MS_pulselength'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,105,160], nmax = 400)
# for k in range(4):
#     ax.errorbar(pulselength, probs[:,k], dprobs[:,k], label = r"$p_{"+str(k)+"}$", capsize = 3, fmt = ".", linestyle = "-")
# plt.title("MS Gate pulse length scan")
# plt.xlabel("Pulse length (us)")
# plt.ylabel("Probability")
# plt.legend()
# plt.show() 

##========================##
#Parity 

# do = data_objects[4][0]

# #do.plot_data_histogram(thresholds = [25,100,170],nmax = 400, ax = ax)
# #thresholds = [25,100,170] from histograms

# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,100,170], nmax = 400)
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

# plt.show() 

##========================##
#Population long 

# do = data_objects[5][0]

# do.df.drop([348], inplace = True, axis = 0)
# do.df.drop(range(240,250), inplace = True, axis = 0)
# do.df.drop(range(70,82), inplace = True, axis = 0)
# do.df.drop(range(40,61), inplace = True, axis = 0)
# #filter

# #do.plot_data_histogram(thresholds = [25,100,160],nmax = 400, ax = ax)
# #thresholds = [25,100,160] from histograms

# probs_1, dprobs_1 = do.get_probs(thresholds = [25,100,160],nmax = 400)
# dummy1 = np.array(range(probs_1[:,0].size))
# # for k in range(4):
# #     ax.errorbar(range(probs[:,k].size),probs[:,k], dprobs[:,k], ls = 'none',marker = '.',capsize = 3, label = r"$p_{"+str(k)+r"}$")
# # plt.title("Long Population Scan")
# # plt.xlabel("Dummy")
# # plt.ylabel("Probability")

# do.df = do.df.iloc[:245]
# probs, dprobs = do.get_probs(thresholds = [25,100,160],nmax = 400)
# dummy = np.array(range(probs[:,0].size))

# means = np.mean(probs, axis = 0)
# std = np.std(probs, axis = 0)/np.sqrt(probs[:,0].size)

# print(means, std)

# #for k in range(4):
# for k in [2]:
#     lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
#     plot_error_joint(dummy1, probs_1[:,k], dprobs_1[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Long Population Scan", xlabel = "Dummy", ylabel = "Probability", label = lab)

# #def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
# plt.legend()
# plt.show()

##========================##
#Parity blocked elevator 

# do_1 = data_objects[6][0]
# #do_1.plot_data_histogram(thresholds = [25,100,165],nmax = 400, ax = ax)
# #thresholds = [25,100,166] from histograms
# phase_1 = do_1.df['seq.phase_MS'].to_numpy()
# probs_1, dprobs_1 = do_1.get_probs(thresholds = [25,100,165],nmax = 400)
# parity_1, dparity_1 = do_1.get_parity(probs_1, dprobs_1)
# #ax.errorbar(phase_1, probs_1[:,0], dprobs_1[:,0])

# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 3, vary = True)
# ft.parameters.add("C",  0.82, vary = True)
# ft.parameters.add("D",  0, vary = True)

# ft.do_minimisation(phase_1, probs_1[:,0])
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# #label = "Amplitude: {}0({})\nFrequency: {}".format(round(params['A'],2), int(params_error['A']*100),round(params['B']/(np.pi),2))
# ft.plot_fit(phase_1, probs_1[:,0], errorbars = dprobs_1[:,0], ax = ax, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity")


# # do_2 = data_objects[7][0]
# # mask = do_2.get_post_select_mask(thresholds = [25,100,165], index = 0, nmax = 400, p_upper = 0.8)
# # do_2.df = do_2.df[mask]
# # #do_1.plot_data_histogram(thresholds = [25,100,165],nmax = 400, ax = ax)
# # #thresholds = [25,100,166] from histograms
# # phase_2 = do_2.df['seq.phase_MS'].to_numpy()
# # probs_2, dprobs_2 = do_2.get_probs(thresholds = [25,100,165],nmax = 400)
# # parity_2, dparity_2 = do_2.get_parity(probs_2, dprobs_2)
# # #ax.errorbar(phase_2, probs_2[:,0], dprobs_2[:,0])

# # #fit 
# # ft = FitTemplate(fit_sinusoid)

# # ft.parameters.add("A", 0.25, vary = False)
# # ft.parameters.add("B", 3, vary = False)
# # ft.parameters.add("C",   -0.4, vary = False)
# # ft.parameters.add("D",  0.25, vary = False)

# # ft.do_minimisation(phase_2, probs_2[:,0])
# # ft.print_fit_result()
# # params = ft.get_opt_parameters()
# # params_error = ft.fit_result_error_dict
# # #label = "Amplitude: {}0({})\nFrequency: {}".format(round(params['A'],2), int(params_error['A']*100),round(params['B']/(np.pi),2))
# # ft.plot_fit(phase_2, probs_2[:,0], errorbars = dprobs_2[:,0], ax = ax, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity", colour_index=1)

# plt.show()



##========================##
#MS Phase compare

# do = data_objects[11][0]
# do.df = do.df.iloc[:50]
# #do.plot_data_histogram(thresholds = [25,100,172],nmax = 400, ax = ax)
# #thresholds = [25,100,172] from histograms

# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,100,172],nmax = 400)
# ax.errorbar(phase, probs[:,0], dprobs[:,0] , capsize = 3, fmt = ".", linestyle = "-", label = "P_0")


# do = data_objects[10][0]
# do.df = do.df.iloc[:50]
# #do.plot_data_histogram(thresholds = [25,100,172],nmax = 400, ax = ax)
# #thresholds = [25,100,172] from histograms

# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,100,172],nmax = 400)
# ax.errorbar(phase, probs[:,0], dprobs[:,0], capsize = 3, fmt = ".", linestyle = "-", label = "P_0")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.show()

##========================##
#MS Phase final gate

# do = data_objects[10][0]
# #do.plot_data_histogram(thresholds = [25,100,172],nmax = 400, ax = ax)
# #thresholds = [25,100,172] from histograms

# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,100,172],nmax = 400)
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(1.12, c = 'k', linestyle = ':', label = "Chosen MS phase: 1.12")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.show()



##========================##
#phase instability?

# do = data_objects[12][0]

# #do.plot_data_histogram(thresholds = [25,100,172],nmax = 400, ax = ax)
# #thresholds = [25,100,172] from histograms

# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(thresholds = [25,100,172],nmax = 400)
# for k in range(1):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# #ax.axvline(1.12, c = 'k', linestyle = ':', label = "Chosen MS phase: 1.12")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.show()

