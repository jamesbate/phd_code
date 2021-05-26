# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

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
pump_length_729=self.set_variable("float","pump_length_729",200.000000,1,2e5)

# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)

# UV Laser
scan_resolution=self.set_variable("float","scan_resolution",0.1,0,100)
pulse_2670=self.set_variable("bool","pulse_2670",1)
pulse_length_267=self.set_variable("float","pulse_length_267",1000.000000,0,2e6)
offset_freq_267=self.set_variable("float","offset_freq_267",400,350,450)
sideband_freq=self.set_variable("float","sideband_freq",1.6,0,10)

# experiment using myTrans
pulse_729=self.set_variable("bool","pulse_729",1)
port_729=self.set_variable("bool","port_729",0)
pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

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
#DOasTTLword 1

# 2, 3, 10, 13, 14, 15
# TTLword 29190

# 2, 3, 5, 10, 13, 14, 15
#TTLword 29206

Cycles 50
</PARAMS OVERRIDE>

<TRANSITIONS>
B_FIELD = 3.026160  # Gauss
SPLITTING = 0.59  # MHz / Gauss
OFFSET = offset_freq_267  # MHz
SIDEBAND = sideband_freq  # MHz
freq1 = OFFSET - 1.5 * SPLITTING * B_FIELD + SIDEBAND
freq2 = OFFSET - 0.5 * SPLITTING * B_FIELD + SIDEBAND
freq3 = OFFSET + 0.5 * SPLITTING * B_FIELD + SIDEBAND
freq4 = OFFSET + 1.5 * SPLITTING * B_FIELD + SIDEBAND
freq5 = OFFSET + 2.5 * SPLITTING * B_FIELD + SIDEBAND
freq6 = OFFSET + 3.5 * SPLITTING * B_FIELD + SIDEBAND
create_transition('1', {1:1.}, freq1, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('2', {1:1.}, freq2, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('3', {1:1.}, freq3, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('4', {1:1.}, freq4, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('5', {1:1.}, freq5, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('6', {1:1.}, freq6, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)

</TRANSITIONS>

<SEQUENCE>
if port_729:
    setTTLOn("729 tips", is_last=False)
else:
    setTTLOn("729 diag", is_last=False)

rf_2670_west(200, 0)

DopplerCooling(doppler_length, repump_length)

if opt_pumping :
    OpticalPumping(pump_length)

if sb_cool :
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length)

if opt_pump_729:
    OpticalPumping729(pump_length_729, repump_length)

seq_wait(wait_time)

if pulse_2670:
    rf_2670(pulse_length_267, 0, "1")
    rf_2670(pulse_length_267, 0, "2")
    rf_2670(pulse_length_267, 0, "3")
    rf_2670(pulse_length_267, 0, "4")
    rf_2670(pulse_length_267, 0, "5")
    rf_2670(pulse_length_267, 0, "6")

if pulse_729:
    rf_729(pulse_length, 0, "myTrans", is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
