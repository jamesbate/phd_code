from stdlib import generalised_Rabi, FitTemplate
import numpy as np 
import matplotlib.pyplot as plt

ft = FitTemplate(generalised_Rabi)

ft.parameters.add('dicke_factor_0', 0.069)
ft.parameters.add('dicke_factor_1', 0.071)
ft.parameters.add('n_av_0', 0)
ft.parameters.add('n_av_1', 1)

ft.parameters.add('detuning', 0)
ft.parameters.add('Rabi', 0.5)
ft.parameters.add('phase', 0)
ft.parameters.add('amplitude', 1)

fitdomain = np.linspace(0,100,200)
y = ft.fit_function(fitdomain, ft.parameters.valuesdict(), total_modes = 2, n_start_index = 2, ld_start_index = 0, m = [1,1], sum_limit = 10)

plt.plot(fitdomain, y)
plt.show()