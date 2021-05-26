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

data_dir = "X:\\measurements\\trics_data\\2021-03-02\\"
save_dir = "C:\\Users\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-03-02-GHZ\\"

folders = ["123152/", "122825/", "124211/", "125050/", "152059/", "152505/", "152737/", "154905/", "155126/", "154727/", "161528/", "160928/", "160645/", "182930/"]
filenames = ["PMT1_2.txt"]

data_objects = data_loader(filenames, folders, data_dir)
#PMT data objects

filenames_cam = ["camera_all.txt", "camera_ion1.txt", "camera_ion2.txt", "camera_ion3.txt"]
folders_cam = ["123152/", "122825/", "124211/", "125050/", "152059/", "152505/", "152737/", "154905/","155126/", "154727/", "161528/", "160928/", "160645/", "182930/"]

data_objects_cam = data_loader(filenames_cam, folders_cam, data_dir, data_column=1)

pt = PlotTemplate((1,1))
ax = pt.generate_figure()
##------------------ANALYSIS--------------------##

##================================##
#Carrier flops with sideband cooling, 123152

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
#     ft.parameters.add('n_av',15, vary = False)
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

##================================##
#Carrier flops, NO SIDEBAND COOLING, closeup at 1 to see detuning, 122825

# do_cam = data_objects_cam[1][0]
# do_pmt = data_objects[1][0]
# #PMT thresholds: nmax = 600, thresholds = [50, 230, 350]

# # do.df.drop(range(52,60), inplace = True)
# # #do_singleion.df.drop(range(52,60), inplace = True)
# # do_pmt.df.drop(range(52,60), inplace = True)

# probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do_pmt.df.shape[1] 
# pulselength = do_pmt.df['seq.probe_729_length'].to_numpy()
# dp = do_cam.projection_uncertainty(probs, cycles)
# dp_weights = do_cam.projection_uncertainty(probs, cycles, allow_zero_error = False)


# for j in range(3):

#     ft = FitTemplate(full_Rabi)
#     #set parameters 
#     ft.parameters.add('dicke_factor', 0.042, vary = False)
#     ft.parameters.add('detuning', 0.1, vary = True)
#     ft.parameters.add('amplitude', 1, vary = False)

#     #free parameters
#     ft.parameters.add('n_av',15, vary = False)
#     ft.parameters.add('Rabi', 1.5, vary = True)
#     ft.parameters.add('phase', 0, vary = False)

#     ft.do_minimisation(pulselength, probs[:,j], weights=1/dp_weights[:,j])
#     ft.print_fit_result()

#     params = ft.get_opt_parameters()
#     params_err = ft.fit_result_error_dict

#     lab = r"$\Omega: {}$".format(round(params['Rabi'],2))+"MHz\n" + r"$\Delta: {}MHz$".format(round(params['detuning'],3))

#     ft.plot_fit(pulselength, probs[:,j], errorbars = dp[:,j], ax = ax, colour_index=j, title = "Camera Rabi Flops", xlabel = "Time (us)", ylabel = "Probability", label = lab)

# plt.savefig(save_dir + "CameraSidebandCooledFlopsZoomed.png")
# plt.show()

# exit()  




##=================================##
#Bichro flops, 124211, 125050

# do_BSB = data_objects[2][0]
# do_BSB.df = do_BSB.df[:40]

# probs,dprobs = do_BSB.get_probs(nmax = 600, thresholds = [50, 230, 350])
# me_BSB, dme_BSB = do_BSB.get_mean_exc(nmax = 600, thresholds = [50, 230, 350])
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
# ft.plot_fit(pulselength, me_BSB, errorbars = dme_BSB, ax = ax, colour_index=0, label = r"$\Omega: {}MHz$".format("0.611(3)")+ "\n" + r"$t_\pi: {}\mu s$".format("5.14(2)"))

# #Now RSB 

# do_RSB = data_objects[3][0]
# do_RSB.df = do_RSB.df[:40]
# #do_RSB.plot_data_histogram(thresholds = [25,105,175],nmax = 400, ax = ax)
# #thresholds = [25,105,175] from histograms

# probs,dprobs = do_RSB.get_probs(nmax = 600, thresholds = [50, 230, 350])
# me_RSB, dme_RSB = do_RSB.get_mean_exc(nmax = 600, thresholds = [50, 230, 350])
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
# ft.plot_fit(pulselength, me_RSB, errorbars = dme_RSB, ax = ax, colour_index = 1, label = r"$\Omega: {}MHz$".format("0.591(2)") + "\n" + r"$t_\pi: {}\mu s$".format("5.32(2)"), title = "Bichro Rabi Flops", xlabel = "Pulse Length (us)", ylabel = "Mean Excitation")
# plt.savefig(save_dir + "BichroFlops.png")
# plt.show()

# exit()


##=================================##
#Best MS gate pulselength, 152059

# do = data_objects[4][0]

# pulselength = do.df['seq.MS_pulselength'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
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
#Shift (0?), 152505

# do = data_objects[5][0]
# phase = do.df['transitions.729_MS.shift'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# plt.title("Symmetric shift scan")
# plt.xlabel("Shift")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSShift.png")
# plt.show()



##=================================##
#Phase scan, 152737, NEED TO DO MORE OF THESE

# do = data_objects[6][0]
# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(1.3, c = 'k', linestyle = ':', label = "Chosen MS phase: 1.3")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSPhase.png")
# plt.show()

##=================================##
#Phase scan, 154727, NEED TO DO MORE OF THESE

# do = data_objects[9][0]
# phase = do.df['seq.phase_MS'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# for k in range(4):
#     ax.errorbar(phase, probs[:,k], dprobs[:,k], linestyle = '-', capsize = 3, label = r"$p_{"+str(k)+r"}$")
# ax.axvline(0.9, c = 'k', linestyle = ':', label = "Chosen MS phase: 0.9")
# plt.title("MS Phase scan")
# plt.xlabel("MS Phase")
# plt.ylabel("Probability")
# plt.legend()
# plt.savefig(save_dir + "MSPhase2.png")
# plt.show()



##=================================##
#Parity, 154905

# do = data_objects[7][0]

# do.df = do.df[:40]

# pulselength = 0.25*do.df['seq.phase_parity'].to_numpy()
# probs, dprobs = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# parity, dparity = do.get_parity(probs, dprobs)

# #fit 
# ft = FitTemplate(fit_sinusoid)

# ft.parameters.add("A", 0.8, vary = True)
# ft.parameters.add("B", 20, vary = True)
# ft.parameters.add("C",  0, vary = True)
# ft.parameters.add("D",  0, vary = False)

# ft.do_minimisation(pulselength, parity, weights = 1/dparity)
# ft.print_fit_result()
# params = ft.get_opt_parameters()
# params_error = ft.fit_result_error_dict
# label = "Amplitude: {}0({})\nFrequency: {}".format(round(params['A'],2), int(params_error['A']*100),round(params['B']/(np.pi),2))
# ft.plot_fit(pulselength, parity, errorbars = dparity, ax = ax, label = label, title = "Parity Flops", xlabel = "Phase"+r"$/\pi$", ylabel = "Parity")
# plt.savefig(save_dir + "Parity.png")
# plt.show() 


##=================================##
#Population, 155126

# do = data_objects[8][0]

# do.df = do.df[:80]


# probs_1, dprobs_1 = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
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
#Ramsey stuff?
##============##
#Population scan 0us,160928

# do = data_objects[10][0]
# do_cam = data_objects_cam[10][0]

# # do.df = do.df[:80]
# # do_cam.df = do_cam.df[:80]


# probs_1, dprobs_1 = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# dummy1 = np.array(range(probs_1[:,0].size))


# probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do.df.shape[1] 
# pulselength = do.df['channel.Dummy'].to_numpy()
# dp = do_cam.projection_uncertainty(probs, cycles)
# dp_weights = do_cam.projection_uncertainty(probs, cycles, allow_zero_error = False)

# means = np.mean(probs, axis = 0)
# std = np.std(probs, axis = 0)/np.sqrt(probs[:,0].size)

# print(means, std)

# for k in range(3):
#     lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
#     plot_error_joint(dummy1, probs[:,k], dp[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Ramsey Population Scan - 0us wait time, Camera", xlabel = "Dummy", ylabel = "Probability", label = lab)

# #def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
# plt.legend()
# plt.ylim([0.8,1])
# #plt.savefig(save_dir + "PopScan_Ramsey0.png")
# plt.show()

##============##
#Population scan 200us,  161528

# do = data_objects[11][0]
# do_cam = data_objects_cam[11][0]

# # do.df = do.df[:80]
# # do_cam.df = do_cam.df[:80]


# probs_1, dprobs_1 = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
# dummy1 = np.array(range(probs_1[:,0].size))


# probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do.df.shape[1] 
# pulselength = do.df['channel.Dummy'].to_numpy()
# dp = do_cam.projection_uncertainty(probs, cycles)
# dp_weights = do_cam.projection_uncertainty(probs, cycles, allow_zero_error = False)

# means = np.mean(probs, axis = 0)
# std = np.std(probs, axis = 0)/np.sqrt(probs[:,0].size)

# print(means, std)

# for k in range(3):
#     lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
#     plot_error_joint(dummy1, probs[:,k], dp[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Ramsey Population Scan - 200us wait time, Camera", xlabel = "Dummy", ylabel = "Probability", label = lab)

# #def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
# plt.legend()
# plt.ylim([0.8,1])
# plt.savefig(save_dir + "PopScan_Ramsey200.png")
# plt.show()

##==================##
#Ramsey Fringes, 200us, 160645

# do_cam = data_objects_cam[12][0]
# do_pmt = data_objects[12][0]

# do_cam.df = do_cam.df[:-5]
# do_pmt.df = do_pmt.df[:-5]

# probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
# cycles = do_pmt.df.shape[1] 
# pulselength = do_pmt.df['seq.phase_ramsey'].to_numpy()
# dp = do_cam.projection_uncertainty(probs, cycles)
# dp_weights = do_cam.projection_uncertainty(probs, cycles, allow_zero_error = False)


# for j in range(3):

#     ft = FitTemplate(fit_sinusoid)
#     #set parameters 
#     ft.parameters.add('A', 0.4, vary = True)
#     ft.parameters.add('B', 0.5, vary = True)
#     ft.parameters.add('C', 1, vary = True)
#     ft.parameters.add('D',0.5, vary = True)

#     ft.do_minimisation(pulselength, probs[:,j], weights=1/dp_weights[:,j])
#     ft.print_fit_result()

#     params = ft.get_opt_parameters()
#     params_err = ft.fit_result_error_dict

#     #lab = r"$\Omega: {}$".format(round(params['Rabi'],2))+"MHz\n" + r"$\Delta: {}MHz$".format(round(params['detuning'],3))
#     lab = ''

#     ft.plot_fit(pulselength, probs[:,j], errorbars = dp[:,j], ax = ax, colour_index=j, title = "Camera Rabi Flops", xlabel = "Time (us)", ylabel = "Probability", label = lab)

# plt.savefig(save_dir + "RamseyFringe200.png")
# plt.show()

# exit()  

##=================================##
#Population drifting? Viktor plots, compare to Ramsey, 182930

do = data_objects[13][0]
do_cam = data_objects_cam[13][0]

do.df = do.df[2:]
do_cam.df = do_cam.df[2:]

#remove smaller than 0.8


probs_1, dprobs_1 = do.get_probs(nmax = 600, thresholds = [50, 230, 350])
dummy1 = np.array(range(probs_1[:,0].size))


probs = do_cam.df[['ion1', 'ion2','ion3']].to_numpy()
cycles = do.df.shape[1] 
pulselength = do.df['seq.phase_MS'].to_numpy()
dp = do_cam.projection_uncertainty(probs, cycles)
dp_weights = do_cam.projection_uncertainty(probs, cycles, allow_zero_error = False)

means = np.mean(probs, axis = 0)
std = np.std(probs, axis = 0)/np.sqrt(probs[:,0].size)

print(probs)

print(means, std)

for k in range(3):
    lab = r"$p_{" + str(k) + r"}$" + ":\t{:.3f}({})".format(round(means[k],3), int(std[k]*1000))
    plot_error_joint(dummy1, probs[:,k], dp[:,k], dummy1*0+means[k], dummy1*0+means[k]+std[k], dummy1*0+means[k]-std[k], ax = ax, color = pt.colours[k], fill=True, title = "Ramsey Population Scan - 0us wait time, Camera", xlabel = "Dummy", ylabel = "Probability", label = lab)

#def plot_error_joint(x, y, dy,y_0,y_1, y_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
plt.legend()
#plt.ylim([0.8,1])
#plt.savefig(save_dir + "PopScan_Ramsey200Vik.png")
plt.show()

