# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
n_loops=self.set_variable("float","n_loops",1,1,500000)

p729_pulse=self.set_variable("bool","p729_pulse",0)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)

# Raman pulse 
pulse_393=self.set_variable("bool","pulse_393",1)
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)
# ion analys
do_pipulse=self.set_variable("bool","do_pipulse",0)
pitime_carrier=self.set_variable("float","pitime_carrier",2.,0,2e5)
do_pihalf=self.set_variable("bool","do_pihalf",0)
qubit_pihalf=self.set_variable("float","qubit_pihalf",2.,0,2e5)

analyse_ion=self.set_variable("bool","analyse_ion",1)
new_zealand=self.set_variable("float","new_zealand",2.,0,2e5)
phase=self.set_variable("float","phase",0.,0,50)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

# sideband cooling
sb_cool_com=self.set_variable("bool","sb_cool_com",0)
#sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
SBCool_time=self.set_variable("float","SBCool_time",2000.000000,1,2e5)
sb_cool_rad1=self.set_variable("bool","sb_cool_rad1",0)
sb_cool_rad2=self.set_variable("bool","sb_cool_rad2",0)
SBCool_time_rad=self.set_variable("float","SBCool_time_rad",5000.000000,1,2e5)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)
repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)


# delays during the experiment
delay=self.set_variable("float","delay",2,0,500000)
repump_length=self.set_variable("float","repump_length854",20.000000,1,2e5)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
mes_type=self.set_variable("float","mes_type",0,0,2e5)


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
#ttl_pulse("31",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
InitPulse(50)


delay = 2
# rf_on(150, -100, dds_address=0, start_time = 0)
#setTTLOn("729_not_393second",0,is_last=True)
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(doppler_length, is_last=False)
    PMTDetection(doppler_length)
    seq_wait(1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
        #ttl_pulse(["854"],repump_length,is_last=False)
    seq_wait(0.1)
    
    if sb_cool_com:
        setTTLOff("729SPswitch",0,is_last=True)
        SBCooling2(length = SBCool_time)
        setTTLOn("729SPswitch",0,is_last=True)
    seq_wait(0.1)
    seq_wait(7)
    if sb_cool_rad1:
        SBCooling2(length = SBCool_time_rad, transition="sideband_cool_rad1")
    if sb_cool_rad2:
        SBCooling2(length = SBCool_time_rad, transition="sideband_cool_rad2")
    seq_wait(0.1)
    seq_wait(7)
    if p729_pulse:
        setTTLOff("729SPswitch",0,is_last=True)
        rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
        setTTLOn("729SPswitch",0,is_last=True)
        seq_wait(delay)
    if pulse_393:
        seq_wait(delay)
        if 1:#(mes_type >5):
            RamanPulse(raman_length)
        seq_wait(delay)
    if analyse_ion:
        do_pipulse = 1
        do_pihalf =1
        #pitime_carrier = 1.0
        #qubit_pihalf = 0.5
    if do_pihalf: #mes_type % 3 == 2:
        setTTLOn("729SPswitch",0,is_last=True)
        rf_pulse(qubit_pihalf, 0*3.14159*0.25, ion=1, transition_param='729_qubit', is_last=True, address=1)	   #sigma y
        seq_wait(1)
        setTTLOff("729SPswitch",0,is_last=True)
        seq_wait(1)
    if(do_pipulse):
        #seq_wait(1000) # new zealand
        setTTLOn("729SPswitch",0,is_last=True)
        rf_pulse(pitime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
        seq_wait(delay)
        setTTLOff("729SPswitch",0,is_last=True)
        seq_wait(1)
    if analyse_ion:
        setTTLOn("729SPswitch",0,is_last=True)
        seq_wait(new_zealand) # new zealand
        rf_pulse(pitime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
        seq_wait(delay)
        rf_pulse(qubit_pihalf, phase*3.14159*0.5, ion=1, transition_param='729_qubit', is_last=True, address=1)	 
        seq_wait(delay)
        setTTLOff("729SPswitch",0,is_last=True)
        seq_wait(delay)
    ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
    PMTDetection(det_time)
    seq_wait(1)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
