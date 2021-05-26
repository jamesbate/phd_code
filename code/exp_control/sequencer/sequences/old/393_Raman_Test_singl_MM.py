# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",20.000000,1,2e5)
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)
raman_length=self.set_variable("float","raman_length",10.000000,1,2e5)
# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

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

# experiment using myTrans
#pulse_729=self.set_variable("bool","pulse_729",1)
#port_729=self.set_variable("bool","port_729",0)
#bichro_729=self.set_variable("bool","bichro_729",0)
#pulse_length=self.set_variable("float","pulse_length",2000.000000,0,2e5)

# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

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
#turning all Lasers off
ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
#TTLsOff("854 sw")
seq_wait(7)

rf_on(150, -100, dds_address=0, start_time = 0)

for i in range(100):
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(doppler_length)
    if opt_pumping:
        ttl_pulse(["397det","Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+20,is_last=True)
    seq_wait(7)
    RamanPulse(raman_length)
    seq_wait(7)

#ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
