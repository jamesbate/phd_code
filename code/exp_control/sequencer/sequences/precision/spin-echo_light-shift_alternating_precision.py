# Alternating Spin Echo experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",100.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

# optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

# sideband cooling
sb_cool=self.set_variable("bool","sb_cool",0)
SBCool_time=self.set_variable("float","SBCool_time",5000.000000,1,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
opt_pump_729=self.set_variable("bool","opt_pump_729",1)
pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)

# experiment using myTrans
pulse_729_1=self.set_variable("bool","pulse_729_1",1)
wait_time=self.set_variable("float","wait_time",1,0,500000)
pulse_729_2=self.set_variable("bool","pulse_729_2",1)
light_shift_pulse=self.set_variable("bool","light_shift_pulse",1)
pulse_729_3=self.set_variable("bool","pulse_729_3",1)
phase_729_3=self.set_variable("float","phase_729_3",0,0,10)
port_729=self.set_variable("bool","port_729",0)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
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
Cycles 50
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>
if port_729:
    setTTLOn("729 tips", is_last=False)
else:
    setTTLOn("729 diag", is_last=False)

DopplerCooling(doppler_length, repump_length)

if opt_pumping :
    OpticalPumping(pump_length)

if sb_cool :
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length)

if opt_pump_729 :
    OpticalPumping729(pump_length_729, repump_length)

seq_wait(1)

if pulse_729_1:
    rf_729(0.5, 0, "myTrans", is_last=True)

seq_wait(wait_time)

if pulse_729_2:
    rf_729(1, 0.5, "myTrans", is_last=True)

scan_resolution = 0.1
if light_shift_pulse and abs(phase_729_3 % (2 * scan_resolution) - scan_resolution) < 0.001:
    ttl_pulse(["267 0"], wait_time, is_last=True)
    print "light on"
else:
    seq_wait(wait_time)
    print "light off"

if pulse_729_3:
    rf_729(0.5, phase_729_3, "myTrans", is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
