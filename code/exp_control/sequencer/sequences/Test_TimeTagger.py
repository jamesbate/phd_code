# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for
# specified time (Duration)


<VARIABLES>

det_time=self.set_variable("float","det_time",1000,0.01,2e7)

switchFlags=self.set_variable("bool","switchFlags",0)

#freqRaman=self.set_variable("float","freqRaman",260.000000,230,400)
#powerRaman=self.set_variable("float","powerRaman",0.000000,-100,1)
#
#switchRaman=self.set_variable("bool","switchRaman",0)
#gl_cam_time=self.set_variable("float","gl_cam_time",100000.000000,0,2e7)
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
Cycles 1
</PARAMS OVERRIDE>

<SEQUENCE>
for i in range(20):
	ttl_pulse("31",100,start_time = 0,is_last=True)
	seq_wait(100)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
