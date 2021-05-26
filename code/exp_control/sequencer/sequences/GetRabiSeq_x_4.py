# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
#MeasPoints=self.set_variable("float","MeasPoints",20.000000,1,2e5)
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)
# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
#optical pumping with 397 sigma
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)


# wait time before the experiment
wait_time=self.set_variable("float","delay",1,0,500000)

# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)


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

Cycles 10
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw","393DP"])
rf_on(150, -100, dds_address=0, start_time = 0)

ttl_pulse("854 sw",repump_length,is_last=False)
DopplerCooling(doppler_length, is_last=False)
PMTDetection(doppler_length)
#opt.pumping
ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
ttl_pulse("866 sw",pump_length+20,is_last=True)
seq_wait(0.1)


setTTLOn("729_not_393second",start_time=0,is_last=True)
#seq_wait(0.1)
rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
seq_wait(5)
rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
seq_wait(5)
rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
seq_wait(5)
rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
seq_wait(5)
setTTLOff("729_not_393second",start_time=0,is_last=True)
#setTTLOff("729 sw",start_time=0,is_last=True)
seq_wait(0.1)

#rf_on(150, -100, dds_address=0, start_time = 0)
ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
