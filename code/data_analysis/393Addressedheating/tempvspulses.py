import numpy as np 
import matplotlib.pyplot as plt 
from stdlib import PhysicalConstants, phonon_to_temp, temp_to_phonon, PlotTemplate, fit_linear, FitTemplate
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/temperature_plots_redo/'
pc = PhysicalConstants() 
freq = 1e6


plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure()


fit_phonons = np.array([0.04,0.6,0.9,1.1,1.4])
fit_phonon_std = np.array([0.08,0.1,0.1,0.1, 0.2])
fit_pulses = np.array([0,10,20,20,40])

# fit = FitTemplate(fit_linear)
# fit.parameters.add('A', 0.1)
# fit.parameters.add('B', 0)
# fit.do_minimisation(fit_pulses, fit_phonons, weights=1/fit_phonon_std)
# params = fit.get_opt_parameters()
# print(fit.fit_result_error_dict)
# ax.plot(np.linspace(0,60,100), fit_linear(np.linspace(0,60,100), params), c = 'g', label = 'fit: Ax + B\nA = {}0 +- 0.004\nB = {} +- 0.07'.format(round(params['A'],3), round(params['B'],2)))


# #ratios
# raman_pulses = np.array([10,20,20,40])

# phonons = np.array([0.6,0.9,1.1,1.4])
# phonon_std = np.array([0.1,0.1,0.1, 0.2])

# ax.scatter(raman_pulses, phonons, c = 'g', label = "Ratios", s = 50, marker = 's')
# ax.errorbar(raman_pulses, phonons, yerr = phonon_std,ls = 'none', capsize = 3,c='g', marker = 's')

#ratios
raman_pulses = np.array([10,20,40])

phonons = np.array([0.5,1.1,1.6])
phonon_std = np.array([0.1,0.1, 0.2])

ax.scatter(raman_pulses, phonons, c = 'g', label = "Ratios", s = 50, marker = 's')
ax.errorbar(raman_pulses, phonons, yerr = phonon_std,ls = 'none', capsize = 3,c='g', marker = 's')


#blue
raman_pulses = np.array([0,10,20,40])
bphonon_upper = np.array([0.1,0.8,1.2,4])
bphonons = np.array([0.04,0.42,0.91, 2])
bphonon_lower = np.array([0.01,0.2,0.7,1.2])
ax.scatter(raman_pulses, bphonons, c = 'b', label = "BSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = '^')


#red
raman_pulses = np.array([10,20,40,60])
rphonon_upper = np.array([0.6,1.2,2.5,5])
rphonons = np.array([0.42,0.9,1.5,2.23])
rphonon_lower = np.array([0.25,0.6,0.8,2])
ax.scatter(raman_pulses, rphonons, c = 'r', label = "RSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = '^')

a = np.concatenate((rphonons, bphonons, phonons))
b = np.concatenate((rphonon_upper, bphonon_upper))
c = np.concatenate((rphonon_lower, bphonon_lower))
d = b - c 
e = np.concatenate((d,phonon_std ))
f = np.concatenate(([10,20,40,60],[0,10,20,40],  [10,20,40]))

fit = FitTemplate(fit_linear)
fit.parameters.add('A', 0.1)
fit.parameters.add('B', 0)
fit.do_minimisation(f, a, weights=1/e)
params = fit.get_opt_parameters()
print(fit.fit_result_error_dict)
ax.plot(np.linspace(0,60,100), fit_linear(np.linspace(0,60,100), params), c = 'g', label = 'fit: Ax + B\nA = {}0 +- 0.004\nB = {} +- 0.07'.format(round(params['A'],3), round(params['B'],2)))

# #average
# raman_pulses = np.array([0,10,20,20,40,60])

# phonons = np.array([0.04]+list(0.5*(bphonons[1:]+rphonons[:-1]))+[3.22])
# phonons_upper = np.array([0.1]+list(0.5*(bphonon_upper[1:]+rphonon_upper[:-1]))+[5])
# phonons_lower = np.array([0.01]+list(0.5*(bphonon_lower[1:]+rphonon_lower[:-1]))+[1.5])

# ax.scatter(raman_pulses, phonons, c = 'purple', label = "Sideband Flops", s = 20)
# ax.errorbar(raman_pulses, phonons, yerr = [phonons - phonons_lower, phonons_upper - phonons],ls = 'none', capsize = 3,c='purple')

# #carrier 
# raman_pulses = np.array([60])
# phonon_upper = np.array([11])
# phonons = np.array([4])
# phonon_lower = np.array([7])
# ax.scatter(raman_pulses, phonons,marker =  'x',c = 'k', label = "Carrier", s = 40)
# ax.errorbar(raman_pulses, phonons,ls = 'none', capsize = 3,c='k')

# #blue two ion 
# raman_pulses = np.array([20])
# bphonon_upper = np.array([1])
# bphonons = np.array([0.75])
# bphonon_lower = np.array([0.4])
# #ax.scatter(raman_pulses, bphonons, c = 'b', label = "BSB", s = 20, marker = 'd', markerfacecolor='none')
# ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = 'd', fillstyle = 'none',markersize = 10, label = "BSB 10*2")


# #red two ion
# raman_pulses = np.array([20])
# rphonon_upper = np.array([0.9])
# rphonons = np.array([0.7])
# rphonon_lower = np.array([0.4])
# #ax.scatter(raman_pulses, rphonons, c = 'r', label = "RSB", s = 20, marker = 'd', markerfacecolor='none')
# ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = 'd', fillstyle = 'none',markersize = 10, label = "RSB 10*2")




# secaxy = ax.secondary_yaxis('right', functions=(phonon_to_temp, temp_to_phonon))
# secaxy.set_ylabel(r'Temperature $(mK)$')





plt.title('Ion temperature vs Raman pulse number')
plt.xlabel('Pulses')
ax.set_ylabel(r'$\langle n\rangle$')      
plt.grid(True)
plt.grid(which='minor', linestyle = '--', alpha = 0.6)  
plt.legend()                                                              
ax2 = ax.twinx() 

ax2.set_ylabel('Temperature (mK)')
ax.set_ylim(0,6)
ax2.set_ylim(0,phonon_to_temp(np.array([6])))

plt.savefig(save_dir+'tempvspulses3.png', dpi = 100)
plt.show() 
