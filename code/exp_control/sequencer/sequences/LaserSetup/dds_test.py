
<VARIABLES>
pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

wait_time=self.set_variable("float","wait_time",1.000000,0.01,2e7)

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

<SEQUENCE>
## Transitions:
# sb_cooling
# PumpBoost
# RSB
# BSB
create_transition('1', {1:1.}, 1.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('2', {1:1.}, 2.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('3', {1:1.}, 3.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('4', {1:1.}, 4.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('5', {1:1.}, 5.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('6', {1:1.}, 6.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('7', {1:1.}, 7.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('8', {1:1.}, 8.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('nine', {1:1.}, 9.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
create_transition('ten', {1:1.}, 10.0, amplitude=0, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)

ttl_pulse(["2"], 10, is_last=True)
#ttl_pulse(["1"], pulse_length, is_last=True)
seq_wait(wait_time)
#ttl_pulse(["1"], pulse_length, is_last=True)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='1', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='2', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='3', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='4', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='5', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='6', is_last=True, address=7)
seq_wait(wait_time)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=0)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=1)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=2)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=3)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=4)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=5)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=6)
rf_pulse(pulse_length, 0, ion=1, transition_param='7', is_last=True, address=7)


#rf_pulse(pulse_length, 0, ion=1, transition_param='PumpBoost', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='myTrans', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='RSB', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='BSB', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='clock1', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='clock2', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='Carrier1', is_last=True, address=1)
#rf_pulse(pulse_length, 0, ion=1, transition_param='Carrier2', is_last=True, address=1)

getPMTcounts(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
