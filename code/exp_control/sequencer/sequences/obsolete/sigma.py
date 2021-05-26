# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>
det_time=self.set_variable("float","det_time",100000.000000,0.01,2e7)

switch729=self.set_variable("bool","switch729",0)
port729diag=self.set_variable("bool","port729diag",0)
port729tips=self.set_variable("bool","port729tips",0)
freq729=self.set_variable("float","freq729",450.000000,440,640)
power729=self.set_variable("float","power729",0.000000,-100,1)

switch2670=self.set_variable("bool","switch2670",0)
freq2670=self.set_variable("float","freq2670",400.000000,300,500)
power2670=self.set_variable("float","power2670",0.000000,-100,1)

switch2674=self.set_variable("bool","switch2674",0)
freq2674=self.set_variable("float","freq2674",400.000000,300,500)
power2674=self.set_variable("float","power2674",0.000000,-100,1)

switch397sigma=self.set_variable("bool","switch397sigma",0)
switch854=self.set_variable("bool","switch854",0)
switch866=self.set_variable("bool","switch866",0)
doppler_mode=self.set_variable("bool","doppler_mode",0)
shutter_394=self.set_variable("bool","shutter_394",1)
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
#TTLword 16898
TTLword 32518
#TTLmask 131071
Cycles 10
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

if switch397sigma:
    setTTLOn("397 sigma", is_last=False)

if switch854:
    setTTLOn(["854 double"], is_last=False)
    setTTLOn(["854 single"], is_last=False)
    setTTLOn(["mon 4"], is_last=False)

if port729diag:
    setTTLOn("729 diag", is_last=False)
else:
    setTTLOff("729 diag", is_last=False)

if port729tips:
    setTTLOn("729 tips", is_last=False)
else:
    setTTLOff("729 tips", is_last=False)
    
if shutter_394:
    setTTLOn("32", is_last=False)
else:
    setTTLOff("32", is_last=False)
    
if switch729:
    rf_729_on(freq729,power729)
else:
    rf_729_on(freq729,-100)

if switch2670:
    rf_2670_on(freq2670,power2670)
    setTTLOn("267 0", is_last=False)
else: 
    rf_2670_on(freq2670,-100)
    setTTLOff("267 0", is_last=False)

if switch2674:
    rf_2674_on(freq2674,power2674)
    setTTLOn("267 4", is_last=False)
else: 
    rf_2674_on(freq2674,-100)
    setTTLOff("267 4", is_last=False)


# if switchRaman: rf_setRaman(freqRaman,powerRaman)
# else: rf_setRaman(freqRaman,-100)

# incl.PMTDetection(det_time,no_lasers=True)
PMTDetection(det_time, doppler=doppler_mode, no866=not switch866)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
