"""After seeing how great the lmfit package, I was inspired to create my own
object employing it. This acts as a fitting template. 
"""
##-------------------------------PREAMBLE-----------------------------------##
import numpy as np 
import matplotlib.pyplot as plt 
from lmfit import minimize, Parameters, fit_report 
import logging 
from stdlib.plots import PlotTemplate
from stdlib.plots.plot_histogram import plot_histogram 
from stdlib.plots.plot_error_joint import plot_error_joint
##-------------------------------CLASS DEFINITION-----------------------------------##

class FitTemplate(): 
    def __init__(self, fit_function, log_dir = None):
        self.fit_function = fit_function 
        self.parameters = Parameters()
        self.fit_result = None
        self.fit_result_params = None
        self.fit_result_error_dict = {}
        

        #setup logging. warning level is standard and is sent to stdout. info is requested by log_dir argument,
        #and is printed to log file
        if log_dir is not None: 
            logging.basicConfig(filename=log_dir +'log.log', level=logging.INFO)
        else:
            logging.basicConfig(level=logging.CRITICAL)
    

    def _residuals_wrapper(self, parameters, x, data,weights,**kwargs):
        model_values = self.fit_function(x, parameters.valuesdict(), **kwargs)
        #reshape data 
        data = data.reshape((data.size,1))
        model_values = model_values.reshape((model_values.size,1))
        if not isinstance(weights, int):
            weights = weights.reshape((weights.size, 1))
        return ((model_values - data)*weights)**2
        
    def do_minimisation(self, x, data, weights = 1, errorbars = None,**kwargs):
        self.fit_result = minimize(self._residuals_wrapper, self.parameters, args = (x, data, weights), kws = kwargs, nan_policy = 'propagate')
        self.fit_result_params = self.get_opt_parameters()
        if errorbars is not None:
            self.fit_result_lower = minimize(self._residuals_wrapper, self.parameters, args = (x, data-errorbars, weights), kws = kwargs, nan_policy = 'propagate')
            self.fit_result_lower_params = self.fit_result_lower.params.valuesdict()
            self.fit_result_upper = minimize(self._residuals_wrapper, self.parameters, args = (x, data+errorbars, weights), kws = kwargs, nan_policy = 'propagate')
            self.fit_result_upper_params = self.fit_result_upper.params.valuesdict()
            #now update error dict 
            for (name_l,param_l),(name_u,param_u) in zip(self.fit_result_lower.params.items(), self.fit_result_upper.params.items()):
                self.fit_result_error_dict.update({name_l: (param_u - param_l)/2})
                
        else:
            self.fit_result_lower_params = {}
            self.fit_result_upper_params = {}
            for name, param in self.fit_result.params.items():
                if param.stderr is None: 
                    self.fit_result_lower_params.update({name: param.value})
                    self.fit_result_error_dict.update({name: param.stderr})
                else:
                    self.fit_result_lower_params.update({name: param.value - param.stderr})
                    self.fit_result_error_dict.update({name: param.stderr})
            for name, param in self.fit_result.params.items():
                if param.stderr is None: 
                    self.fit_result_upper_params.update({name: param.value})
                else:
                    self.fit_result_upper_params.update({name: param.value + param.stderr})

        logging.info('Fit Result')
        logging.info('==========')
        self.log_print_result()
        return self.fit_result

    def plot_fit_errorcurves(self, x, y, dy,args_0,args_1, args_2, ax = None, color = 'g', label = None, fill = False, xlabel = 'pick xlabel', ylabel = 'pick ylabel', title = "pick title"):
        """wrapper around the plot_fit_curve function 
        """
        #args of form [params_dict, kwargs]

        [params_dict_0, kwargs_0] = args_0
        [params_dict_1, kwargs_1] = args_1
        [params_dict_2, kwargs_2] = args_2
        y_0 = self.fit_function(x, params_dict_0, **kwargs_0)
        y_lower = self.fit_function(x, params_dict_1, **kwargs_1)
        y_upper = self.fit_function(x, params_dict_2, **kwargs_2)
        dy = dy.reshape((1, dy.size))[0]#or else errorbar plot complains
        plot_error_joint(x, y, dy,y_0,y_lower.ravel(), y_upper.ravel(), ax = ax, color = color, label = label, fill = fill, xlabel = xlabel, ylabel =ylabel, title = title)
    
    def plot_fit_optcurve(self, x, parameters = None,points = 1000,xlabel = None, ylabel = None, title = None, label = None, ax = None, c = None, colour_index = None,**kwargs):
        """This function plots the curve of the optimum set of parameters. If parameters argument given, this overrides optimum parameters and 
        plots custom parameters. 
        """

        #Use plot template if no ax argument given
        plot_template = PlotTemplate((1,1))
        if ax is None:
            ax = plot_template.generate_figure() 

        #decide colour 
        if c is not None: 
            color = c 
        elif colour_index is not None: 
            color = plot_template.colours[colour_index]
        else: 
            color = plot_template.colours[0]

        #plot model
        fitdomain = np.linspace(x[0], x[-1], points)	
        if parameters is None:
            y = self.fit_function(fitdomain, self.fit_result.params.valuesdict(), **kwargs)
            ax.plot(fitdomain, y, c = color, label = label)
        else:
            y = self.fit_function(fitdomain, parameters, **kwargs)
            ax.plot(fitdomain, y, c = color, label = label)
        #set labels
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        return y


    def plot_fit(self, x, y, xlabel = None, ylabel = None, title = None, errorbars = None, label = None, ax = None, c = None, colour_index = None, error_lines = False,**kwargs): 
        """Full plotting function. 
        """
        #Use plot template if no ax argument given
        plot_template = PlotTemplate((1,1))
        if ax is None:
            ax = plot_template.generate_figure() 

        #decide colour 
        if c is not None: 
            color = c 
        elif colour_index is not None: 
            color = plot_template.colours[colour_index]
        else: 
            color = plot_template.colours[0]

        #First check if error lines are requested
        if error_lines is not False: 
            if error_lines == 'filled':
                fill = True
            else:
                fill = False
            args_0 = [self.fit_result_params, kwargs]
            args_1 = [self.fit_result_lower_params, kwargs]
            args_2 = [self.fit_result_upper_params, kwargs]
            self.plot_fit_errorcurves(x, y, errorbars,args_0,args_1, args_2, ax = ax, color = color, label = label, fill = fill, xlabel = xlabel, ylabel = ylabel, title = title)
            return y 
        
        #if error plot not requested, go ahead with standard plot
        #scatter plot
        ax.scatter(x, y, color = color)
        #plot errors
        if errorbars is not None:
            ax.errorbar(x, y, errorbars, ls = 'none', c = color, capsize = 3)
        
        #plot model
        self.plot_fit_optcurve(x, ax = ax, c = color, label = label, xlabel = xlabel, ylabel = ylabel, title = title, **kwargs)

        return y

    def get_opt_parameters(self):
        if self.fit_result is None: 
            raise ValueError("No fit result! Do a fit before asking for")
        return self.fit_result.params.valuesdict()

    def print_parameters(self):
        self.parameters.pretty_print() 
    
    def print_fit_result(self):
        print(fit_report(self.fit_result))

    def log_print_result(self):
        logging.info((fit_report(self.fit_result)))
        logging.info('Errors:')
        logging.info(self.fit_result_error_dict)






