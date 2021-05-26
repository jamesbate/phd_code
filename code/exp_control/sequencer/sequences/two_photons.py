# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
n_loops=self.set_variable("float","n_loops",1,1,500000)

# Raman pulse 
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)
between_raman=self.set_variable("float","between_raman",50.000000,0,2e5)
# ion analys


# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)
dc_long=self.set_variable("float","dc_long",5000.000000,0.01,2e7)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)
repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)
switchSH=self.set_variable("bool","turn_on_SH",1)

# delays during the experiment
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
p729_pulse=self.set_variable("bool","p729_pulse",0)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)

mes_type=self.set_variable("float","mes_type",0,0,2e5)


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
DopplerCooling(dc_long, is_last=False)
PMTDetection(dc_long)
if switchSH:
    setTTLOff("17",0.0,is_last=True) #switch to hold
    seq_wait(2)
    setTTLOff("9",0.0,is_last=True) #switch off 806 SP going to ion cavity
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(doppler_length, repump866_length, is_last=True)
    seq_wait(1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    seq_wait(0.1)
    ttl_pulse("31",5,is_last=True)
    RamanV(raman_length)
    ttl_pulse("866 sw",between_raman,is_last=False)
    ttl_pulse("854 sw",between_raman,is_last=True)
    RamanH(raman_length)

    seq_wait(2)
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(doppler_length, repump866_length, is_last=True)
    seq_wait(1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    seq_wait(0.1)
    if not p729_pulse:
        RamanV(raman_length)
        ttl_pulse("854 sw",between_raman,is_last=True)
        seq_wait(40)
        RamanH(raman_length)

  
if p729_pulse:
    rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    seq_wait(1)    
    ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
    PMTDetection(det_time)
setTTLOn("9",0.0,is_last=True) #switch on again 806 SP going to ion cavity
seq_wait(2)
setTTLOn("17",0.0,is_last=True) #switch to sampling
seq_wait(2)

TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
