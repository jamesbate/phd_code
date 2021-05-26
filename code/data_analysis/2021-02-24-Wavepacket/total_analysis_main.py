from total_analysis import fit_wavepacket
from stdlib import CavipyPlotter
from stdlib import PhotonObject, PlotTemplate
import matplotlib.pyplot as plt

cavipy_folder = "C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2020-02-24-Wavepacket\\"

time_tagger_file = "X:\\measurements\\QFC\\2021_02_24\\2021_02_24_153010.txt"
cavipy_results_files = ["Results_fine.dat", "\Results_highg.dat", "Results15g.dat", "Results12g.dat"]

#cavipy_results_files =["C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2020-02-24-Wavepacket\\Results_highg.dat"]
roi = [0.10e8,0.5e8]

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

cp_array = [CavipyPlotter(cavipy_folder+c) for c in cavipy_results_files]
photon_object = PhotonObject(time_tagger_file)

photon_object.print_channel_counts()
print(photon_object.get_efficiency(0,6))
#photon_object.plot_normalised_wavepacket(0,2 , 2e6,[0,2e8], ax = ax)
photon_object.plot_normalised_wavepacket(0,6 , 2e6, roi, ax = ax)
# cp.plot_wavepacket_single(ax = ax, amplitude = 0.3, displace_time = 10.5)

init_values = [
    [0.32, 12.6],
    [0.12, 12.6],
    [0.22, 12.6],
    [0.28, 12.6]
]

for n,i in enumerate(cp_array):
    fit_wavepacket(i, photon_object, roi, init_values[n],ax = ax)
plt.show()
