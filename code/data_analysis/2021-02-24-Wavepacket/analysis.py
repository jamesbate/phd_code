import matplotlib.pyplot as plt

from stdlib import PhotonObject, PlotTemplate

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

time_tagger_file = "X:\\measurements\\QFC\\2021_02_24\\2021_02_24_153010.txt"

photon_object = PhotonObject(time_tagger_file)
photon_object.print_channel_counts()
print(photon_object.get_efficiency(0,6))
photon_object.plot_normalised_wavepacket(0,2 , 2e6,2e8, ax = ax)
photon_object.plot_normalised_wavepacket(0,6 , 2e6,2e8, ax = ax)
plt.show()