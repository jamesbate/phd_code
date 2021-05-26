"""Basic class to create plot templates because I got tired of constantly 
creating new figures
"""
##-------------------------------PREAMBLE-----------------------------------##
import matplotlib.pyplot as plt 
#packages

##-------------------------------CLASS DEFINITION-----------------------------------##

class PlotTemplate:

    def __init__(self, dim):
        self.property_params = {
            'font.size': 16,
            'figsize': (18,9)
        }
        self.dim = dim
        self.colours = ['b','m','c','r','tab:orange', 'tab:pink']
    
    def generate_figure(self):
        plt.rcParams.update({'font.size': self.property_params['font.size']})#not sure this works?

        _, axes = plt.subplots(self.dim[0], self.dim[1], constrained_layout=True, figsize=self.property_params['figsize'])
        

        #lazy implementation, can be improved
        if self.dim[0] == 1 and self.dim[1] == 1:
            axes.minorticks_on()
            axes.grid(True)
            axes.grid(which='minor', linestyle = '--', alpha = 0.6)            
        else:
            for ax in axes:
                ax.minorticks_on()
                ax.grid(True)
                ax.grid(which='minor', linestyle = '--', alpha = 0.6)

        return axes