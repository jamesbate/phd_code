# 729 clock experiment
# 06.02.2014 DH/MG
# Description: measure the two clock transitions


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
SBCool_time=self.set_variable("float","SBCool_time",7000.000000,1,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
opt_pump_729=self.set_variable("bool","opt_pump_729",1)
pump_length_729=self.set_variable("float","pump_length_729",175.000000,1,2e5)

# wait time between the pulses
wait_time=self.set_variable("float","wait_time",1,0,500000)

# experiment using myTrans
pulse_729=self.set_variable("bool","pulse_729",1)
pulse2_729=self.set_variable("bool","pulse2_729",1)

# before detecting we can switch on the 854 to see if it can depopulate the D state
repump_test=self.set_variable("bool","repump_test",0)
repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)


meas_type=self.set_variable("float","meas_type",1.000000,1,4)

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
#DOasTTLword 1
#TTLword 29190
Cycles 100
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>
meas_type = meas_type % 4
if meas_type == 0:
    meas_type = 4
assert meas_type in [1., 2., 3., 4.]
if meas_type==1:
    clock="clock1"
    phase=0.5
if meas_type==2:
    clock="clock2"
    phase=1.5
if meas_type==3:
    clock="clock2"
    phase=0.5
if meas_type==4:
    clock="clock1"
    phase=1.5

DopplerCooling(doppler_length, repump_length)

if opt_pumping :
    OpticalPumping(pump_length)

if sb_cool :
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_COM")
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_Strech")

if opt_pump_729 :
    OpticalPumping729(pump_length_729, repump_length)

seq_wait(1)

switch_729_port("diag", "on")

if pulse_729:
    rf_729(0.5, 0, clock, is_last=True)

seq_wait(wait_time)

if pulse2_729:
    rf_729(0.5, phase, clock, is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
