from lib import FitTemplate, fit_rabi_twoions, PlotTemplate
import numpy as np
import matplotlib.pyplot as plt

pt = PlotTemplate((1,1))
ax = pt.generate_figure() 
fit_temp = FitTemplate(fit_rabi_twoions)

#set parameters 
fit_temp.parameters.add('dicke_factor', 0.068/np.sqrt(2), vary = False)
fit_temp.parameters.add('detuning', 0, vary = False)
fit_temp.parameters.add('amplitude', 1, vary = False)

#free parameters
fit_temp.parameters.add('n_av', 1, vary = False)
fit_temp.parameters.add('phase', 1, vary = True)
fit_temp.parameters.add('Rabi', 0.6, vary = False)

points = 100
x = np.linspace(0,350, points)

y1 = fit_temp.plot_fit_optcurve(x, parameters = fit_temp.parameters.valuesdict(), dn = 1, pop_state = 2, points = points)
fit_temp.parameters.add('Rabi', 0.601, vary = False)
y2 = fit_temp.plot_fit_optcurve(x, parameters = fit_temp.parameters.valuesdict(), dn = -1, pop_state = 2, points =points)
ax.plot(x[1:], y2[1:]/y1[1:])
plt.show() 