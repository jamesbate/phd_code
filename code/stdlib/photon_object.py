"""Object to handle all data related to photon wavepackets
"""
##----------------------PREAMBLE---------------------------##
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
#package dependencies

from stdlib.plots import PlotTemplate
#external imports

from scipy import stats

##-----------------------CLASS DEFINITION-----------------------##

class PhotonObject:
    def __init__(self, time_tagger_file):
        self.time_tagger_file = time_tagger_file 

        #total data file
        self.data = self._extract_data(time_tagger_file)
        #data for each channel
        self.channel_data = self._extract_channel_data()

        #Store all data
        self.df_signals = None
        #store counts for each channel
        self.channel_counts = None 

        self.pt = PlotTemplate((1,1))
        

    
    def plot_histogram(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, count_thresholds = None,ax = None, colour = None, plot_roi = True):
        #manually plot histogram with bar so I can define bin size
        #count thresholds should be an array [min_count, max_count]

        times, values = self.get_binned_triggered_times_counts(channel_totrigger, channel_tocount, bin_size, region_of_interest)

        if count_thresholds:
            #applying value thresholds
            mask = np.logical_and(values > count_thresholds[0], values < count_thresholds[1])
            times = times[mask]
            values = values[mask]
            times_reject = times[np.logical_not(mask)]
            values_reject = values[np.logical_not(mask)]
            print('Mask applied:\n{}'.format(mask))
            if np.any(np.logical_not(mask)):
                ax.bar(times_reject, values_reject, width = bin_size, color = 'r', label = "Rejected counts")

        if ax is None: 
            ax = self.pt.generate_figure()

        if region_of_interest:
            if plot_roi == True:
                ax.axvline(region_of_interest[0], c = 'r', linestyle = "--", linewidth = 2)
                ax.axvline(region_of_interest[1], c = 'r', label = "Region of interest", linestyle = "--", linewidth = 2)

        if colour is not None:
            ax.bar(times, values, width = bin_size, color = colour)
        else:
            ax.bar(times, values, width = bin_size, color = 'g')
        #decoration
        ax.set_title("Histogram of Photon counts")
        ax.set_xlabel("Time from trigger (us)")
        ax.set_ylabel("Counts")

    def get_cumalative(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, count_thresholds = None, colour = None, plot_roi = True, microseconds=True):
        times, values = self.get_binned_triggered_times_counts(channel_totrigger, channel_tocount, bin_size, region_of_interest, microseconds = microseconds)

        if count_thresholds:
            #applying value thresholds
            mask = np.logical_and(values > count_thresholds[0], values < count_thresholds[1])
            times = times[mask]
            values = values[mask]
            print('Mask applied:\n{}'.format(mask))

        #sort data in time order
        args = np.argsort(times)
        times = times[args]
        values = values[args]

        values = np.cumsum(values)

        #find probs and dprobs 
        total_triggers = self.get_channel_counts()[channel_totrigger]

        probs = values/total_triggers
        dprobs = probs/np.sqrt(values)

        return (times, probs, dprobs)

    def plot_cumulative(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, count_thresholds = None,ax = None, colour = None, plot_roi = True, microseconds = True):
        #manually plot histogram with bar so I can define bin size
        #count thresholds should be an array [min_count, max_count]

        times, probs, dprobs = self.get_cumalative(channel_totrigger, channel_tocount, bin_size, region_of_interest = region_of_interest, count_thresholds = count_thresholds, colour = colour, plot_roi = plot_roi, microseconds=microseconds)

        if ax is None: 
            ax = self.pt.generate_figure()

        if region_of_interest:
            if plot_roi == True:
                #chose to remove label this time
                ax.axvline(region_of_interest[0], c = 'r', linestyle = "--", linewidth = 2)
                ax.axvline(region_of_interest[1], c = 'r', linestyle = "--", linewidth = 2)

            
        #add efficiency calculation
        eff = self.get_efficiency(channel_totrigger, channel_tocount, region_of_interest)

        if colour is None:
            ax.errorbar(times, probs, dprobs,ls = "none", fmt = 'o', capsize = 3)
            ax.axhline(eff, c = 'm', linestyle = "--", linewidth = 2, label = "Efficiency: {}".format(round(eff,3)))
        else:
            ax.errorbar(times, probs, dprobs,ls = "none", fmt = 'o', capsize = 3, c = colour)
            ax.axhline(eff, c = colour, linestyle = "--", linewidth = 2, label = "Efficiency: {}".format(round(eff,3)))

        
        #decoration
        ax.set_title("Cumalitive Probability")
        ax.set_xlabel("Time from trigger "+r"$\mu s$")
        ax.set_ylabel("Cumalitive Probability Density "+r"$\mu s^{-1}$")
    
    def plot_normalised_wavepacket(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, count_thresholds = None,ax = None, colour=None, microseconds = True):

        times, probs, dprobs = self.get_normalised_wavepacket(channel_totrigger, channel_tocount, bin_size, region_of_interest = region_of_interest, count_thresholds = count_thresholds, microseconds =microseconds)

        #sort data in time order
        args = np.argsort(times)
        times = times[args]
        probs = probs[args]
        dprobs = dprobs[args]

        dt = times[1] - times[0]

        
        if ax is None: 
            ax = self.pt.generate_figure()

        if colour is None:
            ax.errorbar(times, probs/dt, dprobs/dt,ls = "none", fmt = 'o', capsize = 3)
        else:
            ax.errorbar(times, probs/dt, dprobs/dt,ls = "none", fmt = 'o', capsize = 3, c = colour)
        

        #decoration
        ax.set_title("Wavepacket\t" + r"$\Omega: 41$" + "MHz\tg: 1.25MHz")
        ax.set_xlabel("Time from trigger "+r"$\mu s$")
        ax.set_ylabel("Probability density "+r"$\mu s^{-1}$")

    def get_normalised_wavepacket(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, count_thresholds = None, microseconds = True):

        times, values = self.get_binned_triggered_times_counts(channel_totrigger, channel_tocount, bin_size, region_of_interest, microseconds =microseconds)

        if count_thresholds:
            mask = np.logical_and(values > count_thresholds[0], values < count_thresholds[1])
            times = times[mask]
            values = values[mask]
            print('Mask applied:\n{}'.format(mask))
        
        #find probs and dprobs 
        total_triggers = self.get_channel_counts()[channel_totrigger]

        probs = values/total_triggers
        dprobs = probs/np.sqrt(values)

        return (times, probs, dprobs)

    def get_binned_triggered_times_counts(self, channel_totrigger, channel_tocount, bin_size, region_of_interest = None, microseconds = True):
        relative_trigger_times = self.get_triggered_times(channel_totrigger, channel_tocount, microseconds =microseconds)
        if region_of_interest:
            relative_trigger_times = relative_trigger_times[np.logical_and(relative_trigger_times < region_of_interest[1],relative_trigger_times > region_of_interest[0])]
        #now use bin data method
        counter = self.bin_data(relative_trigger_times, bin_size)
        #is this the best thing to return?
        return (np.array(list(counter.keys())), np.array(list(counter.values())))

    def bin_data(self, data, binsize):
        #copied form trics, adapt

        cnt = Counter()

        #bin count data
        for d in data:
            bin_num = d//binsize
            #counter are always indexed by center
            cnt[bin_num*binsize + 0.5*binsize] += 1

        return cnt


    def _get_trigger_indices(self, tigger_times, count_times):
        trigger_indices = [np.searchsorted(tigger_times, k) for k in count_times]
        return np.array(trigger_indices) - 1

    def get_channel_counts(self):
        #return total counts for each channel
        return [self.channel_data[k].shape[0] for k in range(8)]
    
    def get_efficiency(self, channel_totrigger, channel_tocount, region_of_interest = None, microseconds = True):
        #VALUE THRESHOLD CURRENTLY NOT IMPLEMENTED
       
        total_triggers = self.get_channel_counts()[channel_totrigger]
        relative_trigger_times = self.get_triggered_times(channel_totrigger, channel_tocount, microseconds = microseconds)
        if region_of_interest:
            mask = np.logical_and(relative_trigger_times < region_of_interest[1],relative_trigger_times > region_of_interest[0])
            c = sum(mask)
        else:
            c = relative_trigger_times.size
        return c/total_triggers

    def print_channel_counts(self):
        channel_counts = self.get_channel_counts()
        for k,n in enumerate(channel_counts):
            print("Channel {}:\t {} counts".format(k, n))

    def _extract_data(self, time_tagger_file):
        #read time tagger data and convert into dataframe for data handling
        return pd.read_csv(time_tagger_file, delimiter = "\t")

    def _extract_channel_data(self):
        #return an array of dataframes containing all times of each signals from each channel
        return [self.data[self.data['Channel'] == k] for k in range(8)]

    def print_data(self, channel_totrigger, channel_tocount, region_of_interest):
        print("Full data:\n{}\n".format(self.data))
        print("Channels:\n")
        for k in range(8):
            print("Channel {}\n".format(k))
            print(self.channel_data[k])
        self.print_channel_counts()
        print(self.get_efficiency(channel_totrigger, channel_tocount, region_of_interest))

    
    def get_triggered_times(self, channel_totrigger, channel_tocount, microseconds = True):
        #Create array of time relative to trigger

        trigger_times = self.channel_data[int(channel_totrigger)]['Time stamps'].to_numpy()
        count_times = self.channel_data[int(channel_tocount)]['Time stamps'].to_numpy()
        trigger_indices = self._get_trigger_indices(trigger_times, count_times)
       
        active_trigger_times = trigger_times[trigger_indices]
        relative_trigger_times = count_times - active_trigger_times

        #convert to microseconds
        if microseconds:
            relative_trigger_times*=1e-6

        return relative_trigger_times


