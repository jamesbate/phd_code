"""This object is designed to handle data from our experiment. It uses pandas
to do most of the general handling. As well as basic pandas methods such as
loading and getting data, it has methods to plot histograms, get probabilities,
get mean excitation and bin data.
"""
##-------------------------------PREAMBLE-----------------------------------##
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import math
#external dependencies

from stdlib.plots.plot_histogram import plot_histogram
#internal imports
##---------------------------OBJECT DEFINITION-------------------------------##

class TricsDataObject:
    """Data handling object for our experimental data
    Methods
    -------
    load_data(self, filename) -> standard pandas loading from file to dataframe

    get_data(self, reshape, indices) -> return all the data in the file, either
        in one single array, or in multiple columns as it was for the datafile.

    get_probs(self, thresholds, indices, nmin, nmax) -> calculates the projection
        noise from binned data with simple poissonian statistics

    get_mean_exc(self, thresholds, indices = None, nmin = 0, nmax = 100) -> adapts
        calculated probabilities into mean excitation which scales well for an
        arbitrary sized ion string

    plot_data_histogram(self, thresholds, indices, nmin, nmax) -> Make histogram plots
        of data, with additional verticle threshold line.

    bin_data(self, data, thresholds, nmin = 0, nmax = 100, binsize = 1) -> group
        data into bins, use for photodetector data.
    
    TO BE ADDED

    Attributes
    ----------
    df -> dataframe of loaded data

    data_start_column -> start column of data as detailed in init docstring

    column_names -> names of columns of data.
    """
    def __init__(self, filename, data_start_column):
        """
        Parameters
        ----------
        filename : str
            Directory of data to load

        data_start_column : int
            If main data in file is spread out from a particular column to the
            final column (as can be the case with out data), specify which
            column the data starts at. This is used in the get_data() method
        """
        self.df = self.load_data(filename)
        self.data_start_column = data_start_column
        self.column_names = self.df.columns

    def load_data(self, filename):
        return pd.read_csv(filename, delimiter = "\t")

    def get_data(self, reshape = True, indices = None):
        """
        Parameters
        ----------
        reshape : bool
            if False, data returns as columns from data_start_column entry. if
            True, all data is reshaped into a single column.

        indices : array-like
            only select some of the columns
        """
        if indices is not None:
            data = self.df.iloc[indices, self.data_start_column:self.df.shape[1]].to_numpy()
        else:
            data = self.df.iloc[:,self.data_start_column:].to_numpy()

        if reshape == False:
            return data

        reshaped = np.prod(data.shape)
        return data.reshape(1,reshaped)[0]

    def plot_data_histogram(self, thresholds = None, indices = None, nmin = 0, nmax = 100, ax = None):
    	#data taken from from self.%data_name%

    	#extract data
        if indices is not None:
            mask = self.df.index.isin(indices)
            self.df = self.df[mask]

        data_shaped = self.get_data()

        #make hist plots
        if ax is None:
            fig, ax = plt.subplots(1	,1, constrained_layout=True)
            plt.grid()

        #do histogram plot
        _, n, _ = plot_histogram(data_shaped, nmin = nmin, nmax = nmax, binsize = 1, ax = ax)

        #apply threshold horizontal lines if given
        if thresholds is not None:
        	for t in thresholds:
        		ax.axvline(x=t, c = 'r')

        #return populations
        return n

    def get_probs(self, thresholds, indices = None, nmin = 0, nmax = 100, allow_zero_error = True):
        #do i need to fix this for more than two ions? 

        #get data
        if indices is not None:
            data = self.get_data(reshape = False, indices = indices)
        else:
            data = self.get_data(reshape = False)

        #prepare arrays of probability
        p = np.zeros([data.shape[0],len(thresholds) + 1])
        dp = np.zeros([data.shape[0],len(thresholds) + 1])

        cycles = data.shape[1]

        print("Cycles:",cycles)
        for i,d in enumerate(data,0):
            #seperate data into each histogram (number of ions detected)


            n = self.bin_data(d, nmin = nmin, nmax = nmax, binsize = 1, thresholds = thresholds)

            #use poissonian statistics to calculate probability and error
            p[i] = np.array(n)/cycles
            if allow_zero_error == True:
                dp[i] = np.sqrt(p[i]*(1-p[i])/cycles)
            else:
                dp[i] = np.maximum(np.sqrt(p[i]*(1-p[i])/cycles), 1/(cycles + 2))


        return (p,dp)
    
    def projection_uncertainty(self, p, cycles, allow_zero_error = True):
        if allow_zero_error == False:
            return np.maximum(np.sqrt(p*(1-p)/cycles), 1/(cycles + 2))
        return np.sqrt(p*(1-p)/cycles)
    
    def get_parity(self, p, dp = None):
        #probability assumed to be numpy
        parity = 0 
        for k in range(p.shape[1]):
            parity += (-1)**k*p[:,k]
        if dp is not None: 
            dparity = 0
            for k in range(dp.shape[1]):
                dparity += dp[:,k]**2
            dparity = np.sqrt(dparity)      
            return (parity, dparity)  
        else:
            return (parity, None)

    def get_mean_exc(self, thresholds, nmax,indices = None, allow_zero_error = True, nmin = 0, **kwargs):
    
            #get data
        if indices is not None:
            data = self.get_data(reshape = False, indices = indices)
        else:
            data = self.get_data(reshape = False)
        

        n_ions = len(thresholds) 
        cycles = data.shape[1]

        #X_mat = np.array([list(range(nions+1))]).T

        me = np.ones(data.shape[0])
        dme = np.zeros(data.shape[0])
        total_bright_ions = np.zeros(data.shape[0])
        total_bright_ions_2 = np.zeros(data.shape[0])

        for i,d in enumerate(data):
            n = self.bin_data(d, nmin = nmin, nmax = nmax, binsize = 1, thresholds = thresholds)
            for j in range(n_ions+1):
                total_bright_ions[i] += j*n[j]  
                total_bright_ions_2[i] += j**2*n[j]
                # if i == 0:
                #     print(n[j])

        E_X = total_bright_ions/(cycles*(n_ions))

        E_X2 = total_bright_ions_2/(cycles*(n_ions)**2)
        #var = total_bright_ions_2 - total_bright_ions**2
        std = np.sqrt(E_X2 - E_X**2)/np.sqrt(cycles)

        if allow_zero_error == False:
            #only used for weighted plots
            std[std == 0] = math.nan
            minim = np.nanmin(std)
            std[np.isnan(std)] = minim

        
        me -= total_bright_ions/(n_ions*cycles)
        dme += np.sqrt(total_bright_ions)/(n_ions*cycles)



        return (1-E_X, std)


    def bin_data(self, data, thresholds, nmin = 0, nmax = 100, binsize = 1):

        cnt = Counter()
        bin_edges = np.array([nmin - binsize/2] + list(thresholds) + [nmax + binsize/2])
        bins = bin_edges[:-1]

        #initialise counter
        for e in bins:
            cnt[e] = 0

        #bin count data
        for d in data:
            for j in range(len(bin_edges)):
                if bin_edges[j] > d:
                    cnt[bins[j-1]] += 1
                    break

        return list(cnt.values())
    
    def get_post_select_mask(self, thresholds, index, p_upper = False, p_lower = False, dp_upper = False, dp_lower = False, nmin = 0, ignore_indices = None,nmax = 100):
        """Calculates probabilities and then post selects points. There may 
        be a more general way to do this? Index tells you what bin you select on. We are binning rows of the df. 
        """
        (p, dp) = self.get_probs(thresholds, indices = None, nmin = nmin, nmax = nmax, allow_zero_error = False)
        #force allow_zero_error to be False for now as I don't see a need for it 

        mask = np.ones(p.shape[0], dtype = bool)
        #first get True mask 

        if p_upper: 
            mask = np.logical_and(mask, p[:,index] < p_upper) 
        if p_lower: 
            mask = np.logical_and(mask, p[:,index] > p_lower) 
        if dp_upper: 
            mask = np.logical_and(mask, dp[:,index] < dp_upper) 
        if dp_lower: 
            mask = np.logical_and(mask, dp[:,index] > dp_lower) 
        if ignore_indices:
            for i in ignore_indices:
                mask[i] = False 
        #compound each condition
        
        return mask 
        

