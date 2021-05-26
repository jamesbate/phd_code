# General S/D experiment

<VARIABLES>
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)
# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

#optical pumping with 397 sigma
#opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)


#Clock_pulse=self.set_variable("bool","Clock_pulse",1)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)


# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)

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

Cycles 100
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
#InitPulse()
seq_wait(7)
#seq_wait(wait_time)
rf_on(150, -100, dds_address=0, start_time = 0)

ttl_pulse("854 sw",repump_length,is_last=False)
DopplerCooling(doppler_length, is_last=True)
#PMTDetection(doppler_length)

ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
ttl_pulse("866 sw",pump_length+20,is_last=True)
#seq_wait(0.1)



rf_pulse(1000, 0, ion=1, transition_param='Clock1', is_last=True, address=1)


ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
