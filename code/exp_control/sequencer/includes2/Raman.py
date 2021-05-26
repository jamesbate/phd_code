
def RamanPulse(raman,delay=1, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
    setTTLOn("30",start_time,is_last=False)
    #setTTLOn("24",40,is_last=False)
    #setTTLOff("24",start_time+40,is_last=False)
    setTTLOn("31",start_time,is_last=True)
    seq_wait(delay)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    setTTLOff("31",start_time,is_last=False)

    setTTLOff("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)
    setTTLOff("30",start_time,is_last=True)
    #setTTLOff("24",50,is_last=True)    
    
def RamanPulse2(raman,delay=1, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
     #setTTLOn("30",start_time,is_last=False)
    #setTTLOn("24",40,is_last=False)
    #setTTLOff("24",start_time+40,is_last=False)
    setTTLOn("31",start_time,is_last=True)
    seq_wait(delay)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    setTTLOff("31",start_time,is_last=False)

    setTTLOff("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)
    setTTLOff("30",start_time,is_last=True)
    #setTTLOff("24",50,is_last=True)
    
def RamanPulse_1550(raman,delay=1, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=True)
    seq_wait(delay)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=0.0, is_last=False, address=0, address2=1)
    setTTLOn("31",52,is_last=False)
    setTTLOn("24",52,is_last=True)
    seq_wait(delay)
    setTTLOff("31",start_time+raman,is_last=False)
    setTTLOff("24",start_time+raman,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    setTTLOff("393DP",start_time,is_last=True)
    seq_wait(1)
    
def TTLsOff(Laser,start_time=0.0, is_last=True):
    for i in range(len(Laser)-1):
        setTTLOff(Laser[i],start_time,is_last=False)
    setTTLOff(Laser[-1],start_time,is_last=is_last)

def TTLsOn(Laser,start_time=0.0, is_last=True):
    for i in range(len(Laser)-1):
        setTTLOn(Laser[i],start_time,is_last=False)
    setTTLOff(Laser[len(Laser)-1],start_time,is_last=is_last)

def SBCooling2(length=1000, reps=1, pumptime=20, repumptime=20, transition="sideband_cool"):
    #switch_729_port("diag", "on")
    #ttl_pulse(["854 double", "854 single", "mon 4"], length + repumptime, is_last=False)
    setTTLOn("729_not_393second",0,is_last=True)
    ttl_pulse(["854 sw"], length + repumptime, is_last=False)
    #rf_729(length, 0, transition, is_last=False)
    rf_pulse(length, 0, ion=1, transition_param=transition, is_last=False, address=1)
    if reps > 1:
        if (reps * pumptime) > length:
            pumptime = length / reps #this should never happen!
        for i in range(1, int(reps) + 1):
            # optical pumping during sbcooling
            OpticalPumping(length=pumptime, start_time=(float(length)/(reps+1))*i, is_last=False)
    
    # after sbcooling once more optical pumping
    #OpticalPumping(length=pumptime, start_time=length+repumptime+1)
    ttl_pulse(["866 sw"], repumptime, start_time=length+repumptime+1,is_last=False)
    ttl_pulse("854 sw", repumptime, start_time=length+repumptime+1,is_last=True)
    #switch_729_port("diag", "off", is_last=True)
    seq_wait(1)

def SBCoolingStrobe(length=1000, reps=1, pumptime=20, repumptime=20, transition="sideband_cool"):
    #switch_729_port("diag", "on")
    #ttl_pulse(["854 double", "854 single", "mon 4"], length + repumptime, is_last=False)
    try:
        Div_Length=float(length)/float(reps)
    except:
        Div_Length=float(length)
    setTTLOn("729_not_393second",0,is_last=True)
    ttl_pulse(["854 sw"], length + repumptime, is_last=False)
    #rf_729(length, 0, transition, is_last=False)
    for rep_count in range (0,reps+1):
        rf_pulse(Div_Length, 0, ion=1, transition_param=transition, start_time=rep_count*(float(Div_Length)+float(pumptime)), is_last=False, address=1)
        OpticalPumping(length=pumptime, start_time=rep_count*float(pumptime)+(rep_count+1)*float(Div_Length), is_last=False)
    #if reps > 1:
    #    if (reps * pumptime) > length:
    #        pumptime = length / reps #this should never happen!
    #    for i in range(1, int(reps) + 1):
    #        # optical pumping during sbcooling
    #        OpticalPumping(length=pumptime, start_time=(float(length)/(reps+1))*i, is_last=False)
    
    # after sbcooling once more optical pumping
    #OpticalPumping(length=pumptime, start_time=length+repumptime+1)
    ttl_pulse(["866 sw"], repumptime, start_time=length+repumptime+1,is_last=False)
    ttl_pulse("854 sw", repumptime, start_time=length+repumptime+1,is_last=True)
    #switch_729_port("diag", "off", is_last=True)
    seq_wait(1)
    
def InitPulse(raman=40,start_time=0.0, is_last=True):
    delay=4 
    #last=True
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=True)
    #setTTLOn("31",start_time,is_last=True)
    seq_wait(delay)
    ttl_pulse("StartSeq",raman-4,is_last=False)
    # rf_pulse(raman, 0, ion=1, transition_param='393_Init', is_last=False, address=0)
    # rf_pulse(raman, 0, ion=1, transition_param='393_Init2', is_last=True, address=1)
    rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Init', transition2_param='393_Init2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    #setTTLOff("31",start_time,is_last=False)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    #rf_pulse(raman, start_time, ion=1, transition_param='393_Init', is_last=is_last, address=0)
    #ttl_pulse("31",raman,is_last=is_last)

def RamanPulse_notGated(raman,delay=4, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
    seq_wait(delay)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(50)


def RamanV(raman,delay=0.95, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    #setTTLOn("31",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
    #seq_wait(delay)
    rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=True, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #seq_wait(delay)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOff("31",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)
def RamanH(raman,delay=0.1, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    #setTTLOn("31",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
    #seq_wait(delay)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #seq_wait(delay)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOff("31",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)

def RamanSetUp(raman,delay=0.1, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOn("31",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False)
    #seq_wait(delay)
    rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=True, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #seq_wait(delay)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOff("31",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)

def Raman729Pulse(raman,delay=10, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=False)
    setTTLOn("30",start_time,is_last=False)
    setTTLOn("31",start_time,is_last=True)
    seq_wait(delay)
    rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=False, address=0)
    rf_pulse(raman, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    setTTLOff("31",start_time,is_last=False)
    setTTLOff("393DP",start_time,is_last=False)
    setTTLOn("729_not_393second",start_time,is_last=True)
    seq_wait(delay)
    setTTLOff("30",start_time,is_last=True)