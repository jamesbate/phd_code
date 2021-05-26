# General S/D experiment

<VARIABLES>
n_loops=self.set_variable("float","n_loops",1,1,500000)
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)
ttl_length=self.set_variable("float","ttl_length",20.000000,1,2e5)
dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

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
for j in range(0,int(n_loops),1):
    ttl_pulse("TTL_TO_UNI",ttl_length,is_last=True)

PMTDetection(det_time)
seq_wait(1)
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
