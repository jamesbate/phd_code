# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",20.000000,1,2e5)
n_loops=self.set_variable("float","n_loops",1,1,500000)

repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

raman_length=self.set_variable("float","raman_length",10.000000,1,2e5)
# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

# sideband cooling
sb_cool_com=self.set_variable("bool","sb_cool_com",0)
#sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
SBCool_time=self.set_variable("float","SBCool_time",2000.000000,1,2e5)

sb_cool_rad1=self.set_variable("bool","sb_cool_rad1",0)
sb_cool_rad2=self.set_variable("bool","sb_cool_rad2",0)
SBCool_time_rad=self.set_variable("float","SBCool_time_rad",5000.000000,1,2e5)


do_raman=self.set_variable("bool","do_raman",0)
p729_pulse=self.set_variable("bool","p729_pulse",1)
probe729_pulse=self.set_variable("bool","probe729_pulse",0)
Clock1_729_pulse=self.set_variable("bool","Clock1_729_pulse",0)
Clock2_729_pulse=self.set_variable("bool","Clock2_729_pulse",0)
pulse729_length=self.set_variable("float","pulse_length",1000.000000,0,2e5)

repump2=self.set_variable("bool","repump2",0)
repump_length2=self.set_variable("float","repump_length2",20.000000,1,2e5)
# sideband cooling
#sb_cool_com=self.set_variable("bool","sb_cool_com",0)
#sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
#SBCool_time=self.set_variable("float","SBCool_time",5000.000000,1,2e5)
#SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
#opt_pump_729=self.set_variable("bool","opt_pump_729",1)
#pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)

# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)
wait_time2=self.set_variable("float","wait_time2",1,0,500000)

# experiment using myTrans
#pulse_729=self.set_variable("bool","pulse_729",1)
#port_729=self.set_variable("bool","port_729",0)
#bichro_729=self.set_variable("bool","bichro_729",0)
#pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
#dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

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

Cycles 10
</PARAMS OVERRIDE>

#<TRANSITIONS>
# work around to "error while getting tag" info
#</TRANSITIONS>

<SEQUENCE>
ttl_pulse("31",10,is_last=False)
#turning all Lasers off
ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
#InitPulse(max(20, raman_length))
InitPulse(50)
#ttl_pulse("854 sw",repump_length,is_last=False)
#TTLsOff("854 sw")
seq_wait(7)

rf_on(150, -100, dds_address=0, start_time = 0)

ttl_pulse("854 sw",repump_length,is_last=False)
DopplerCooling(doppler_length, is_last=True)
if sb_cool_com:
    SBCooling2(length = SBCool_time)
if sb_cool_rad1:
    SBCooling2(length = SBCool_time_rad, transition="sideband_cool_rad1")
if sb_cool_rad2:
    SBCooling2(length = SBCool_time_rad, transition="sideband_cool_rad2")
seq_wait(0.1)
seq_wait(7)
    
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+20,is_last=True)
    
    seq_wait(7)
    
    
    if do_raman:
        RamanPulse2(raman_length)
    seq_wait(7)
    
    if p729_pulse:
        seq_wait(wait_time)
        rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
    if probe729_pulse:
        seq_wait(wait_time)
        rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
        seq_wait(wait_time2)
    if Clock1_729_pulse:
        seq_wait(wait_time)
        rf_pulse(pulse729_length, 0, ion=1, transition_param='Clock1', is_last=True, address=1)
    if Clock2_729_pulse:
        seq_wait(wait_time)
        rf_pulse(pulse729_length, 0, ion=1, transition_param='Clock2', is_last=True, address=1)
    
if repump2:
    ttl_pulse("854 sw",repump_length2,is_last=False)

ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
