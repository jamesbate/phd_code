# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",20.000000,1,2e5)
raman_length=self.set_variable("float","raman_length",10.000000,1,2e5)

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
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])

seq_wait(7)

for i in range(5):
    seq_wait(7)
    RamanPulse(raman_length)
    seq_wait(70)

ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
