# Difference Fluorescence experiment
# 15.2.06 TKK


# det_time in ms
<VARIABLES>
det_time=self.set_variable("float","det_time",200000.000000,0.01,2e7)

switch729=self.set_variable("bool","switch729",0)
port729diag=self.set_variable("bool","port729diag",0)
port729tips=self.set_variable("bool","port729tips",0)
freq729=self.set_variable("float","freq729",450.000000,400,500)
power729=self.set_variable("float","power729",0.000000,-100,1)

switch2670=self.set_variable("bool","switch2670",0)
freq2670=self.set_variable("float","freq2670",400.000000,300,500)
power2670=self.set_variable("float","power2670",0.000000,-100,1)

switch2674=self.set_variable("bool","switch2674",0)
freq2674=self.set_variable("float","freq2674",400.000000,300,500)
power2674=self.set_variable("float","power2674",0.000000,-100,1)

switch397sigma=self.set_variable("bool","switch397sigma",0)
switch854=self.set_variable("bool","switch854",0)
sigma_mode=self.set_variable("bool","sigma_mode",0)
doppler_mode=self.set_variable("bool","doppler_mode",0)
#word=self.set_variable("int","word",0)  # Labview is blind to integers
#mask=self.set_variable("int","mask",0)  # Labview is blind to integers
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
#AcquisitionMode fluorescence
AcquisitionMode differential
Cycles 20

# TTLwords:
# default: 29190 (397 double & pi, 866 double & single)
# with 854: 32270
# with sigma: 29446
# with 854 & sigma: 32526

TTLword 28934
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

# ttl_setall(word,mask)
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

if switch729:
    rf_729_on(freq729,power729)
else: rf_729_on(freq729,-100)

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

#ttl_pulse(["397 double", "397 pi", "mon 2"], 5000, is_last=False)
#ttl_pulse(["866 double", "866 single", "mon 3"], 5000 + 20, is_last=True)
setTTLOff("397 sigma", is_last=True)
#DopplerCooling(det_time, 10)
PMTDetection(det_time, doppler=doppler_mode)

seq_wait(5)
PMTDetection(det_time, doppler=doppler_mode, sigma_mode = True)
seq_wait(5)
#if sigma_mode:
#    PMTDetection(det_time, doppler=doppler_mode, sigma_mode = True)
#else:
#    PMTDetection(det_time, doppler=doppler_mode, no866 = True, sigma_mode = True)

</SEQUENCE>

<AUTHORED BY LABVIEW>
4
</AUTHORED BY LABVIEW>
