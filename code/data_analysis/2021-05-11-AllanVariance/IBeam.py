from stdlib import PlotTemplate, allan_variance
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\" 
data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\docs\\PILasers\\IBEAM375LongPower.csv", "\t", skiprows = [0,2,3])
time = data['time unit [ms]']
power = data['value unit [W]']
time.drop([34039], inplace = True)
power.drop([34039], inplace = True)
power *= 1e3
time *=1e-3/60

m = round(np.mean(power),3)
st = round(np.std(power),3)

av = []
tt = []
for k in [1e4, 2e4, 4e4, 6e4, 8e4, 10e4, 12e4,14e4, 15e4, 16e4, 17e4, 18e4, 18.5e4]:
    al_var, time_2, power_2, td= allan_variance(time.to_numpy(), power.to_numpy(),int(k))
    av += [al_var]
    tt += [td]
    print(len(power_2))
print(av, tt)
ax.plot(tt, av)
plt.show()
exit()

ax.plot(time, power, label = "Allan Variancd: {}\nTime Bin: {}".format(al_var, td))


ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Power (mW)")
ax.set_title("375 IBEAM - 16 Hour Power Stability")
plt.legend()
#plt.savefig(savedir + "PowerStabilityPlotIBEAM.png")
plt.show()