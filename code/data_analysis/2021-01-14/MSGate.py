from stdlib import TricsDataObject, data_loader, PlotTemplate, plot_histogram, FitTemplate, fit_sinusoid, plot_error_joint, full_Rabi, fit_lorentzian
import matplotlib.pyplot as plt
import numpy as np

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/2021-01-14/'

data_folders = ["2021-01-14/114547/", "2021-01-14/121327/", "2021-01-14/155320/", "2021-01-14/155431/", "2021-01-14/163350/", "2021-01-14/164249/", "2021-01-14/165005/", "2021-01-14/155807/", "2021-01-14/112211/"]
filenames = ["PMT1_2.txt"]

savefiles = ['MSGate.png']

##----------------------------MAIN----------------------------------##

plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure() 

data_obj = data_loader(filenames, data_folders, data_dir_trics)[:,0]

##------------------FULL GATE----------------------##
# do = data_obj[7]
# mspulselength = do.df['seq.MS_pulselength']
# #do.plot_data_histogram(ax = ax, nmax = 300, thresholds = [50,160])
# (probs, dprobs) = do.get_probs(thresholds = [50,160], nmax = 300)
# #plt.plot(mspulselength, probs)
# ax.errorbar(mspulselength, probs[:,2], dprobs[:,2], capsize = 3, label = r'$P_{\downarrow\downarrow}$')
# ax.errorbar(mspulselength, probs[:,1], dprobs[:,1], capsize = 3, label = r'$P_{\downarrow\uparrow},P_{\uparrow\downarrow}$')
# ax.errorbar(mspulselength, probs[:,0], dprobs[:,0], capsize = 3, label = r'$P_{\uparrow\uparrow}$')
# plt.title('Bichromatic pulse length scan')
# plt.xlabel('Pulse time (us)')
# plt.ylabel('Probability')
# plt.legend()
# plt.savefig(save_dir+'MSPulseLengthScan.png', dpi = 100)
# plt.show()

##------------------PARITY----------------------##

# #data
# do = data_obj[5]
# phase = do.df['seq.phase_MS'].to_numpy()
# (probs, dprobs) = do.get_probs(thresholds = [50, 160], nmax = 300)
# parity = probs[:,2] + probs[:,0] - probs[:,1]
# dparity = np.sqrt(dprobs[:,2]**2 + dprobs[:,0]**2 + dprobs[:,1]**2)

# #fit
# ft = FitTemplate(fit_sinusoid)
# #parameters 
# ft.parameters.add('A', 1, vary = True)
# ft.parameters.add('B', 3, vary = True)
# ft.parameters.add('C', -1.5, vary = True)
# ft.parameters.add('D', 0, vary = True)


# fit_results = ft.do_minimisation(phase, parity, weights = 1/dparity)
# ft.print_fit_result()
# #plot
# label = 'Amplitude: 0.982(13)'
# ft.plot_fit(phase, parity, errorbars = dparity, ax = ax, xlabel = 'Phase', ylabel = 'Parity', title = 'Parity', label = label)
# #plt.savefig(save_dir+'Parity.png', dpi = 100)
# plt.show()

##------------------POPULATIONS----------------------##

#data 
do = data_obj[4]
dummy = do.df['channel.Dummy'].to_numpy() 
(probs, dprobs) = do.get_probs(thresholds = [50,160], nmax = 350, allow_zero_error = False)
#extract means 
means = np.average(probs, axis = 0, weights = 1/dprobs)
#means = np.average(probs, axis = 0)
cycles = probs.shape[1]
std = np.std(probs, axis = 0)/np.sqrt(cycles)
print('Means: {}, Std: {}'.format(means, std))
#plot
plot_error_joint(dummy, probs[:,0], dprobs[:,0], 0*dummy + means[0], dummy*0 + means[0] - std[0], 0*dummy + means[0] + std[0], ax = ax, fill = True, color = 'b', xlabel='Dummy', ylabel='Probability', title = 'Populations', label = r'$P_{\uparrow\uparrow}$ = 0.489(13)')
plot_error_joint(dummy, probs[:,1], dprobs[:,1], 0*dummy + means[1], dummy*0 + means[1] - std[1], 0*dummy + means[1] + std[1], ax = ax, fill = True, color = 'g', xlabel='Dummy', ylabel='Probability', title = 'Populations', label = r'$P_{\downarrow\uparrow},P_{\uparrow\downarrow}$ = 0.007(3)')
plot_error_joint(dummy, probs[:,2], dprobs[:,2], 0*dummy + means[2], dummy*0 + means[2] - std[2], 0*dummy + means[2] + std[2], ax = ax, fill = True, color = 'm', xlabel='Dummy', ylabel='Probability', title = 'Populations', label = r'$P_{\downarrow\downarrow}$ = 0.501(13)')
#plt.savefig(save_dir+'MSPopulations.png', dpi = 100)
print(np.std((probs[:,0]+probs[:,2])/1)/np.sqrt(probs[:,2].size))
plt.show()

##------------------CARRIER----------------------##

# #data 
# do = data_obj[0]
# pulselength = do.df['seq.probe_729_length'].to_numpy() 
# # do.plot_data_histogram(ax = ax, nmax = 300, thresholds = [50,145])
# # plt.show()
# # exit()
# (me, dme) = do.get_mean_exc(thresholds = [50, 145], nmax = 300)

# #fit 
# ft = FitTemplate(full_Rabi)
# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 1, vary = True)
# ft.parameters.add('Rabi', 1.5, vary = True)
# ft.parameters.add('phase', 0, vary = True)


# #plot 
# ft.do_minimisation(pulselength, me[:,np.newaxis])
# ft.print_fit_result()
# label = r'$Rabi: 1.407(3)MHz$'+'\n'+r'$\langle n\rangle: 15(1)$'
# ft.plot_fit(pulselength, me, errorbars = dme, ax = ax, xlabel = 'Pulse Length (us)', ylabel = 'Mean Excitation', title = 'Carrier Flops', label = label)
# #plt.savefig(save_dir+'Carrier.png', dpi = 100)
# plt.show()

##------------------CARRIER SIDEBAND COOLING----------------------##

# #data 
# do = data_obj[1]
# pulselength = do.df['seq.probe_729_length'].to_numpy() 
# # do.plot_data_histogram(ax = ax, nmax = 300, thresholds = [50,145])
# (me, dme) = do.get_mean_exc(thresholds = [50, 145], nmax = 300)

# #fit 
# ft = FitTemplate(full_Rabi)
# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 7, vary = False)
# ft.parameters.add('Rabi', 1.4, vary = True)
# ft.parameters.add('phase', 0, vary = True)

# #plot 
# ft.do_minimisation(pulselength, me[:,np.newaxis], weights = 1/dme)
# ft.print_fit_result()
# label = r'$Rabi: 1.551(5)MHz$'+'\n'+r'$\langle n\rangle: 7(2)$'
# ft.plot_fit(pulselength, me, errorbars = dme, ax = ax, xlabel = 'Pulse Length (us)', ylabel = 'Mean Excitation', title = 'Carrier Flops', label = label)
# plt.savefig(save_dir+'CarrierSidebandCool.png', dpi = 100)
# plt.show()


##------------------BICHRO FLOPS----------------------##

# #REMOVE FIRST 5 POINTS

# #data 
# do = data_obj[2]
# do.df = do.df.iloc[2:]
# pulselength = do.df['seq.MS_pulselength'].to_numpy() 
# #do.plot_data_histogram(ax = ax, nmax = 300, thresholds = [50,175])
# (me, dme) = do.get_mean_exc(thresholds = [50, 175], nmax = 300)

# #fit 
# ft = FitTemplate(full_Rabi)
# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 1, vary = True)
# ft.parameters.add('Rabi', 0.5, vary = True)
# ft.parameters.add('phase', 0, vary = True)

# #plot 
# ft.do_minimisation(pulselength, me[:,np.newaxis])
# ft.print_fit_result()
# label = 'RSB: ' + r'$t_{\pi/2} = 4.69\mu s$'
# ft.plot_fit(pulselength, me, errorbars = dme, ax = ax, xlabel = 'Pulse Length (us)', ylabel = 'Mean Excitation', label = label, c = 'b')

# #data 
# do = data_obj[3]
# do.df = do.df.iloc[2:]
# pulselength = do.df['seq.MS_pulselength'].to_numpy() 
# # do.plot_data_histogram(ax = ax, nmax = 300, thresholds = [50,145])
# (me, dme) = do.get_mean_exc(thresholds = [50, 175], nmax = 300)

# #fit 
# ft = FitTemplate(full_Rabi)
# #set parameters 
# ft.parameters.add('dicke_factor', 0.049, vary = False)
# ft.parameters.add('detuning', 0, vary = False)
# ft.parameters.add('amplitude', 1, vary = False)

# #free parameters
# ft.parameters.add('n_av', 1, vary = True)
# ft.parameters.add('Rabi', 0.5, vary = True)
# ft.parameters.add('phase', 0, vary = True)

# #plot 
# ft.do_minimisation(pulselength, me[:,np.newaxis])
# ft.print_fit_result()
# label = 'BSB: ' + r'$t_{\pi/2} = 4.60\mu s$'
# ft.plot_fit(pulselength, me, errorbars = dme, ax = ax, xlabel = 'Pulse Length (us)', ylabel = 'Mean Excitation',  title = 'Bichromat Carrier Flops',label = label, c = 'm')
# plt.savefig(save_dir+'CarrierBichromat.png', dpi = 100)

# plt.show()

##------------------RAMSEY----------------------##

# #data 
# do = data_obj[6]
# pulselength = do.df['seq.phase_ramsey'].to_numpy() 
# (me, dme) = do.get_mean_exc(thresholds = [50, 175], nmax = 300)

# #fit 
# ft = FitTemplate(fit_sinusoid)
# #parameters 
# ft.parameters.add('A', 0.5, vary = True)
# ft.parameters.add('D', 0.5, vary = False)
# ft.parameters.add('B', 1.5)


# #plot 
# ft.do_minimisation(pulselength, me)
# params = ft.get_opt_parameters()
# ft.print_fit_result()
# label = 'Contrast: {}'.format(round(params['A'],3)/0.5)
# ft.plot_fit(pulselength, me, errorbars = dme, ax = ax, xlabel = 'Relative Phase'+r'$(4/\pi)$', ylabel = 'Mean Excitation',  title = 'Ramsey Flops (100us wait time)',label = label, c = 'b')
# plt.savefig(save_dir+'Ramsey.png', dpi = 100)
# plt.show()

##------------------CARRIER SPECTRUM----------------------##

# #data 
# do = data_obj[8]
# freq = do.df['transitions.729_Probe.frequency'].to_numpy()
# #do.plot_data_histogram(thresholds = [50, 150], nmax = 300)

# me,dme = do.get_mean_exc(thresholds = [50,150], nmax = 300)

# #fit 
# ft = FitTemplate(fit_lorentzian)

# ft.parameters.add('x_0', 444.295, vary = True)
# ft.parameters.add('Gamma', 0.014, vary = True)
# ft.parameters.add('A', 0.008, vary = True)

# ft.do_minimisation(freq, me)
# ft.print_fit_result()
# label = 'Centre: 444.29186(8)MHz'
# ft.plot_fit(freq, me, errorbars = dme, ax = ax, xlabel = 'AOM frequency', ylabel = 'Mean Excitation',  title = 'Carrier Spectrum',label = label, c = 'g')
# plt.savefig(save_dir+'Spectrum.png', dpi = 100)
# plt.show()