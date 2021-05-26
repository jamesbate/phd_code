from stdlib import PlotTemplate
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def time_parser(time_string, date_string, start_day):
    date_list = list(map(float,date_string.split('/')))
    day = date_list[1]

    time_list = list(map(float,time_string.split(':')))
    hours = time_list[0]
    hours += time_list[1]/60
    hours += time_list[2]/(24*60)
    
    hours += 24*(day - start_day)
    return hours
    

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\Images\\PILasersNewSetup\\" 

# data = pd.read_csv("C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\Lasers\\17-04-2021-413DLProPowerStabilityLong\\DLProLongPower.csv", ";", skiprows = range(14))
# data2 = pd.read_csv("C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\Lasers\\17-04-2021-413DLProPowerStabilityLong\\DLProLongPower.csv", ",", skiprows = range(15))
data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\Lasers\\18-04-2021-HeNePowerStabilityLong\\HeNePowerLong.csv", ";", skiprows = range(14))
data2 = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\Lasers\\18-04-2021-HeNePowerStabilityLong\\HeNePowerLong.csv", ",", skiprows = range(15))
data.drop([0], inplace = True)

# time = data['Time of day (hh:mm:ss) ']
time = data['Samples '].to_numpy()
power = data2.iloc[:,1].to_numpy()
date = data['Date (MM/dd/yyyy) ']
# time.drop(range(132424, 132514), inplace = True)  
# power.drop(range(132424, 132514)    , inplace = True)
#temp solution to remove incorrectly saved data?!?!?
power_mask = power < 20000
power[power_mask]*=10
power_mask = power < 20000
power[power_mask]*=10
power_mask = power < 20000
power[power_mask]*=10
power_mask = power < 20000
power[power_mask]*=10

power_mask = power < 20000
power[power_mask]*=10


#power /= 1000
power /= 100000

#time_hours = np.array([time_parser(t, d, 16) for t,d in zip(time, date)], dtype = float)
#time_hours -= time_hours[0]


time_hours = time / (60*60)

m = round(np.mean(power[300:]),3)
st = round(np.std(power[300:]),3)

# print(time_hours[200:220], power[200:220])
# exit()


#ax.plot(time_hours[5000:5050], power[5000:5050], label = "Mean: {}\nStd: {}".format(m, st))
ax.plot(time_hours, power, label = "Mean: {}\nStd: {}".format(m, st))
ax.set_xlabel("Time (hours)")
ax.set_ylabel("Power (mW)")
ax.set_title("633 HeNe - 28 Hour Power Stability")
#ax.set_title("413 DLPro - 20 Hour Power Stability")
# plt.savefig(savedir + "PowerStabilityPlot.png")

# plt.legend()
#plt.savefig(savedir + "PowerStabilityDLPRONewLab.png")
plt.show()