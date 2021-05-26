# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser

init_length=self.set_variable("float","init_length",100.000000,1,2e5)
wait_length=self.set_variable("float","wait_length",100.000000,1,2e5)
pulse_length=self.set_variable("float","pulse_length",100.000000,1,2e5)
dummy=self.set_variable("float","dummy",100.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)


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

Cycles 1
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
#TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
#rf_on(150, 0, dds_address=0, start_time = 0)
#setTTLOff("StartSeq",0,is_last=False)

InitPulse()
#setTTLOn("StartSeq",raman_length*2,is_last=True)
#ttl_pulse("32",raman_length/2,is_last=False)
seq_wait(wait_length)

RamanPulse(pulse_length,is_last=False)
ttl_pulse("24",pulse_length/2,is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
