from lib import TricsDataObject, data_loader, plot_error_joint, fit_sinusoid, fit_rabi, PlotTemplate, FitTemplate, full_Rabi
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit 

##----------------------------PARAMETERS----------------------------------##
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/'

data_folders = ["2020-12-10-ms/173322/"]
filenames = ["PMT1_2.txt"]
savefiles = ['MSGate.png']

plot_temp = PlotTemplate((1,1))
ax = plot_temp.generate_figure() 
##----------------------------MAIN----------------------------------##

dat = data_loader(filenames,data_folders,data_dir_trics)[0][0]
#dat.plot_data_histogram(thresholds = (25, 90), nmax = 180)


(p, dp) = dat.get_probs(thresholds = (25, 90), nmax = 180)
pulse_length = dat.df['seq.MS_pulselength']

for i in range(3):
    ax.errorbar(pulse_length, p[:,i], dp[:,i], c = plot_temp.colours[i])
    ax.plot(pulse_length, p[:,i], label = "p"+str(i), c = plot_temp.colours[i])
plt.legend() 
plt.show()