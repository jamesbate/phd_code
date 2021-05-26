# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# DDS 1
switch729=self.set_variable("bool","switch729",0)
port729diag=self.set_variable("bool","port729diag",0)
#port729tips=self.set_variable("bool","port729tips",0)
freq729=self.set_variable("float","freq729",450.000000,440,640)
power729=self.set_variable("float","power729",0.000000,-100,1)

# DDS 2
switch729bic_blue=self.set_variable("bool","switch729bic_blue",0)
freq729bic_blue=self.set_variable("float","freq729bic_blue",81.000000,70,90)
power729bic_blue=self.set_variable("float","power729bic_blue",0.000000,-100,1)

# DDS 3
switch729bic_red=self.set_variable("bool","switch729bic_red",0)
freq729bic_red=self.set_variable("float","freq729bic_red",79.000000,70,90)
power729bic_red=self.set_variable("float","power729bic_red",0.000000,-100,1)

# DDS 4
switch2670_east=self.set_variable("bool","switch2670_east",0)
freq2670_east=self.set_variable("float","freq2670_east",200.000000,150,250)
power2670_east=self.set_variable("float","power2670_east",0.000000,-100,1)

# DDS 5
switch2670_west=self.set_variable("bool","switch2670_west",0)
freq2670_west=self.set_variable("float","freq2670_west",200.000000,150,250)
power2670_west=self.set_variable("float","power2670_west",0.000000,-100,1)

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
Cycles 100
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>

if port729diag:
    setTTLOn("729 diag", is_last=False)
else:
    setTTLOff("729 diag", is_last=False)

if switch729:
    rf_729_on(freq729,power729)
else:
    rf_729_on(freq729,-100)
    
rf_729_bichromat_blue_on(freq729bic_blue,-100)
rf_729_bichromat_red_on(freq729bic_red,-100)

seq_wait(1000000)
if switch729bic_blue:
    rf_729_bichromat_blue_on(freq729bic_blue,power729bic_blue)
else:
    rf_729_bichromat_blue_on(freq729bic_blue,-100)
seq_wait(1000000)
if switch729bic_red:
    rf_729_bichromat_red(freq729bic_red,power729bic_red)
else:
    rf_729_bichromat_red_on(freq729bic_red,-100)

seq_wait(1000000)
if switch2670_east:
    rf_2670_east_on(freq2670_east, power2670_east)
else:
    rf_2670_east_on(freq2670_east, -100)
    
if switch2670_west:
    rf_2670_west_on(freq2670_west, power2670_west)
else:
    rf_2670_west_on(freq2670_west, -100)

#PMTDetection(det_time)

current_pm_counts = get_return_var("PM Count")
if current_pm_counts == None:
    current_pm_counts = 0
add_to_return_list("PM Count", current_pm_counts + 2)
ttl_pulse(["PMT trigger","mon 1"], 10, is_last=False)
ttl_pulse(["PMT trigger","mon 1"], 10, start_time=det_time, is_last=True)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
