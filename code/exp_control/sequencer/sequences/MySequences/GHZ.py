"""Prepares GHZ states and performs MS gate. 
Date: 21/01/2021
Author: James Bate
"""
##--------------------------------------------------VARIABLES----------------------------------------------------##
<VARIABLES>

MeasPoints=self.set_variable("float","MeasPoints",500,1,2e5)#unsure of purpose?

#Global
pipulse_loopnumber = self.set_variable("float","pipulse_loopnumber",1,0,50)#For setting pitime

#Ramsey
do_ramsey=self.set_variable("bool","do_ramsey",1)
ramsey_wait=self.set_variable("float","ramsey_wait",0,0,5e3)
phase_ramsey=self.set_variable("float","phase_ramsey",0,0,2e5)

#Carrier pulse
do_carrier_pipulse=self.set_variable("bool","do_carrier_pipulse",0)#For setting pitime
pitime_carrier=self.set_variable("float","pitime_carrier",2.,0,2e5)
pihalftime_carrier=self.set_variable("float","pihalftime_carrier",2.,0,2e5)

#MS
do_MS=self.set_variable("bool","do_MS",0)
do_MS_pihalf = self.set_variable("bool","do_MS_pihalf",0)
MS_pulselength=self.set_variable("float","MS_pulselength",1000.000000,0,2e5)
phase_MS=self.set_variable("float","phase_MS",0,0,2e5)



#Parity flops
do_pihalf_pulse=self.set_variable("bool","do_pihalf_pulse",0)

#Ground state preparation 

#Doppler cooling
dc_long=self.set_variable("float","dc_long",8000.000000,0.01,2e7)

#sideband cooling
sb_cool_com=self.set_variable("bool","sb_cool_com",0)
SBCool_time=self.set_variable("float","SBCool_time",2000.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",2500.000000,0.01,2e7)

#optical pumping with 397 sigma
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)
repump_length=self.set_variable("float","repump_length854",20.000000,1,2e5)
short_cool_length=self.set_variable("float","short_cool_length",50.000000,0,2e5)

#Analysis

do_probe_729_pulse=self.set_variable("bool","do_probe_729_pulse",0)
probe_729_length=self.set_variable("float","probe_729_length",1000.000000,0,2e5)

</VARIABLES>

##--------------------------------------------------PREAMBLE----------------------------------------------------##

<TRANSITIONS>
</TRANSITIONS>
# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum;       (1:N);      %1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode fluorescence

Cycles 50
</PARAMS OVERRIDE>

##--------------------------------------------------SEQUENCE----------------------------------------------------##
<SEQUENCE>
##=======================================##
#TRANSITION -> FUNCTION 
#729_Carrier -> GLOBAL PULSE's (PARITY FLOPS, RAMSEY, MS CORRECTION)
#729_MS -> IMPLEMENT MS GATE
#729_Probe -> ANALYSIS
##=======================================##

##----------------------CONSTANTS--------------------------##

#global constants 
opt_pumping = True
repump866_length = repump_length
delay =0.1
delay_between = 5
aod_delay = 5
init_length =  150

##----------------------STATE PREPARE--------------------------##

#Turning all lasers off
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw", "729SP1", "20"])
seq_wait(1)

#Line trigger
ttl_pulse("21",5,is_last=True)

#Doppler cooling
ttl_pulse("854 sw",dc_long+repump_length,is_last=False)
DopplerCooling(dc_long, is_last=False)
PMTDetection(dc_long)

#Optical pumping
if opt_pumping:
    ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
    ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    #ttl_pulse(["854"],repump_length,is_last=False)
seq_wait(1)

#Sideband cooling
if sb_cool_com:
    setTTLOn("729SP2",0,is_last=True)
    SBCooling2(length = SBCool_time, pumptime = pump_length)
    setTTLOff("729SP2",0,is_last=True)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump_length,is_last=True)
seq_wait(1)


# switchSH:
setTTLOff("28",0.0,is_last=True) #switch to hold #was 17 before 05.12
seq_wait(2)
setTTLOff("11",0.0,is_last=True) #switch off 806 SP going to ion cavity  #was 9
seq_wait(2)


setTTLOff("393DP",0,is_last=True) #off for using pulsebox dds
seq_wait(delay)
setTTLOff("7",0,is_last=True)# RESET LOGIC

##----------------------APPLY GATES--------------------------##

#setting pitime
setTTLOn("729_not_393second",0,is_last=True)
if do_carrier_pipulse:
    for k in range(int(pipulse_loopnumber)):
        seq_wait(3)
        setTTLOn("729SP2",0,is_last=True)
        rf_pulse(pitime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1) 
        setTTLOff("729SP2",0,is_last=True)
seq_wait(1)

#MS gate
if do_MS:
    setTTLOn("20",0,is_last=True) #bichro
    setTTLOn("729SP2",0,is_last=True)
    seq_wait(5)
    rf_pulse(MS_pulselength, phase_MS*3.141592653*0.25, ion=1, transition_param='729_MS', is_last=True, address=1)
    seq_wait(5)
    setTTLOff("20",0,is_last=True) #bichro

    if do_MS_pihalf:
        #Global pi/2 pulse if odd number of ions
        rf_pulse(pihalftime_carrier, (phase_MS)*3.141592653*0.25, ion=1, transition_param='729_Carrier', is_last=True, address=1)#THINK THIS IS THE RIGHT PHASE?

    setTTLOff("729SP2",0,is_last=True)

seq_wait(delay)

#Ramsey 
if(do_ramsey):
    setTTLOn("729SP2",0,is_last=True)
    seq_wait(5)
    rf_pulse(pihalftime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)    #sigma y
    seq_wait(ramsey_wait)
    rf_pulse(pihalftime_carrier, phase_ramsey*3.141592653*0.25, ion=1, transition_param='729_Carrier', is_last=True, address=1)
    seq_wait(1)
    setTTLOff("729SP2",0,is_last=True)
        

#MS - Parity flops   
if(do_pihalf_pulse):
    seq_wait(3)
    setTTLOn("729SP2",0,is_last=True)
    seq_wait(5)
    rf_pulse(pihalftime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)    #sigma y
    seq_wait(1)
    setTTLOff("729SP2",0,is_last=True)
        
seq_wait(1)

##----------------------ANALYSIS----------------------------##

#Analysis pulse
if do_probe_729_pulse:
    setTTLOn("729SP2",0,is_last=True)
    rf_pulse(probe_729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    setTTLOff("729SP2",0,is_last=True)
    seq_wait(delay)

setTTLOn("11",0.0,is_last=True) #switch on again 806 SP going to ion cavity  #was 10
seq_wait(2)
setTTLOn("28",0.0,is_last=True) #switch to sampling

seq_wait(0.1)
setTTLOff("729SP2",0,is_last=True)

#Final state detection
ttl_pulse(["22"],100,is_last=False) #camera    
ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
seq_wait(1)
ttl_pulse("29",20,is_last=True)#Reset
TTLsOff(["Pi397","866 sw", "729_not_393second"])

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
