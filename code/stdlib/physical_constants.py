"""This class simply saves all of the physical constants I need
"""
##----------------------------CLASS DEFINITION--------------------------------##
import numpy as np

class PhysicalConstants:
    def __init__(self):
        self.h_bar = 1.054571817e-34
        self.m_e = 9.10938356e-31
        self.m_p = 1.6726219e-27
        self.m_calc = 40*self.m_p
        self.k_B = 1.38064852e-23
        self.h = 6.62607004e-34
        self.q_e = 1.6022e-19
        self.mu_B = 9.274e-24
        self.mu_0 = 4*(np.pi)*1e-7
        self.epsilon_0 = 8.854187817e-12

    def g_j(self,j,l,s):
	    return (3*j*(j+1) - l*(l+1) + s*(s+1))/(2*j*(j+1))

