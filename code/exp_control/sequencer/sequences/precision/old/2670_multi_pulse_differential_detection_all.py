# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",100.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

# optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

# sideband cooling
sb_cool_com=self.set_variable("bool","sb_cool_com",0)
sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
SBCool_time=self.set_variable("float","SBCool_time",7000.000000,1,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
opt_pump_729=self.set_variable("bool","opt_pump_729",1)
pump_length_729=self.set_variable("float","pump_length_729",200.000000,1,2e5)

# wait time before the experiment
#wait_time=self.set_variable("float","wait_time",1,0,500000)

# UV Laser
#scan_resolution=self.set_variable("float","scan_resolution",0.1,0,100)
pulse_2670=self.set_variable("bool","pulse_2670",1)
power_2670=self.set_variable("float","power_2670",0,-100,0)
pump_length_267=self.set_variable("float","pump_length_267",1000.000000,0,2e6)
pulse_length_267=self.set_variable("float","pulse_length_267",1000.000000,0,2e6)
offset_freq_267=self.set_variable("float","offset_freq_267",400,350,450)
sideband_freq=self.set_variable("float","sideband_freq",1.6,0,10)
sigma_minus=self.set_variable("bool","sigma_minus",0)

# experiment using myTrans
#pulse_729=self.set_variable("bool","pulse_729",1)
port_729=self.set_variable("bool","port_729",0)
#pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

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
B_FIELD = 4.043401  # Gauss
#SPLITTING = 0.59  # MHz / Gauss
mu_bohr = 1.3996246
g_1S0 = -0.00079248
g_3P1 = 3./7
OFFSET = 399.7  # MHz
SIDEBAND = sideband_freq  # MHz
#freq1 = OFFSET - 1.5 * SPLITTING * B_FIELD 
#freq2 = OFFSET - 0.5 * SPLITTING * B_FIELD 
#freq3 = OFFSET + 0.5 * SPLITTING * B_FIELD 
#freq4 = OFFSET + 1.5 * SPLITTING * B_FIELD 
#freq5 = OFFSET + 2.5 * SPLITTING * B_FIELD 
FIXEDOFFSET = offset_freq_267
sigma_sign = -1 if sigma_minus else 1
freq1 = FIXEDOFFSET - sigma_sign * (-1.5 * g_3P1 + 2.5 * g_1S0) * mu_bohr * B_FIELD
freq2 = FIXEDOFFSET - sigma_sign * (-0.5 * g_3P1 + 1.5 * g_1S0) * mu_bohr * B_FIELD
freq3 = FIXEDOFFSET + sigma_sign * (0.5 * g_3P1 + 0.5 * g_1S0) * mu_bohr * B_FIELD
freq4 = FIXEDOFFSET + sigma_sign * (1.5 * g_3P1 - 0.5 * g_1S0) * mu_bohr * B_FIELD
freq5 = FIXEDOFFSET + sigma_sign * (2.5 * g_3P1 - 1.5 * g_1S0) * mu_bohr * B_FIELD
freq6 = offset_freq_267 + sigma_sign * (3.5 * g_3P1 - 2.5 * g_1S0) * mu_bohr * B_FIELD + SIDEBAND
PUMPAMPL = 0;
create_transition('1', {1:1.}, freq1, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('2', {1:1.}, freq2, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('3', {1:1.}, freq3, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('4', {1:1.}, freq4, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('5', {1:1.}, freq5, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('6', {1:1.}, freq6, amplitude=power_2670, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)

</TRANSITIONS>

<SEQUENCE>
if port_729:
    setTTLOn("729 tips", is_last=False)
else:
    setTTLOn("729 diag", is_last=False)

rf_2670_west_on(200, 0)

DopplerCooling(doppler_length, repump_length, take_counts=False)


if opt_pumping:
    OpticalPumping(pump_length)

if sb_cool_com:
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_COM")
    
if sb_cool_strech:
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_Strech")

if opt_pump_729:
    OpticalPumping729(pump_length_729, repump_length)


rf_729(1, 0, "clock1")  # Carrier 0.5 -> 1.5
rf_729(1, 0, "Carrier1")  # Carrier 0.5 -> 2.5
rf_729(1, 0, "BSB")  # BSB 0.5 -> 1.5

PMTDetection(det_time)

#seq_wait(wait_time)
if pulse_2670:
    PUMPWAIT = 300;
    rf_2670(pump_length_267*4.587, 0, "1")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_267*2.645, 0, "2")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_267*1.869, 0, "3")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_267*1.449, 0, "4")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_267*1.183, 0, "5")
    seq_wait(PUMPWAIT)
    
    #rf_2670(pump_length_267, 0, "1")
    #rf_2670(pump_length_267, 0, "2")
    #rf_2670(pump_length_267, 0, "3")
    #rf_2670(pump_length_267, 0, "4")
    #rf_2670(pump_length_267, 0, "5")
    pass

if pulse_2670:
    rf_2670(pulse_length_267, 0, "6")


rf_729(1, 0, "BSB", is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
