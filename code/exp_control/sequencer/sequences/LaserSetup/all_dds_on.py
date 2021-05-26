
<VARIABLES>

all_on=self.set_variable("bool","all_on",1)

power=self.set_variable("float","power",0.000000,-100,0)

delta_freq=self.set_variable("float","delta_freq",0.000000,-200,200)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

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
Cycles 50
</PARAMS OVERRIDE>

<SEQUENCE>

#dds_on(address, freq, power_dB)
if all_on:
    dds_on(0, 230 + delta_freq, power)
    dds_on(1, 80 + delta_freq, power)
    dds_on(2, 80 + delta_freq, power)
    dds_on(3, 200 + delta_freq, power)
    dds_on(4, 200 + delta_freq, power)
    dds_on(5, 200 + delta_freq, power)
    dds_on(6, 200 + delta_freq, power)
    dds_on(7, 200 + delta_freq, power)

getPMTcounts(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
