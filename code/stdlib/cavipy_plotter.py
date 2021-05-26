import pandas as pd
from stdlib.plots import PlotTemplate
import numpy as np

class CavipyPlotter:

    def __init__(self, cavipy_result_file):
        self.result_file = cavipy_result_file 
        #extract data file into DataFrame
        self.df = self._extract_data(self.result_file)

        self.pt = PlotTemplate((1,1))

    def _extract_data(self, file):
        return pd.read_csv(file, delimiter = "\t")

    def get_efficiency(self, roi):
        time = self.df['Time(us)']
        prob_dens_cum = self.df['PhotonACum'].to_numpy()

        dt = time[1] - time[0]

        prob_cum = prob_dens_cum*dt

        index = np.searchsorted(time, roi[1])


        return prob_cum[index]

    def plot_wavepacket_single(self, roi,ax = None,efficiency = 1, displace_time = None, label = None, colour = None):
        if ax is None: 
            ax = self.pt.generate_figure()
        time = self.df['Time(us)']
        if displace_time:
            time += displace_time
        prob = self.df['PhotonA']

        eff_sim = self.get_efficiency(roi)
        amplitude = efficiency/eff_sim

        if colour is None:
            ax.plot(time, amplitude*prob, label = label)
        else:
            ax.plot(time, amplitude*prob, label = label, c = colour)
    
    def get_wavepacket_single(self, displace_time = None):
        #maybe other methods should use this? Quite simple. unsure
        time = self.df['Time(us)']
        time_copy = time.copy()
        if displace_time:
            time_copy += displace_time
        prob = self.df['PhotonA']
        return (time_copy, prob)

    def plot_wavepacket_cumulative(self, roi, ax = None, efficiency = 1, displace_time = None, label = None, colour = None):
        if ax is None: 
            ax = self.pt.generate_figure()
        time = self.df['Time(us)']
        if displace_time:
            time += displace_time
        prob_dens_cum = self.df['PhotonACum'].to_numpy()

        dt = time[1] - time[0]

        prob_cum = prob_dens_cum*dt

        eff_sim = self.get_efficiency(roi)
        amplitude = efficiency/eff_sim


        if colour is None:
            ax.plot(time, amplitude*prob_cum, label = label)
        else:
            ax.plot(time, amplitude*prob_cum, label = label, c = colour)