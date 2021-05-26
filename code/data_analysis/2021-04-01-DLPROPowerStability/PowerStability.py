from stdlib import PlotTemplate
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\Images\\PILasersNewSetup\\" 

# data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\DLPRO413LongPower.csv", "\t", skiprows = [0,2,3])
data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\DLPRO413LongPowerNewLab.csv", "\t", skiprows = [0,2,3])
time = data['time unit [ms]']
power = data['value unit [W]']
time.drop(range(132424, 132514), inplace = True)  
power.drop(range(132424, 132514)    , inplace = True)


power *= 1e3

m = round(np.mean(power),3)
st = round(np.std(power[100:]),3)

ax.plot(time[0:200]*1e-3/60, power[0:200], label = "Mean: {}\nStd: {}".format(m, st))
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Power (mW)")
# ax.set_title("413 DLPro - 3 Hour Power Stability")
ax.set_title("413 DLPro - 11 Hour Power Stability")
# plt.savefig(savedir + "PowerStabilityPlot.png")

plt.legend()
#plt.savefig(savedir + "PowerStabilityDLPRONewLab.png")
plt.show()