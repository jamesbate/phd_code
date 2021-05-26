"""First attempt at GHZ states with Viktor
"""
##------------------PREAMBLE-------------------##
from stdlib import data_loader
#data handling

from stdlib import FitTemplate, fit_lorentzian
#fitting 

from stdlib import PlotTemplate
#plotting

import numpy as np 
import matplotlib.pyplot as plt
#packages

##------------------PARAMETERS--------------------##

data_dir = "X:\\measurements\\trics_data\\2021-02-24\\"
savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-02-24-Wavepacket\\"

folders = ["151615/", "151912/"]
filenames = ["APD1.txt", "APD2.txt"]

data_objects = data_loader(filenames, folders, data_dir, data_column=1)
#PMT data objects

pt = PlotTemplate((1,1))
ax = pt.generate_figure()
##------------------ANALYSIS--------------------##

##=================##
#Rabi frequency extraction

d1 = data_objects[0][1]

freq1 = d1.df['transitions.DP_393_3.frequency']
probs1 = d1.df[' APD(sum)']

ax.plot(freq1, probs1, c = pt.colours[0])

d3 = data_objects[1][1]
d3.df = d3.df.iloc[range(40, 60)]

freq3 = d3.df['transitions.DP_393_3.frequency']
probs3 = d3.df[' APD(sum)']

# plt.plot(probs3)
# plt.show()
# exit()

ax.plot(freq3, probs3, c = pt.colours[1])

probs1 = probs1.to_numpy()
freq1 = freq1.to_numpy()
probs3 = probs3.to_numpy()
freq3 = freq3.to_numpy()

ft = FitTemplate(fit_lorentzian)
ft.parameters.add("A", 0.01)
ft.parameters.add("Gamma", 0.1)
ft.parameters.add("x_0", 324)
ft.do_minimisation(freq1, probs1)
ft.print_fit_result()
params = ft.get_opt_parameters()
ft.plot_fit(freq1, probs1, ax = ax,  c = pt.colours[0], label = "High Power {}".format(round(params['x_0'],2)))

ft.do_minimisation(freq3, probs3)
ft.print_fit_result()
params = ft.get_opt_parameters()
ft.plot_fit(freq3, probs3, ax = ax,  c = pt.colours[1], label = "Low Power {}".format(round(params['x_0'],2)))

ax.set_title("Raman Spectrum")
ax.set_xlabel("Frequency")
ax.set_ylabel("Photon Probability")
plt.savefig(savedir + "RamanSpectrum.png")
plt.show()