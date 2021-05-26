from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt 

Nmeasurements = 100 
relative_phase = 0.1
dG = 5

def probabilities(phase):
    return (np.cos(phase)**2,  np.sin(phase)**2) 

def var_binomial(n,p):
    return n*p*(1-p)

def var_prob_estimator(n,p):
    return var_binomial(n,p)/n**2 

std_prob_estimator = lambda n,p: np.sqrt(var_prob_estimator(n,p)) 

def var_phase_estimator(n,relative_phase):
    p = probabilities(relative_phase)[0]
    return abs(var_prob_estimator(n,p)/(2*np.cos(relative_phase)*np.sin(relative_phase))**2)

def var_alpha_estimator(n,relative_phase):
    return var_phase_estimator(n,relative_phase)/relative_phase**2

p1 = probabilities(relative_phase)[0]
print('Probabilities: {}\np estimator std/var: {}/{}\nPhase estimator std/var: {}/{}\nAlpha estimator std/var {}/{}'.format(probabilities(relative_phase), std_prob_estimator(Nmeasurements, p1),var_prob_estimator(Nmeasurements, p1), np.sqrt(var_phase_estimator(Nmeasurements, relative_phase)), var_phase_estimator(Nmeasurements, relative_phase),  np.sqrt(var_alpha_estimator(Nmeasurements, relative_phase)), var_alpha_estimator(Nmeasurements,relative_phase)))


def phi(alpha):
    return dG*alpha 


relative_phase_array = np.linspace(0.1,3,100)
plt.plot(probabilities(relative_phase_array)[0], var_phase_estimator(Nmeasurements, relative_phase_array))
plt.show()
