
<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

# optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

# sideband cooling
sb_cool_com=self.set_variable("bool","sb_cool_com",0)
sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
SBCool_time=self.set_variable("float","SBCool_time",5000.000000,1,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
opt_pump_729=self.set_variable("bool","opt_pump_729",1)
pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)

# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)

# experiment using myTrans
bichro1_729=self.set_variable("bool","bichro1_729",1)
pulse_2670=self.set_variable("bool","pulse_2670",1)
bichro2_729=self.set_variable("bool","bichro2_729",1)
bichro_length=self.set_variable("float","bichro_length",2000.000000,0,2e6)
pulse_2670_length=self.set_variable("float","pulse_2670_length",2000.000000,0,2e6)
phase_2670=self.set_variable("float","phase_2670",0.000000,0,4)
bichro_phase2=self.set_variable("float","bichro_phase2",0.000000,0,4)
#bichrom_offset=self.set_variable("float","bichrom_offset",80.000000,70,90)
sideband_freq=self.set_variable("float","sideband_freq",1000.000000,0,2e4)
#power_blue=self.set_variable("float","power_blue",0.000000,-100,1)
#power_red=self.set_variable("float","power_red",0.000000,-100,1)

pulse_729=self.set_variable("bool","pulse_729",1)
phase_729=self.set_variable("float","phase_729",0,0,4)
pulse_length_729=self.set_variable("float","pulse_length_729",2000.000000,0,2e5)

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
#OFFSET = bichrom_offset  # MHz
#SIDEBAND = sideband_freq  # MHz
#freq_blue = OFFSET + SIDEBAND
#freq_red = OFFSET - SIDEBAND
#create_transition('bichro_blue', {1:1.}, freq_blue, amplitude=power_blue, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
#create_transition('bichro_red', {1:1.}, freq_red, amplitude=power_red, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)

</TRANSITIONS>

<SEQUENCE>

switch_729_port("diag", "on")
rf_2670_east_on(200. + sideband_freq/2)
rf_2670_west_on(200. - sideband_freq/2)

DopplerCooling(doppler_length, repump_length)

if opt_pumping :
    OpticalPumping(pump_length)

if sb_cool_com:
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_COM")
    
if sb_cool_strech:
    SBCooling(SBCool_time,SBCool_reps,pump_length / 3,repump_length, transition="SBC_Strech")

if opt_pump_729:
    OpticalPumping729(pump_length_729, repump_length)

seq_wait(wait_time)

if bichro1_729:
    bichromat_729(bichro_length, 0, 'myTrans', 'bichro_blue', 'bichro_red')

seq_wait(0.01)
#add 267 stuff here
if pulse_2670:
    rf_2670(pulse_2670_length, phase_2670, "AluPump", is_last=True)

if bichro2_729:
    bichromat_729(bichro_length, bichro_phase2, 'myTrans', 'bichro_blue', 'bichro_red')

if pulse_729:
    switch_729_port("diag", "off")
    switch_729_port("tips", "on")
    rf_729(pulse_length_729, phase_729, 'myTrans',is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
