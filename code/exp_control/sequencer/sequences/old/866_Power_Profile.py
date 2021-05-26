# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
#repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)

# optical pumping with 397 sigma
#opt_pumping=self.set_variable("bool","opt_pumping",1)
#pv729_pulse=self.set_variable("bool","p729_pulse",1)
#pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)

# sideband cooling
#sb_cool_com=self.set_variable("bool","sb_cool_com",0)
#sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
#SBCool_time=self.set_variable("float","SBCool_time",5000.000000,1,2e5)
#SBCool_reps=self.set_variable("float","SBCool_reps",5,1,2e5)

# optical pumping with 729 on -1/2 to +3/2 transition
#opt_pump_729=self.set_variable("bool","opt_pump_729",1)
#pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)

# wait time before the experiment
#wait_time=self.set_variable("float","wait_time",1,0,500000)
#wait_time2=self.set_variable("float","wait_time2",1,0,500000)

# experiment using myTrans
#pulse_729=self.set_variable("bool","pulse_729",1)
#port_729=self.set_variable("bool","port_729",0)
#bichro_729=self.set_variable("bool","bichro_729",0)
#pulse_length=self.set_variable("float","pulse_length",50000.000000,0,2e5)

# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
#dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

</VARIABLES>

#<TRANSITIONS>
#</TRANSITIONS>

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

<SEQUENCE>
#turning all Lasers off
setTTLOff("854 sw",0,is_last=False)
setTTLOff("Pi397",0,is_last=False)
setTTLOff("Sigma397",0,is_last=False)
setTTLOff("dp397",0,is_last=False)
setTTLOff("397det",0,is_last=False)
setTTLOff("866 sw",0,is_last=False)
setTTLOff("729 sw",0,is_last=True)
seq_wait(10)

#dopplercooling
#ttl_pulse("854 sw",repump_length,is_last=False)
ttl_pulse("Pi397",doppler_length,is_last=False)
ttl_pulse("dp397",doppler_length,is_last=False)
ttl_pulse("866 sw",doppler_length*1.1,is_last=False)
PMTDetection(det_time)
seq_wait(0.1,start_time = doppler_length)

#detection
# ttl_pulse("866 sw",det_time,is_last=False)
# ttl_pulse("Pi397",det_time,is_last=False)
# ttl_pulse("dp397",det_time,is_last=False)
# ttl_pulse("397det",det_time,is_last=False)
# PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
