import matplotlib.pyplot as plt
from stdlib import CavipyPlotter

cp = CavipyPlotter("C:\\Users\\James\OneDrive - OnTheHub - The University of Oxford\\phd\\data\\2020-02-24-Wavepacket\\Results.dat")

cp.plot_wavepacket_single()
plt.show()