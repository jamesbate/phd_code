# Simple Fluorescence experiment

<VARIABLES>

# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

# switch the 729 laser on or off, e.g. to see quantum jumps
switch729=self.set_variable("bool","switch729",0)
port729diag=self.set_variable("bool","port729diag",0)
port729tips=self.set_variable("bool","port729tips",0)
freq729=self.set_variable("float","freq729",450.000000,440,640)
power729=self.set_variable("float","power729",0.000000,-100,1)

# switch the 267.0 laser on or off
switch2670=self.set_variable("bool","switch2670",0)
freq2670=self.set_variable("float","freq2670",400.000000,300,500)
power2670=self.set_variable("float","power2670",0.000000,-100,1)

# switch the 267.4 laser on or off
switch2674=self.set_variable("bool","switch2674",0)
freq2674=self.set_variable("float","freq2674",400.000000,300,500)
power2674=self.set_variable("float","power2674",0.000000,-100,1)

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
# 2, 3, 5, 10, 13, 14, 15:
# TTLword 29206

#TTLword 16898

# 2, 3, 10, 13, 14, 15:
#TTLword 29190

#TTLmask 131071
Cycles 10
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

if port729diag:
    switch_729_port("diag", "on")
else:
    switch_729_port("diag", "off")

if port729tips:
    switch_729_port("tips", "on")
else:
    switch_729_port("tips", "off")
    
if shutter_394:
    setTTLOn("32", is_last=False)
else:
    setTTLOff("32", is_last=False)
    
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
#else: 
#    rf_2674_on(0.,-100)
#    setTTLOff("267 4", is_last=False)

getPMTcounts(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
