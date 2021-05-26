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
sigma_minus=self.set_variable("bool","sigma_minus",0)

pump_pulses_2670=self.set_variable("bool","pump_pulses_2670",1)
pump_offset_2670=self.set_variable("float","pump_offset_2670",400.000000,350,450)
pump_length_2670=self.set_variable("float","pump_length_2670",1000.000000,0,2e6)
pump_power_2670=self.set_variable("float","pump_power_2670",0,-100,0)

carrier_pulse_2670=self.set_variable("bool","carrier_pulse_2670",0)
carrier_offset_2670=self.set_variable("float","carrier_offset_2670",400.000000,350,450)
carrier_delta_2670=self.set_variable("float","carrier_delta_2670",0.1,0,1)
carrier_length_2670=self.set_variable("float","carrier_length_2670",1000.000000,0,2e6)
carrier_power_2670=self.set_variable("float","carrier_power_2670",0,-100,0)

bsb_pulse_2670=self.set_variable("bool","bsb_pulse_2670",1)
bsb_length_2670=self.set_variable("float","bsb_length_2670",1000.000000,0,2e6)
bsb_power_2670=self.set_variable("float","bsb_power_2670",0,-100,0)
#sideband_freq=self.set_variable("float","sideband_freq",1.6,0,10)

# experiment using myTrans
#pulse_729=self.set_variable("bool","pulse_729",1)
port_729=self.set_variable("bool","port_729",0)
#pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

modulo_var=self.set_variable("float","modulo_var",0,0,1e5)

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
def calculate_alu_pump_freq(mi, mf, bField, offset, polarization="sigma +"):
    if polarization == "sigma +":
        sign = +1
    elif polarization == "sigma -":
        sign = -1
    g_alu_1S0 = -0.00079248
    g_alu_3P1 = 3/7.
    MuBohrDivByPlanck = 1.399624605
    return offset + sign * MuBohrDivByPlanck * (mf * g_alu_3P1 - mi * g_alu_1S0) * bField

B_FIELD = 4.024648  # Gauss
SIDEBAND_FREQ = 1.594780  # MHz

if sigma_minus:
    polarization = "sigma -"
else:
    polarization = "sigma +"

freq1 = calculate_alu_pump_freq(-2.5, -1.5, B_FIELD, pump_offset_2670, polarization)
freq2 = calculate_alu_pump_freq(-1.5, -0.5, B_FIELD, pump_offset_2670, polarization)
freq3 = calculate_alu_pump_freq(-0.5, +0.5, B_FIELD, pump_offset_2670, polarization)
freq4 = calculate_alu_pump_freq(+0.5, +1.5, B_FIELD, pump_offset_2670, polarization)
freq5 = calculate_alu_pump_freq(+1.5, +2.5, B_FIELD, pump_offset_2670, polarization)

modulo_sign = -1 if modulo_var % 2 < 0.0001 else 1
bsb_freq = calculate_alu_pump_freq(+2.5, +3.5, B_FIELD, pump_offset_2670 + SIDEBAND_FREQ, polarization)
carrier_freq = calculate_alu_pump_freq(+2.5, +3.5, B_FIELD, carrier_offset_2670, polarization) + modulo_sign * carrier_delta_2670

PUMPAMPL = pump_power_2670
create_transition('1', {1:1.}, freq1, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('2', {1:1.}, freq2, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('3', {1:1.}, freq3, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('4', {1:1.}, freq4, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('5', {1:1.}, freq5, amplitude=PUMPAMPL, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('Alu_BSB', {1:1.}, bsb_freq, amplitude=bsb_power_2670, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)
create_transition('Alu_Carrier', {1:1.}, carrier_freq, amplitude=carrier_power_2670, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=0.5)

</TRANSITIONS>

<SEQUENCE>
if port_729:
    setTTLOn("729 tips", is_last=False)
else:
    setTTLOn("729 diag", is_last=False)

#rf_2670_west(200, 0)
switch_2670_port("west", "on")

DopplerCooling(doppler_length, repump_length, take_counts=False)

if pump_pulses_2670:
    PUMPWAIT = 300
    rf_2670(pump_length_2670 * 4.587, 0, "1")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_2670 * 2.645, 0, "2")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_2670 * 1.869, 0, "3")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_2670 * 1.449, 0, "4")
    seq_wait(PUMPWAIT)
    rf_2670(pump_length_2670 * 1.183, 0, "5")
    seq_wait(PUMPWAIT)
    pass

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

if carrier_pulse_2670:
    rf_2670(carrier_length_2670, 0, "Alu_Carrier")

if bsb_pulse_2670:
    rf_2670(bsb_length_2670, 0, 'Alu_BSB')


rf_729(1, 0, "BSB", is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
