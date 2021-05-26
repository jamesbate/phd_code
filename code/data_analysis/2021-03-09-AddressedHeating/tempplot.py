import numpy as np 
import matplotlib.pyplot as plt 
from stdlib import PhysicalConstants, phonon_to_temp, temp_to_phonon, PlotTemplate, fit_linear, FitTemplate
save_dir = 'C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\phd\\images\\2021-03-09-AddressedHeating\\'
pc = PhysicalConstants() 
freq = 1e6


plot_template = PlotTemplate((1,1))
ax = plot_template.generate_figure()



# #ratios
# raman_pulses = np.array([5, 10,20,30])

# phonons = np.array([0.5,0.7,1.3, 1.7])
# phonon_std = np.array([0.4,0.5, 0.7, 0.8])

# ax.scatter(raman_pulses, phonons, c = 'g', label = "Ratios", s = 50, marker = 's')
# ax.errorbar(raman_pulses, phonons, yerr = phonon_std,ls = 'none', capsize = 3,c='g', marker = 's')


#blue
raman_pulses = np.array([0, 5,10,20,30])
bphonon_upper = np.array([0.2, 0.65,0.9,2.2,2.4])
bphonons = np.array([0.15, 0.49,0.8,1.77, 2.05])
bphonon_lower = np.array([0.1, 0.35,0.6,1.4,1.8])
ax.scatter(raman_pulses, bphonons, c = 'b', label = "BSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, bphonons, yerr = [bphonons - bphonon_lower, bphonon_upper - bphonons],ls = 'none', capsize = 3, c='b', marker = '^')


#red
raman_pulses = np.array([0,5,10,20,30])
rphonon_upper = np.array([0.3,0.65,1,1.9, 4])
rphonons = np.array([0.23,0.61,0.89,1.71,2.99])
rphonon_lower = np.array([0.15,0.5,0.8,1.5, 2])
ax.scatter(raman_pulses, rphonons, c = 'r', label = "RSB", s = 50, marker = '^')
ax.errorbar(raman_pulses, rphonons, yerr = [rphonons - rphonon_lower, rphonon_upper - rphonons],ls = 'none', capsize = 3,c='r', marker = '^')

# a = np.concatenate((rphonons, bphonons, phonons))
a = np.concatenate((rphonons, bphonons))
b = np.concatenate((rphonon_upper, bphonon_upper))
c = np.concatenate((rphonon_lower, bphonon_lower))
d = b - c 
# e = np.concatenate((d,phonon_std ))
e = d
# f = np.concatenate(([0,5,10,20,30],[5,10,20,30],  [5, 10,20,30]))
f = np.concatenate(([0,5,10,20,30],  [0,5, 10,20,30]))

fit = FitTemplate(fit_linear)
fit.parameters.add('A', 0.1, vary = True)
fit.parameters.add('B', 0)
fit.do_minimisation(f, a, weights=1/e)
params = fit.get_opt_parameters()
fit.print_fit_result()
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

plt.savefig(save_dir+'tempvspulses2.png', dpi = 100)
plt.show() 
