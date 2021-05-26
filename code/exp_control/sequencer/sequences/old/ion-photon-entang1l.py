# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",1000.000000,1,2e5)
repump_length=self.set_variable("float","repump_length854",20.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",200.000000,1,2e5)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)
repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)

# Raman pulse 
pulse_393=self.set_variable("bool","393_pulse",1)
raman_length=self.set_variable("float","raman_length",10.000000,0,2e5)


p729_pulse=self.set_variable("bool","p729_pulse",0)
pulse729_length=self.set_variable("float","pulse_length",1000.000000,0,2e5)

# delays during the experiment
delay=self.set_variable("float","delay",1,0,500000)
n_loops=self.set_variable("float","n_loops",20,0,500000)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",250.000000,0.01,2e7)

# ion analys
#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
mes_type=self.set_variable("float","mes_type",0,0,2e5)


analyse_ion=self.set_variable("bool","state_analysis_on",1)

</VARIABLES>
<TRANSITIONS>
</TRANSITIONS>
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

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
#turning all Lasers off
ttl_pulse("31",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
InitPulse()


delay = 4
#rf_on(150, -100, dds_address=0, start_time = 0)
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(doppler_length, is_last=False)
    PMTDetection(doppler_length)
    seq_wait(1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    seq_wait(0.1)
    if pulse_393:
        seq_wait(delay)
        RamanPulse(raman_length)
        seq_wait(delay)
    if p729_pulse:
        rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
        seq_wait(delay)
    if analyse_ion:
        rf_pulse(1., 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
        seq_wait(delay)
        if 0: #mes_type % 3 == 1:
            #rf_pulse(1/2., pi/2, ion=1, transition_param='729_qubit', is_last=True, address=1) # sima x
            seq_wait(delay)
        if 1: #mes_type % 3 == 2:
            rf_pulse(0.5, 0, ion=1, transition_param='729_qubit', is_last=True, address=1)	   #sigma y
            seq_wait(delay)
    ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
    PMTDetection(det_time)
    seq_wait(1)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
