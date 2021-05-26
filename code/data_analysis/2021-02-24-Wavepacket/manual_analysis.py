from total_analysis import fit_wavepacket
from stdlib import CavipyPlotter
from stdlib import PhotonObject, PlotTemplate
import matplotlib.pyplot as plt

save_dir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\2021-02-24-Wavepacket\\"
cavipy_folder = "C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2020-02-24-Wavepacket\\"

time_tagger_file = "X:\\measurements\\QFC\\2021_02_24\\2021_02_24_153010.txt"
cavipy_results_files = ["Results_fine.dat", "\Results_highg.dat", "Results15g.dat", "Results12g.dat", "Results08g.dat"]
cavipy_results_files = ["Results_newstark_10.dat", "Results_newstark_11.dat", "Results_newstark_12.dat", "Results_newstark_13.dat", "Results_newstark_14.dat"]
cavipy_results_files = ["Results_newstark_125.dat"]

roi = [10,60]
roi2 =  [110, 160]

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

# pt = PlotTemplate((2,1))
# axes = pt.generate_figure()

cp_array = [CavipyPlotter(cavipy_folder+c) for c in cavipy_results_files]
photon_object = PhotonObject(time_tagger_file)

#print stuff
photon_object.print_channel_counts()


# photon_object.plot_histogram(0, 6, 2, region_of_interest = roi,ax = axes[0])
# photon_object.plot_histogram(0, 2, 2, region_of_interest = roi2,ax = axes[1], colour = pt.colours[1])


# photon_object.plot_histogram(0, 6, 2, region_of_interest = [0,200],ax = axes[0], plot_roi=False)
# photon_object.plot_histogram(0, 2, 2, region_of_interest = [0,200],ax = axes[1], colour = pt.colours[1], plot_roi=False)
# plt.legend()
# plt.savefig(save_dir + "Wavepacketssim.png")
# plt.show() 
# exit()

# photon_object.plot_cumulative(0, 6, 2, region_of_interest = roi, colour = "g", ax = ax)
# photon_object.plot_cumulative(0, 2, 2, region_of_interest = roi2, colour = pt.colours[1], ax = ax)

eff1 = photon_object.get_efficiency(0,6, roi)
eff2 = photon_object.get_efficiency(0,2, roi2)




#print(photon_object.get_efficiency(0,2, roi2))
# print(photon_object.get_efficiency(0,6, [10, 80]))
# exit()

#do plot
photon_object.plot_normalised_wavepacket(0,2 , 2,roi2, ax = ax, colour = pt.colours[1])
photon_object.plot_normalised_wavepacket(0,6 , 2, roi, ax = ax, colour = 'g')

# cp.plot_wavepacket_single(ax = ax, amplitude = 0.3, displace_time = 10.5)

#now plot cavipy stuff
# init_values = [
#     [0.33, 12.8],
#     [0.13, 14],
#     [0.2, 13.5],
#     [0.28, 12.8],
#     [0.5, 12.8]
# ]
# init_values = [
#     [0.49, 13],
#     [0.41, 13],
#     [0.36, 13],
#     [0.33, 13],
#     [0.29, 13]
# ]
init_values = [
    12,
    98
]

# lab = ['1.05','2','1.5','1.2','0.8']
lab = ['1.0','1.1','1.25','1.3','1.4']

cp_array[0].plot_wavepacket_single(roi = roi, ax = ax, efficiency = eff1, displace_time = init_values[0], label = "g: {}MHz".format(lab[2]), colour = "r")
cp_array[0].plot_wavepacket_single(roi = roi2, ax = ax, efficiency = eff2, displace_time = init_values[1], label = "g: {}MHz".format(lab[2]), colour = "r")


# cp_array[0].plot_wavepacket_cumulative(ax = ax, amplitude = init_values[0][0], displace_time = init_values[0][1], label = "g: {}MHz, A: {}".format(lab[2], init_values[0][0]), colour = "r")
# cp_array[0].plot_wavepacket_cumulative(ax = ax, amplitude = init_values[1][0], displace_time = init_values[1][1], label = "g: {}MHz, A: {}".format(lab[2], init_values[0][0]), colour = "r")


print(cp_array[0].get_efficiency(roi = roi))
exit()
# cp_array[0].plot_wavepacket_cumulative(roi = roi,ax = ax,efficiency = eff1, displace_time = init_values[0], label = "g: {}MHz".format(lab[2]), colour = "r")
# cp_array[0].plot_wavepacket_cumulative(roi = roi2, ax = ax,efficiency = eff2, displace_time = init_values[1], label = "g: {}MHz".format(lab[2]), colour = "r")

plt.legend()
#plt.savefig(save_dir + "Wavepacketscumfitsim4.png")
plt.savefig(save_dir + "Wavepacketsfitsim4.png")

# for n,i in enumerate(cp_array):
#     inits = init_values[n]
#     # l = "g: {}MHz, A: {}".format(lab[n], inits[0])
#     l = "g: {}MHz, A: {}".format(lab[2], inits[0])
#     i.plot_wavepacket_single(ax = ax, amplitude = inits[0], displace_time = inits[1], label = l)

plt.show()
