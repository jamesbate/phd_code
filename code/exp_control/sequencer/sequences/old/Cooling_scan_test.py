# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)
# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)

# detection time
det_time=self.set_variable("float","det_time",100.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
#dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

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
#ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
#TTLsOff("854 sw")
seq_wait(7)

for i in range(1):
    DopplerCooling(doppler_length)
    if opt_pumping:
        ttl_pulse(["397det","Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+20,is_last=True)

ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOn(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
