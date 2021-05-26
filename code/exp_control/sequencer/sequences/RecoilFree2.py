# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
n_loops=self.set_variable("float","n_loops",1,1,500000)

opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)

Repump854=self.set_variable("bool","Repump854",0)
length_854=self.set_variable("float","length_854",50.000000,0,2e5)

RSB_Probe=self.set_variable("bool","RSB_Probe",0)
RSB_probe_length=self.set_variable("float","RSB_probe_length",5000.000000,0.01,2e7)

sb_cool_com=self.set_variable("bool","sb_cool_com",0)
SBCool_time=self.set_variable("float","SBCool_time",5000.000000,1,2e5)
sb_cool_rad=self.set_variable("bool","sb_cool_rad",0)
SBCool_time_rad=self.set_variable("float","SBCool_time_rad",5000.000000,1,2e5)
SBC_Pump_Time=self.set_variable("float","SBC_Pump_Time",30,1,2e5)
SBC_RePump_Time=self.set_variable("float","SBC_RePump_Time",500,1,2e5)
RepNo=self.set_variable("float","RepNo",1,0,2e5)
doLoops=self.set_variable("bool","doLoops",0)

# Raman pulse 
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)
#between_raman=self.set_variable("float","between_raman",50.000000,0,2e5)

# ion analys


# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)


#optical pumping with 397 sigma

repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)
#switchSH=self.set_variable("bool","turn_on_SH",1)

# delays during the experiment
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
p729_pulse=self.set_variable("bool","p729_pulse",0)
Ax729Pulse=self.set_variable("bool","Ax729Pulse",0)
Rad729Pulse=self.set_variable("bool","Rad729Pulse",0)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)

#mes_type=self.set_variable("float","mes_type",0,0,2e5)


</VARIABLES>
<TRANSITIONS>
</TRANSITIONS>
# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(1:N);		%1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode fluorescence

Cycles 50
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
#ttl_pulse("31",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
InitPulse(40)#max(20, raman_length))
ttl_pulse("854 sw",repump_length,is_last=False)
DopplerCooling(det_time, is_last=False)
PMTDetection(det_time)

if opt_pumping:
    ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
    ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)

# if p729_pulse:
    # setTTLOn("729_not_393second",0,is_last=True)
    # rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
    # #rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    # #rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    # #rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    # seq_wait(1)

# if Repump854:
    # ttl_pulse("854 sw",length_854,is_last=True)

if sb_cool_rad:
    setTTLOn("729SP2",0,is_last=True)
    SBCoolingStrobe(length = SBCool_time_rad,reps=int(RepNo), pumptime=SBC_Pump_Time,repumptime=SBC_RePump_Time,transition="sideband_cool_rad1")
    SBCoolingStrobe(length = SBCool_time_rad,reps=int(RepNo), pumptime=SBC_Pump_Time,repumptime=SBC_RePump_Time,transition="sideband_cool_rad2")
    setTTLOff("729SP2",0,is_last=True)
seq_wait(0.1)


if sb_cool_com:
    setTTLOn("729SP2",0,is_last=True)
    SBCoolingStrobe(length = SBCool_time, reps=int(RepNo), pumptime=SBC_Pump_Time, repumptime=500,transition="sideband_cool")
    setTTLOff("729SP2",0,is_last=True)
seq_wait(0.1)

# if doGSC:
    # #SBCooling2(length = SBCool_time, reps=2, pumptime=30, repumptime=500)
    # #SBCoolingStrobe(length = SBCool_time, reps=2, pumptime=SBC_Pump_Time, repumptime=500)
    # SBCoolingStrobe(length = SBCool_time, reps=int(RepNo), pumptime=SBC_Pump_Time, repumptime=500)
    # #ttl_pulse("854 sw",length_854,is_last=True)
    # #setTTLOn("729_not_393second",0,is_last=True)
    # #ttl_pulse(["854 sw"], SBCool_time + 400, is_last=False)
    # #rf_729(length, 0, transition, is_last=False)
    # #rf_pulse(SBCool_time, 0, ion=1, transition_param="sideband_cool", is_last=True, address=1)
    # #OpticalPumping(length=150, start_time=0)
# if RSB_Probe:
    # #setTTLOn("729_not_393second",0,is_last=True)
    # rf_pulse(RSB_probe_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
# if switchSH:
    # setTTLOff("17",0.0,is_last=True) #switch to hold
    # seq_wait(2)
    # setTTLOff("9",0.0,is_last=True) #switch off 806 SP going to ion cavity
# for i in range(int(n_loops)):
    # ttl_pulse("854 sw",repump_length,is_last=False)
    # DopplerCooling(doppler_length, repump866_length, is_last=True)
    # seq_wait(1)
    # if opt_pumping:
        # ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        # ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    # seq_wait(0.1)
    # ttl_pulse("31",5,is_last=True)
    # RamanV(raman_length)
    # ttl_pulse("866 sw",between_raman,is_last=False)
    # ttl_pulse("854 sw",between_raman,is_last=True)
    # RamanV(raman_length)
if doLoops:
    for i in range(int(n_loops)):
        RamanV(raman_length) #Do Raman pulse
        TTLsOff(["729SP2","729SP1"])
        seq_wait(1)
        setTTLOn("729SP1",is_last=True)#Here do a pi pulse only with radial
        rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)# Do pi pulse on a 729 transition
        seq_wait(1)
  
if p729_pulse:
    
    TTLsOff(["729SP1","729SP2"])
    seq_wait(1)
    if Ax729Pulse:#Here I can choose whetherIuse Ax or Rad beam
        setTTLOn("729SP1",is_last=True)
    if Rad729Pulse:
        setTTLOn("729SP2",is_last=True)
    rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    seq_wait(1)    
    ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
    PMTDetection(det_time)
    
    
    # seq_wait(2)
    # ttl_pulse("854 sw",repump_length,is_last=False)
    # DopplerCooling(doppler_length, repump866_length, is_last=True)
    # seq_wait(1)
    # if opt_pumping:
        # ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        # ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    # seq_wait(0.1)
    # RamanV(raman_length)
    # ttl_pulse("854 sw",between_raman,is_last=True)
    # RamanV(raman_length)
    # seq_wait(40)





ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
# setTTLOn("9",0.0,is_last=True) #switch on again 806 SP going to ion cavity
# seq_wait(2)
# setTTLOn("17",0.0,is_last=True) #switch to sampling
# seq_wait(2)

TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
