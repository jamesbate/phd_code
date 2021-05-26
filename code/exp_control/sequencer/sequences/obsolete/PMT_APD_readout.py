# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>

# Typically the name of the PMT detection time field is 'det_time'
# not 'PMT_det_time'.
det_time=self.set_variable("float","det_time",100000.000000,0.01,2e7)

# APD detection time
apd_det_time=self.set_variable("float","apd_det_time",300000.000000,0.01,2e7)

freq729=self.set_variable("float","freq729",482.750000,400,600)
power729=self.set_variable("float","power729",0.000000,-100,1)
freqRaman=self.set_variable("float","freqRaman",260.000000,230,400)
powerRaman=self.set_variable("float","powerRaman",0.000000,-100,1)
switch729=self.set_variable("bool","switch729",0)
switchRaman=self.set_variable("bool","switchRaman",0)
</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(1:N);		%1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode apd
APD_PM_Count 2
DOasTTLword 1
Cycles 1
</PARAMS OVERRIDE>

<SEQUENCE>

# if switch729: rf_set729(freq729,power729)
# else: rf_set729(freq729,-100)
# if switchRaman: rf_setRaman(freqRaman,powerRaman)
# else: rf_setRaman(freqRaman,-100)

# incl.PMTDetection(det_time,no_lasers=True)
PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
