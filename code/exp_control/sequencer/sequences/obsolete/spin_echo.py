# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)
#freq729=self.set_variable("float","freq729",482.750000,400,600)
#power729=self.set_variable("float","power729",0.000000,-100,1)
#freqRaman=self.set_variable("float","freqRaman",260.000000,230,400)
#powerRaman=self.set_variable("float","powerRaman",0.000000,-100,1)
#switch729=self.set_variable("bool","switch729",0)
#switchRaman=self.set_variable("bool","switchRaman",0)

doppler_length=self.set_variable("float","doppler_length",5000,1,2e5)
repump_length=self.set_variable("float","repump_length",1000,1,2e5)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)
pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)
pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

SBCool_time=self.set_variable("float","SBCool_time",10000.000000,1,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

opt_pumping=self.set_variable("bool","opt_pumping",1)
opt_pump_729=self.set_variable("bool","opt_pump_729",1)
sb_cool=self.set_variable("bool","sb_cool",0)
pulse_729=self.set_variable("bool","pulse_729",1)
pulse2_729=self.set_variable("bool","pulse2_729",1)
shutter_394=self.set_variable("bool","shutter_394",1)
phase_729=self.set_variable("float","phase_729",0,0,10)

wait_time=self.set_variable("float","wait_time",1,0,500000)

modulo_var=self.set_variable("float","modulo_var",0,0,1e5)
dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

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
TTLword 29190
Cycles 1
</PARAMS OVERRIDE>

<SEQUENCE>
setTTLOn("729 diag", is_last=False)

DopplerCooling(doppler_length, repump_length)

if opt_pumping :
	OpticalPumping(pump_length)

if sb_cool :
	SBCooling(SBCool_time,SBCool_reps,pump_length)

if opt_pump_729 :
	OpticalPumping729(pump_length_729, is_last=False)

timingHelper = 2500 - wait_time - 21 - 250
    
if shutter_394:
    if timingHelper > 0:
        if (phase_729 + 0.0001) % (2 * 0.1575) < 0.001:
            print "0"
            ttl_pulse(["32"], 500, is_last=True)
        else: print "1"
        #print (phase_729 + 0.0001) % (2 * 0.1575)
        seq_wait(timingHelper)
seq_wait(1)    
if pulse_729:
    #rf_2674(pulse_length, 0, "myTrans", is_last=False)
    rf_729(0.5, 0, "myTrans", is_last=True)
    #rf_2674(pulse_length, 0, "myTrans", is_last=False)
    #rf_2670(pulse_length, 0, "myTrans")

seq_wait(wait_time)
rf_729(1, math.pi/4, "myTrans", is_last=True)

#if shutter_394:
    #setTTLOn("32", is_last=False)
    
seq_wait(wait_time)

#setTTLOff("32", is_last=False)

if pulse2_729:
    #rf_2674(pulse_length, phase_729, "myTrans", is_last=False)
    rf_729(0.5, phase_729, "myTrans", is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
