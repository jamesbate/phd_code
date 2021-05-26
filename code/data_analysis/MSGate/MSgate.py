from lib import TricsDataObject, data_loader, plot_error_joint, fit_sinusoid, fit_rabi
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/'

data_folders = ["2020-11-13/183418/", "2020-11-13/193654/", "2020-11-13/193927/", "2020-11-13/182010/", "2020-11-13/171102/", "2020-11-13/171517/", "2020-11-13/152931/"]
filenames = ["PMT1_2.txt"]
filenames_2 = ["camera_all.txt"]

savefiles = ['MSGate.png']


##----------------------------MAIN----------------------------------##

plt.rcParams.update({'font.size': 16})
colours = ['b','m','g','c','r','tab:orange', 'tab:pink']
fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))
plt.grid()


tdo = data_loader(filenames, data_folders, data_dir_trics)[:,0]

##----------------------------------------------------------------------##

#used histograms to find thresholds [9,34]


# for i in range(len(data_folders)):
#     tdo[i].plot_data_histogram([9,34])
#     plt.savefig(save_dir + 'histogram' + str(i) +savefiles[0], dpi = 1000)

##----------------------------------------------------------------------##

# #populations against pulse time plot

# pulse_length = tdo[0].df['seq.MS_pulselength'].to_numpy() 

# (probs, dprobs) = tdo[0].get_probs([9,34])

# labels = [r'$|\uparrow\uparrow\rangle$', r'$|\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle$', r'$|\downarrow\downarrow\rangle$']

# for i in range(3):
#     ax.errorbar(pulse_length, probs[:,i], dprobs[:,i], c = colours[i],ls = 'none', capsize = 3)
#     ax.scatter(pulse_length, probs[:,i], c = colours[i])
#     ax.plot(pulse_length, probs[:,i], c = colours[i], label = labels[i])

# plt.title('Populations against Bichromatic Pulse Time')
# plt.xlabel('Pulse time $(\mu s)$')
# plt.ylabel('Probability')
# plt.legend() 
# plt.savefig(save_dir + savefiles[0], dpi = 1000)
# plt.show() 

##----------------------------------------------------------------------##

# #Populations plot 
# pulse_length = tdo[2].df['channel.Dummy'].to_numpy() 
# (probs, dprobs) = tdo[2].get_probs([9,34])

# #average along columns
# mean_pops = np.mean(probs, axis = 0)
# mean_errors = np.mean(dprobs, axis = 0)

# labels = [r'$|\uparrow\uparrow\rangle$', r'$|\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle$', r'$|\downarrow\downarrow\rangle$']
# for i in range(3):
#     #ax.errorbar(pulse_length, probs[:,i], dprobs[:,i], c = colours[i],ls = 'none', capsize = 3)
#     #ax.scatter(pulse_length, probs[:,i], c = colours[i])
#     ax.plot(pulse_length, probs[:,i], c = colours[i], label = labels[i])
#     #ax.axhline(mean_pops[i], linestyle =  'dotted',c = colours[i])
#     plot_error_joint(pulse_length, probs[:,i], dprobs[:,i], [mean_pops[i]]*pulse_length.size, [mean_pops[i] - mean_errors[i]]*pulse_length.size,[mean_pops[i] + mean_errors[i]]*pulse_length.size,ax = ax, fill = True, color = colours[i], xlabel = 'Dummy', ylabel = 'Probability', title = "Populations")
# plt.savefig(save_dir + 'populations' + savefiles[0], dpi = 1000)
# plt.show() 
# print(mean_pops, mean_errors)

##----------------------------------------------------------------------##

# #Phase Oscillations  
# pulse_length = tdo[1].df['seq.phase_MS'].to_numpy() 
# (probs, dprobs) = tdo[1].get_probs([9,34])
# parity = probs[:,2] + probs[:,0] - probs[:,1]
# dparity = dprobs[:,2] + dprobs[:,0] - dprobs[:,1]

# (popt, pcov) = curve_fit(fit_sinusoid, pulse_length, parity, [1, 2, 0])
# lab = "Amplitude: " + str(round(popt[0],3))
# ax.errorbar(pulse_length, parity, dparity,ls = 'none', capsize = 3, c = 'g')
# ax.scatter(pulse_length, parity, c = 'g')
# fit_domian = np.linspace(0,pulse_length[-1], 500)
# ax.plot(fit_domian, fit_sinusoid(fit_domian, *popt), c = 'g', label = lab)
# ax.set_title('Parity Flops')
# ax.set_xlabel(r'Pulse Length $\mu s$')
# ax.set_ylim([-1,1])
# ax.set_ylabel(r'$\langle\sigma_z^{(1)}\otimes\sigma_z^{(2)}\rangle$')
# plt.legend()
# plt.savefig(save_dir + 'parity' + savefiles[0], dpi = 1000)
# plt.show() 
# print(popt)
# print(np.linalg.eigvals(pcov))

##----------------------------------------------------------------------##

# Finding Symmetric shift offset

#checked thresholds, [9,34]

# freq = tdo[3].df['transitions.729_MS.frequency'].to_numpy()
# (probs, dprobs) = tdo[3].get_probs([9,34])
# labels = [r'$|\uparrow\uparrow\rangle$', r'$|\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle$', r'$|\downarrow\downarrow\rangle$']
# for i in range(3):
#     ax.errorbar(freq, probs[:,i], dprobs[:,i], c = colours[i],ls = 'none', capsize = 3)
#     ax.scatter(freq, probs[:,i], c = colours[i])
#     ax.plot(freq, probs[:,i], c = colours[i], label = labels[i])

# ax.set_title('Centre Line Frequency Scan')
# ax.set_xlabel(r'Frequency AOM $(MHz)$')
# ax.set_ylabel('Probability')
# plt.legend() 
# plt.savefig(save_dir + 'centrescan' + savefiles[0], dpi = 1000)

# plt.show() 

##----------------------------------------------------------------------##

# #pi times 

# pulse_length = tdo[4].df['seq.MS_pulselength'].to_numpy()[5:]
# (probs, dprobs) = tdo[4].get_mean_exc([9,34], indices = list(range(5,50)))
# (probs_2, dprobs_2) = tdo[5].get_mean_exc([9,34], indices = list(range(5,50)))

# #ditch first 5 data points

# initial_fit = [
#     [0.068, 5, 0,2*0.35, 0]
# ]*2


# r = fit_rabi(pulse_length, np.array([probs, probs_2]).T[0], np.array([dprobs, dprobs_2]).T[0], initial_fit, labels = ['+1 Sideband', '-1 Sideband'], p_fix = [[0.068,None,13e-3,None,None]]*2,m = 0, ax = ax)
# print(r)
# plt.savefig(save_dir + 'pitime' + savefiles[0], dpi = 1000)
# plt.show() 

##----------------------------------------------------------------------##

# #Camera flops - setting DC 

# tdo = data_loader(filenames_2, [data_folders[6]], data_dir_trics,1)[0,0]
# tdo_pd =  data_loader(filenames, [data_folders[6]], data_dir_trics,1)[0,0]

# scan_point = tdo.df['# scan point']
# probs = tdo.get_data(reshape = False) 
# pulse_length = tdo_pd.df['seq.probe_729_length'].to_numpy() 
# initial_fit = [
#     [0.068, 0, 0,1, 0]
# ]*2
# r = fit_rabi(pulse_length, np.array([probs[:,0], probs[:,1]]).T, np.array([[None, None]]), initial_fit, labels = [None,None],p_fix = [[0.068,None,0,None,None]]*2,m = 0, ax = ax)
# ax.set_title("Carrier Flops - Camera")
# ax.set_xlabel(r'Pulse Length $(\mu s)$')
# ax.set_ylabel('Probability')
# plt.savefig(save_dir + 'cameraflops' + savefiles[0], dpi = 1000)
