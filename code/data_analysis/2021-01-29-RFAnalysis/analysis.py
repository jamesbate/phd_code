##--------------------------PREAMBLE------------------------##
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#packages 

from stdlib import PlotTemplate
##------------------------------PARAMETERS-----------------------##
data_folder = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2021-01-29-RFAnalysis\\"
save_folder = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-01-29-RFAnalysis\\"
pt = PlotTemplate((1,1))
ax = pt.generate_figure()

##------------------------NO DP------------------------##

# pd_data = pd.read_csv(data_folder+"scope_13.csv", sep = ',', skiprows = 2)
# times = np.linspace(0,20000, 2000)[1600:1900]
# ax.plot(times, pd_data.iloc[1600:1900,2], label = "length: 900ns")
# ax.get_yaxis().set_visible(False)
# plt.title("Second pi/2 pulse: No 393 double pass")
# plt.xlabel('Time (ns)')
# plt.legend()
# plt.savefig(save_folder + "npdp.png")
# plt.show()

##-------------------------NORMAL CONDITIONS------------------------##
#1999 rows
# pd_data = pd.read_csv(data_folder+"scope_14.csv", sep = ',', skiprows = 2)
# times = np.linspace(0,20000, 2000)
# ax.plot(times[1700:1900], pd_data.iloc[1700:1900,2], label = "length: 600ns")
# ax.get_yaxis().set_visible(False)
# plt.title("Second pi/2 pulse: Normal conditions")
# plt.xlabel('Time (ns)')
# plt.legend()
# plt.savefig(save_folder + "normalconditions.png")
# plt.show()

##===================================##
#Out of line

# pd_data = pd.read_csv(data_folder+"scope_14.csv", sep = ',', skiprows = 2)
# labels = ['Raman SP', '','Raman DP' ,'AOD\ndisplaced by 200ns']
# times = np.linspace(0,20000, 2000)
# for j in [1,3,4]:
#     ax.plot(times[1300:1600], pd_data.iloc[1300:1600,j], label = labels[j-1])
# ax.get_yaxis().set_visible(False)
# plt.title("Ending of 393 Dp/Sp and AOD: Normal conditions")
# plt.xlabel('Time (ns)')
# plt.legend()
# plt.savefig(save_folder + "alignment.png")
# plt.show()

##-------------------------NO AOD------------------------##

# pd_data = pd.read_csv(data_folder+"scope_11.csv", sep = ',', skiprows = 2)

# ax.plot(pd_data)
# plt.show()

##-------------------------NORMAL CONDITIONS 2------------------------##

# pd_data = pd.read_csv(data_folder+"scope_07.csv", sep = ',', skiprows = 2)

# ax.plot(pd_data)
# plt.show()