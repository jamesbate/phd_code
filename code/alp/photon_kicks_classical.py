from stdlib import PhysicalConstants

pc = PhysicalConstants()

p_393 = pc.h/393e-9 
p_854 = pc.h/854e-9 

trap_freq = 1e6 

class ClassicalPhaseState:
    def __init__(self, E_init):
        self.E = E_init 
        self.E_list = [E_init]

    def apply_kick_random_time(self):
        pass 
        #directed laser pulse

    def apply_kick_random_time_phase(self):
        pass
        #spontaneous emission