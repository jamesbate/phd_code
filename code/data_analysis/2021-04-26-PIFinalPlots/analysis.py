import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from stdlib import PlotTemplate

pt = PlotTemplate((1,1))
ax = pt.generate_figure()


data = pd.read_csv("C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\data\\Lasers\\2021-04-26-PIDataForPost\\data3_413Sync.txt",delimiter = "\t", skiprows = range(17))


time = data['Time [s]']
t1 = data['Temperature[C]']
t2 = data['TH1[C]']
t3 = data['TH2[C]']

# plt.plot(time, t1)
# plt.plot(time, t2)
# plt.plot(time, t3)
# plt.show()

##---------------------------------------------------------##
#Temp synced with wavelength
# print(time.shape)

# low = 5131 - 2760

# time = time[low:]
# t1 = t1[low:]
# t2 = t2[low:]
# t3 = t3[low:]

# ax.plot(time, t1)
# ax.plot(time, t2)
# ax.plot(time, t3)
# plt.xlabel("Time (s)")
# plt.ylabel("Temperature (C)")
# plt.show()


##---------------------------------------------------------##
#Temp sync coupling 413

# low = 0
# upp = 2200

# time = time[low:upp]
# t1 = t1[low:upp]
# t2 = t2[low:upp]
# t3 = t3[low:upp]

# plt.plot(time, t1)
# plt.plot(time, t2)
# plt.plot(time, t3)

# plt.xlabel("Time (s)")
# plt.ylabel("Temperature (C)")
# plt.show()


##-----------------------------------------------##
#fibre coupling plot

data = pd.read_csv("C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\data\\Lasers\\2021-04-26-PIDataForPost\\DLProCoupingBetter.txt",delimiter = "\t", skiprows = range(14))

p = data[' 4/21/2021'].to_numpy(dtype = str)

p = [1e2*float("0." + st) for st in p]

ax.plot(p)
plt.ylabel("Power (mW)")
plt.xlabel("Time (s)")
plt.title("413 Fibre Coupling Power Stability - 18 Hours")
plt.show()