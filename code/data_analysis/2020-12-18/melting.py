from lib import TricsDataObject, data_loader
import matplotlib.pyplot as plt
import numpy as np

##----------------------------PARAMETERS----------------------------------##
#data_dir_trics = "zidshare.uibk.ac.at/qos/qfc/measurements/trics_data/"
data_dir_trics = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/data/'
save_dir = 'C:/Users/James/OneDrive - OnTheHub - The University of Oxford/phd/images/trics/'

data_folders = ["2020-12-18/182923/", "2020-12-18/174126/", "2020-12-18/173301/"]
filenames = ["PMT1_1.txt", "PMT1_2.txt"]

savefiles = ['MSGate.png']

##----------------------------MAIN----------------------------------##

plt.rcParams.update({'font.size': 16})
colours = ['b','m','g','c','r','tab:orange', 'tab:pink']
fig, ax = plt.subplots(1	,1, constrained_layout=True, figsize=(18, 9))
plt.grid()


# tdo = data_loader(filenames, data_folders, data_dir_trics)[:,0][0]

# plt.plot(tdo.df['channel.Dummy'].to_numpy(), tdo.df['PMT1_1(sum)'].to_numpy())
# plt.xlabel('Dummy')
# plt.ylabel('Sum of counts')
# plt.show() 

tdo_rabi = data_loader([filenames[1]],[data_folders[1]], data_dir_trics)[0,0]
(probs, dprobs) = tdo_rabi.get_probs(nmax = 180, thresholds = [25, 100])
(me, dme) = tdo_rabi.get_mean_exc(nmax = 180, thresholds = [25, 100])
#tdo_rabi.plot_data_histogram(nmax = 180, thresholds = [25, 100]) 
plt.plot(tdo_rabi.df['seq.MS_pulselength'].to_numpy(),me )
plt.show() 

# tdo_rabi = data_loader([filenames[1]],[data_folders[2]], data_dir_trics)[0,0]
# tdo_rabi.plot_data_histogram(nmax = 100, thresholds = [10, 42]) 
# plt.show() 

# (probs, dprobs) = tdo_rabi.get_probs(nmax = 180, thresholds = [25, 100])
# (me, dme) = tdo_rabi.get_mean_exc(nmax = 100, thresholds = [10, 42])
# # tdo_rabi.plot_data_histogram(nmax = 180, thresholds = [25, 100]) 
# plt.plot(tdo_rabi.df['seq.probe_729_length'].to_numpy(),me )
# plt.show() 