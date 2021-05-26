# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
#MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
analyse_ion=self.set_variable("bool","analyse_ion",1)

#on_time=self.set_variable("float","on_time",5000.000000,0.01,2e7)
# Doppler cooling
# detection time
ResTime=self.set_variable("float","ResTime",5000.000000,0.0,2e7)
pulse_length=self.set_variable("float","pulse_length",500.000000,0.0,2e7)
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

Cycles 50
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
#ttl_pulse("31",10,is_last=True)
for i in range (0,3):
    ttl_pulse("28",pulse_length,is_last=False)
    #setTTLOn("28",0,is_last=True)
    #seq_wait(ResTime)
    ttl_pulse("29",pulse_length,start_time=ResTime,is_last=True)
    #setTTLOn("29",0,is_last=True)
    seq_wait(500)
    #setTTLOFF("29",0,is_last=True)
    #setTTLOFF("29",0,is_last=True)
    

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
