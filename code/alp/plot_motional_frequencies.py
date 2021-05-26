"""Ben wanted me to plot motional sidebands 
for planned 3 ion GHZ states
"""

import numpy as np 
import matplotlib.pyplot as plt  
from stdlib import PlotTemplate

rad = 2100/1000
axm = np.array([869, 1550, 2160])/1000
orders = 5
thick = 0.6

pt = PlotTemplate((1,1))
ax = pt.generate_figure()

def df_MHZ(m):
    dg = 0.8 
    B = 4.229 
    return 1.4*B*m*dg

for f0 in df_MHZ(np.array([0,1,2,3,4])):

    for k in range(orders):
        if k == orders-1:
            plt.axvline(x=f0+(k+1)*axm[0], c='b', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[0], label='COM', c='b', linewidth = thick*(orders + 1 - k))
        else:
            plt.axvline(x=f0+(k+1)*axm[0], c='b', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[0], c='b', linewidth = thick*(orders + 1 - k))

    for k in range(orders):
        if k == orders-1:
            plt.axvline(x=f0+(k+1)*axm[1], c='g', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[1], label='Stretch', c='g', linewidth = thick*(orders + 1 - k))
        else: 
            plt.axvline(x=(k+1)*axm[1], c='g', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[1], c='g', linewidth = thick*(orders + 1 - k))

    for k in range(orders):
        if k == orders-1:
            plt.axvline(x=f0+(k+1)*axm[2], c='m', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[2], label='3rd', c='m', linewidth = thick*(orders + 1 - k))
        else: 
            plt.axvline(x=f0+(k+1)*axm[2], c='m', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*axm[2], c='m', linewidth = thick*(orders + 1 - k))

    for k in range(orders):
        if k == orders-1:
            plt.axvline(x=f0+(k+1)*rad, c='r', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*rad, label='Radial', c='r', linewidth = thick*(orders + 1 - k))
        else: 
            plt.axvline(x=f0+(k+1)*rad, c='r', linewidth = thick*(orders + 1 - k))
            plt.axvline(x=f0-(k+1)*rad, c='r', linewidth = thick*(orders + 1 - k))

plt.legend()
plt.xlabel('Frequency (MHz)')
plt.show()