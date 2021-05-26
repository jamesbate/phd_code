# Difference Fluorescence experiment

<VARIABLES>

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# switch the 729 laser on or off, e.g. to see quantum jumps
switch729=self.set_variable("bool","switch729",0)
port729diag=self.set_variable("bool","port729diag",0)
port729tips=self.set_variable("bool","port729tips",0)
freq729=self.set_variable("float","freq729",450.000000,400,500)
power729=self.set_variable("float","power729",0.000000,-100,1)

# switch the 267.0 laser on or off
switch2670=self.set_variable("bool","switch2670",0)
freq2670=self.set_variable("float","freq2670",400.000000,300,500)
power2670=self.set_variable("float","power2670",0.000000,-100,1)

# switch the 267.4 laser on or off
switch2674=self.set_variable("bool","switch2674",0)
freq2674=self.set_variable("float","freq2674",400.000000,300,500)
power2674=self.set_variable("float","power2674",0.000000,-100,1)

# Do the detection sequence with (usually) reduced power
doppler_mode=self.set_variable("bool","doppler_mode",0)


dummy=self.set_variable("float","dummy",0.000000,0,1000)

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
Cycles 100

# TTLwords:
# default: 29190 (397 double & pi, 866 double & single)
# with 854: 32270
# with sigma: 29446
# with 854 & sigma: 32526

# 2, 3, 10, 13, 14, 15:
# TTLword 29190

# 2, 3, 5, 10, 13, 14, 15:
# TTLword 29206
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

if port729diag:
    setTTLOn("729 diag", is_last=False)
else:
    setTTLOff("729 diag", is_last=False)

if port729tips:
    #setTTLOn("729 tips", is_last=False)
    rf_729_tips_on(80., 0)
else:
    #setTTLOff("729 tips", is_last=False)
    rf_729_tips_on(0., -100)

if switch729:
    rf_729_on(freq729,power729)
else:
    rf_729_on(0.,-100)

if switch2670:
    rf_2670_on(freq2670,power2670)
    setTTLOn("267 0", is_last=False)
else: 
    rf_2670_on(0.,-100)
    setTTLOff("267 0", is_last=False)

if switch2674:
    rf_2674_on(freq2674,power2674)
    setTTLOn("267 4", is_last=False)
else: 
    rf_2674_on(0.,-100)
    setTTLOff("267 4", is_last=False)

if doppler_mode:
    power = "doppler"
else:
    power = "detection"
    
if abs(dummy - 5) < 0.0001:
    ttl_pulse("30", 100, start_time=0.0, is_last=True)

PMTDetection(det_time, power)
seq_wait(5)
PMTDetection(det_time, power, background = True)

</SEQUENCE>

<AUTHORED BY LABVIEW>
4
</AUTHORED BY LABVIEW>
