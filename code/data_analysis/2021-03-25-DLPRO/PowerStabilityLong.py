from stdlib import PlotTemplate
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\" 

# data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\DLPRO413LongPower.csv", "\t", skiprows = [0,2,3])
data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\IBEAM375LongPower.csv", "\t", skiprows = [0,2,3])
time = data['time unit [ms]']
power = data['value unit [W]']
time.drop([34039], inplace = True)
power.drop([34039], inplace = True)


power *= 1e3

m = round(np.mean(power),3)
st = round(np.std(power),3)

ax.plot(time[100:36000]*1e-3/60, power[100:36000], label = "Mean: {}\nStd: {}".format(m, st))
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Power (mW)")
# ax.set_title("413 DLPro - 3 Hour Power Stability")
ax.set_title("375 IBEAM - 16 Hour Power Stability")
# plt.savefig(savedir + "PowerStabilityPlot.png")

plt.legend()
#plt.savefig(savedir + "PowerStabilityPlotIBEAM.png")
plt.show()