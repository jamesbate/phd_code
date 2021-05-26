import qutip 

dm = qutip.coherent_dm(5, 1.25)
(eig_energy, eig_states) = dm.eigenstates()

print(dm.transform(eig_states))
