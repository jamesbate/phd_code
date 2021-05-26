"""GHZ states with Marco, 729 stability issue noticed
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

data_dir = "X:\\measurements\\trics_data\\2021-03-04\\"
save_dir = "C:\\Users\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-03-04-GHZ\\"

folders = ["155314/", "161603/", "162053/", "181434/", "182037/", "170109/", "180739/", "171310/", "164205/", "164813/", "174147/", "174725/", "173803/", "173636/"]
filenames = ["PMT1_2.txt"]

data_objects = data_loader(filenames, folders, data_dir)
#PMT data objects

filenames_cam = ["camera_all.txt", "camera_ion1.txt", "camera_ion2.txt", "camera_ion3.txt"]
folders_cam = ["155314/", "161603/", "162053/"]

data_objects_cam = data_loader(filenames_cam, folders_cam, data_dir, data_column=1)

pt = PlotTemplate((1,1))
ax = pt.generate_figure()
##------------------ANALYSIS--------------------##

##================================##
#Carrier flops with sideband cooling, 155314

# do_cam = data_objects_cam[0][0]
# do_pmt = data_objects[0][0]
# #PMT thresholds: nmax = 600, thresholds = [50, 230, 350]

# # do.df.drop(range(52,60), inplace = True)
# # #do_singleion.df.drop(range(52,60), inplace = True)
# # do_pmt.df.drop(range(52,60), inplace = True)

# probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do_pmt.df.shape[1] 
# pulselength = do_pmt.df['seq.probe_729_length'].to_numpy()
# dp = do_cam.projection_uncertainty(probs, cycles)


# for j in range(3):

#     ft = FitTemplate(full_Rabi)
#     #set parameters 
#     ft.parameters.add('dicke_factor', 0.042, vary = False)
#     ft.parameters.add('detuning', 0, vary = False)
#     ft.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     ft.parameters.add('n_av',10, vary = False)
#     ft.parameters.add('Rabi', 1.5, vary = True)
#     ft.parameters.add('phase', 0, vary = True)

#     ft.do_minimisation(pulselength, probs[:,j])
#     ft.print_fit_result()

#     params = ft.get_opt_parameters()
#     params_err = ft.fit_result_error_dict

#     lab = r"$\Omega: {}$".format(round(params['Rabi'],2))+"MHz\n" + r"$\langle n\rangle: {}$".format(round(params['n_av'],1))

#     ft.plot_fit(pulselength, probs[:,j], errorbars = dp[:,j], ax = ax, colour_index=j, title = "Camera Rabi Flops", xlabel = "Time (us)", ylabel = "Probability", label = lab)

# #plt.savefig(save_dir + "CameraSidebandCooledFlops.png")
# plt.show()

# exit()  


##=================================##
#Bichro flops, 161603, 162053

# do_BSB = data_objects[1][0]

# #histogram plot
# #do_BSB.plot_data_histogram(nmax = 500, thresholds = [30, 120, 200], ax = ax)

# probs,dprobs = do_BSB.get_probs(nmax = 600, thresholds = [30, 120, 200])
# me_BSB, dme_BSB = do_BSB.get_mean_exc(nmax = 600, thresholds = [30, 120, 200])
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
# ft.plot_fit(pulselength, me_BSB, errorbars = dme_BSB, ax = ax, colour_index=0, label = r"$\Omega: {}MHz$".format("0.613(1)")+ "\n" + r"$t_\pi: {}\mu s$".format("5.12(1)"))

# #Now RSB 
# do_RSB = data_objects[2][0]
# #filter
# do_RSB.df.drop([16,17],inplace = True)

# probs,dprobs = do_RSB.get_probs(nmax = 600, thresholds = [30, 120, 200])
# me_RSB, dme_RSB = do_RSB.get_mean_exc(nmax = 600, thresholds = [30, 120, 200])
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
# ft.plot_fit(pulselength, me_RSB, errorbars = dme_RSB, ax = ax, colour_index = 1, label = r"$\Omega: {}MHz$".format("0.611(1)") + "\n" + r"$t_\pi: {}\mu s$".format("5.14(1)"), title = "Bichro Rabi Flops", xlabel = "Pulse Length (us)", ylabel = "Mean Excitation")
# plt.savefig(save_dir + "BichroFlops.png")
# plt.show()

# exit()


##=================================##
#Best MS gate pulselength,  

# do = data_objects[5][0]
# do.df.drop(range(35,40), inplace = True)

# pulselength = do.df['seq.MS_pulselength'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 200])

# for k in range(4):
#     ax.errorbar(pulselength, probs[:,k], dprobs[:,k], label = r"$p_{"+str(k)+"}$", capsize = 3, fmt = ".", linestyle = "-")
# ax.axvline(120, linestyle = ':',label = r"$t_{gate}: 120\mu s$", c = 'k')
# plt.title("MS Gate pulse length scan")
# plt.xlabel("Pulse length (us)")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSPulselength.png")
# plt.show() 



##=================================##
#Shift, 171310

# do = data_objects[7][0]
# phase = do.df['transitions.729_MS.shift'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(0.003, c = 'k', linestyle = ':', label = "Chosen shift: 3KHz")
# plt.title("Symmetric shift scan")
# plt.xlabel("Shift")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSShift.png")
# plt.show()



##=================================##
#Phase scan, 180739

# do = data_objects[6][0]
# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(0.4, c = 'k', linestyle = ':', label = "Chosen MS phase: 0.4")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSPhase.png")
# plt.show()



##=================================##
#Parity, 182037

# do = data_objects[4][0]


# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# parity, dparity = do.get_parity(probs, dprobs)

# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 20, vary = True)
# ft.parameters.add("C",  0, vary = True)
# ft.parameters.add("D",  0, vary = False)

# ft.do_minimisation(pulselength, parity)
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# label = "Amplitude: {}({})".format(round(params['A'],2), int(params_error['A']*100))
# ft.plot_fit(pulselength, parity, errorbars = dparity, ax = ax, label = label, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity")
# plt.savefig(save_dir + "Parity.png")
# plt.show() 


##=================================##
#Population, 181434

# do = data_objects[3][0]
# #filter

# do.df.drop(range(84,89), inplace = True)
# do.df.drop(range(176,181), inplace = True)

# probs_1, dprobs_1 = do.get_probs(nmax = 600, thresholds = [30, 120, 200])
# dummy1 = np.array(range(probs_1[:,0].size))

# means = np.mean(probs_1, axis = 0)
# std = np.std(probs_1, axis = 0)/np.sqrt(probs_1[:,0].size)

# print(means, std)

# for k in range(4):
#     lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
#     plot_error_joint(dummy1, probs_1[:,k], dprobs_1[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Long Population Scan", xlabel = "Dummy", ylabel = "Probability", label = lab)

# #def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
# plt.legend()
# plt.savefig(save_dir + "PopScan.png")
# plt.show()




##=================================##
#Limitation investigations

##================##
#MS shifts, heating effect/ 164205, 164813
# pt2 = PlotTemplate((2,1))
# axes = pt2.generate_figure()

# do = data_objects[8][0]
# phase = do.df['transitions.729_MS.shift'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# for k in range(4):
#     axes[0].errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# axes[0].set_title("Symmetric shift scan")
# axes[0].set_xlabel("Shift")
# axes[0].set_ylabel("Probability")
# axes[0].legend()

# do = data_objects[9][0]
# phase = do.df['transitions.729_MS.shift'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# for k in range(4):
#     axes[1].errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# axes[1].set_title("Symmetric shift scan - Sideband cooled")
# axes[1].set_xlabel("Shift")
# axes[1].set_ylabel("Probability")
# axes[1].legend()
# plt.savefig(save_dir + "ShiftCompare.png")
# plt.show()

##================##
#Micromotion comparison, 174147, 174725, 173803, 173636 -> 10...

#==========#
#Parity


# do = data_objects[10][0]
# #filter 
# do.df.drop(range(35,39), inplace = True)
# do.df.drop(range(24,29), inplace = True)


# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# parity, dparity = do.get_parity(probs, dprobs)
# _, dprobs_weight = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# _, dparity_weight = do.get_parity(probs, dprobs_weight)

# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 20, vary = True)
# ft.parameters.add("C",  0, vary = True)
# ft.parameters.add("D",  0, vary = False)

# ft.do_minimisation(pulselength, parity, weights = 1/dparity_weight)
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# label = "Before Correcting Micromotion\nAmplitude: {}0({})".format(round(params['A'],2), int(params_error['A']*100))
# ft.plot_fit(pulselength, parity, errorbars = dparity, ax = ax, label = label, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity" ,colour_index = 0)


# do = data_objects[12][0]
# #filter 
# do.df.drop(range(2,7), inplace = True)


# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# parity, dparity = do.get_parity(probs, dprobs)
# _, dprobs_weight = do.get_probs(nmax = 400, thresholds = [30, 125, 205])
# _, dparity_weight = do.get_parity(probs, dprobs_weight)


# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 20, vary = True)
# ft.parameters.add("C",  0, vary = True)
# ft.parameters.add("D",  0, vary = False)

# ft.do_minimisation(pulselength, parity, weights = 1/dparity_weight)
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# label = "Corrected Micromotion\nAmplitude: {}({})".format(round(params['A'],2), int(params_error['A']*100))
# ft.plot_fit(pulselength, parity, errorbars = dparity, ax = ax, label = label, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity", colour_index = 1)
# plt.savefig(save_dir + "Paritycompare.png")
# plt.show() 

#==========#
#Populations

# pt2 = PlotTemplate((2,1))
# axes = pt2.generate_figure()

# do = data_objects[11][0]
# #filter

# do.df.drop(range(21,25), inplace = True)

# probs_1, dprobs_1 = do.get_probs(nmax = 400, thresholds = [30, 120, 200])
# dummy1 = np.array(range(probs_1[:,0].size))



# means = np.mean(probs_1, axis = 0)
# std = np.std(probs_1, axis = 0)/np.sqrt(probs_1[:,0].size)

# print(means, std)

# for k in range(4):
#     lab =  r"$p_{" + str(k) + r"}$" + ": {:.3f}({}) ".format(round(means[k],3), int(std[k]*1000)) + r"$\sigma: {}$".format(round(std[k]*np.sqrt(probs_1[:,k].size),3))
#     plot_error_joint(dummy1, probs_1[:,k], dprobs_1[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = axes[0], color = pt.colours[k], fill=True, title = "Population Scan: Before Micromotion Compensation", xlabel = "Dummy", ylabel = "Probability", label = lab)

# axes[0].legend()
# axes[0].set_ylim([0,0.7])

# do = data_objects[13][0]
# #filter

# do.df.drop(range(46, 51), inplace = True)

# probs_1, dprobs_1 = do.get_probs(nmax = 400, thresholds = [30, 120, 200])
# dummy1 = np.array(range(probs_1[:,0].size))

# means = np.mean(probs_1, axis = 0)
# std = np.std(probs_1, axis = 0)/np.sqrt(probs_1[:,0].size)

# print(means, std)

# for k in range(4):
#     lab = r"$p_{" + str(k) + r"}$" + ": {:.3f}({}) ".format(round(means[k],3), int(std[k]*1000))+ r"$\sigma: {}$".format(round(std[k]*np.sqrt(probs_1[:,k].size),3))
#     plot_error_joint(dummy1, probs_1[:,k], dprobs_1[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = axes[1], color = pt.colours[k], fill=True, title = "Population Scan: After Micromotion Compensation", xlabel = "Dummy", ylabel = "Probability", label = lab)

# axes[1].legend()
# axes[1].set_ylim([0,0.7])
# plt.savefig(save_dir + "PopScancompare.png")
# plt.show()



##================##
#Lift

