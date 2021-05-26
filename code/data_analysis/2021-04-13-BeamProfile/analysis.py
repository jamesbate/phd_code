from stdlib import PlotTemplate, FitTemplate, fit_gaussian
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

pt = PlotTemplate((1,2))
axes = pt.generate_figure()
savedir = "C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\Images\\PILasersNewSetup\\" 

data = pd.read_csv("C:\\Users\\James\\OneDrive - OnTheHub - The University of Oxford\\phd\\images\\PILasersNewSetup\\DLProXProfile_#001.txt", "\t", skiprows = range(10))

xpos = data['Pos X [um]'].to_numpy()
xval = data['X Value [%]'].to_numpy()
ypos = data['Pos Y [um]'].to_numpy()
yval = data['Y Value [%]'].to_numpy()
ypos = ypos[np.logical_not(np.isnan(ypos))]
yval = yval[np.logical_not(np.isnan(yval))]


ft= FitTemplate(fit_gaussian)
ft.parameters.add("A", value  = 100000)
ft.parameters.add("mean", value  = -200)
ft.parameters.add("sigma", value  = 500)

axes[0].plot(xpos, xval, c = pt.colours[0])
axes[1].plot(ypos, yval,c = pt.colours[2])



ft.do_minimisation(xpos, xval)
ft.print_fit_result()
params2 = ft.get_opt_parameters()
ft.plot_fit_optcurve(xpos, ax = axes[0], c = "r", label = r"$\sigma = $" + str(round(params2['sigma'],2)))
axes[0].set_xlabel("Distance (um)")
axes[0].set_ylabel("Fractional Intensity")
axes[0].set_title("DLPRO 413 - Beam Profile X\n"+ r"$\sigma = $" + str(round(params2['sigma'],2)))


ft.do_minimisation(ypos, yval)
ft.print_fit_result()
params1 = ft.get_opt_parameters()
ft.plot_fit_optcurve(ypos, ax = axes[1], c = "r", label = r"$\sigma = $" + str(round(params1['sigma'],2)))
axes[1].set_xlabel("Distance (um)")
axes[1].set_ylabel("Fractional Intensity")
axes[1].set_title("DLPRO 413 - Beam Profile Y\n" + r"$\sigma = $" + str(round(params1['sigma'],2)))

plt.savefig(savedir + "BeamProfileDLPro.png")
plt.show()