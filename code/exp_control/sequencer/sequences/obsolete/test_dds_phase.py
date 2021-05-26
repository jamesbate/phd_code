# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>
det_time=self.set_variable("float","det_time",100000.000000,0.01,2e7)
wait_time=self.set_variable("float","wait_time",100000.000000,0.01,2e7)
#freq729=self.set_variable("float","freq729",482.750000,400,600)
#power729=self.set_variable("float","power729",0.000000,-100,1)
#freqRaman=self.set_variable("float","freqRaman",260.000000,230,400)
#powerRaman=self.set_variable("float","powerRaman",0.000000,-100,1)
#switch729=self.set_variable("bool","switch729",0)
#switchRaman=self.set_variable("bool","switchRaman",0)

pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e7)
phi=self.set_variable("float","phi",0.0,0,10)


</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(1:N);		%1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode fluorescence
DOasTTLword 1
TTLword 0
Cycles 1
</PARAMS OVERRIDE>

<SEQUENCE>


PMTDetection(det_time)
rf_729(pulse_length, 0, "myTrans")
#seq_wait(wait_time)
rf_729(pulse_length, math.pi * phi, "myTrans")

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
