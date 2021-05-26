# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
#MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
#analyse_ion=self.set_variable("bool","analyse_ion",1)

#on_time=self.set_variable("float","on_time",5000.000000,0.01,2e7)
# Doppler cooling
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)
variable_time=self.set_variable("float","variable_time",100.000000,0.01,2e7)
dummy_to_scan=self.set_variable("float","dummy_to_scan",100.000000,0.01,2e7)
num_of_pulses=self.set_variable("float","num_of_pulses",100.000000,0.01,2e7)
pulse_duration=self.set_variable("float","pulse_duration",100.000000,0.01,2e7)
gap_duration=self.set_variable("float","gap_duration",100.000000,0.01,2e7)




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
seq_wait(variable_time)
#turning all Lasers off
#ttl_pulse("31",10,is_last=True)
for i in range (0,int(num_of_pulses)):
    setTTLOn("28",0,is_last=True)
    seq_wait(pulse_duration)
    setTTLOff("28",0,is_last=True)
    seq_wait(gap_duration)
#seq_wait(10000)
PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
