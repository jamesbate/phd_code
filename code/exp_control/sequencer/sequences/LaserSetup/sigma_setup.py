# Difference Fluorescence experiment
# 15.2.06 TKK


<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(0:N);		%1.0f
  addPMTcounts;2;sum;(0:0);     (0:N);          %1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode differential

# 2, 3, 5, 9, 10, 13, 14, 15:
#TTLword 29462
Cycles 50

</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

DopplerCooling(doppler_length, repump_length, take_counts=False)

ttl_pulse(["397 double", "397 sigma"], det_time, is_last=False)
PMTDetection(det_time, power="off")

ttl_pulse(["397 double", "397 sigma"], det_time, is_last=False)
PMTDetection(det_time, power="off", background=True)

</SEQUENCE>

<AUTHORED BY LABVIEW>
4
</AUTHORED BY LABVIEW>
