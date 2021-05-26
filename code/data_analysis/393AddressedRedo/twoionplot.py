import numpy as np 
import matplotlib.pyplot as plt 
from lib import PhysicalConstants, phonon_to_temp, temp_to_phonon, PlotTemplate, fit_linear, FitTemplate
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/temperature_plots_redo_ampfree/'
pc = PhysicalConstants() 
freq = 1e6


plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure()

raman_pulses = np.array([20,30,40])
phonons = np.array([0.6,0.9,1.1])
phonon_std = np.array([0.1,0.1,0.1])
ax.scatter(raman_pulses, phonons, c = 'g', label = "Ratios", s = 50, marker = 's')
ax.errorbar(raman_pulses, phonons, yerr = phonon_std,ls = 'none', capsize = 3,c='g', marker = 's')

#blue
raman_pulses = np.array([20,40])
bphonon_upper = np.array([0.8,1.2])
bphonons = np.array([0.42,0.91])
bphonon_lower = np.array([0.2,0.7])
ax.scatter(raman_pulses, bphonons, c = 'b', label = "BSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = '^')

#red
raman_pulses = np.array([20,40])
rphonon_upper = np.array([0.6,1.2])
rphonons = np.array([0.42,0.9])
rphonon_lower = np.array([0.25,0.6])
ax.scatter(raman_pulses, rphonons, c = 'r', label = "RSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = '^')

#blue two ion 
raman_pulses = np.array([30])
bphonon_upper = np.array([1])
bphonons = np.array([0.75])
bphonon_lower = np.array([0.4])
#ax.scatter(raman_pulses, bphonons, c = 'b', label = "BSB", s = 20, marker = 'd', markerfacecolor='none')
# ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = 'd', fillstyle = 'none',markersize = 10, label = "BSB 10*2")
ax.scatter(raman_pulses, bphonons, c = 'b', s = 50, marker = '^')
ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = '^')

#red two ion
raman_pulses = np.array([30])
rphonon_upper = np.array([0.9])
rphonons = np.array([0.7])
rphonon_lower = np.array([0.4])
#ax.scatter(raman_pulses, rphonons, c = 'r', label = "RSB", s = 20, marker = 'd', markerfacecolor='none')
# ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = 'd', fillstyle = 'none',markersize = 10, label = "RSB 10*2")
ax.scatter(raman_pulses, rphonons, c = 'r', s = 50, marker = '^')
ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = '^')


# a = np.concatenate((rphonons, bphonons, phonons))
# b = np.concatenate((rphonon_upper, bphonon_upper))
# c = np.concatenate((rphonon_lower, bphonon_lower))
# d = b - c 
# e = np.concatenate((d,phonon_std ))
# f = np.concatenate(([10,20],[10,20],  [10,20]))
ax.get_xaxis().set_visible(False)
plt.title('Ion temperature vs Optical Pumping and Raman pulses')
#plt.xlabel('Pulses')
ax.set_ylabel(r'$\langle n\rangle$')      
plt.legend()   
plt.savefig(save_dir+'tempvspulses_twoions.png', dpi = 100)
plt.show()