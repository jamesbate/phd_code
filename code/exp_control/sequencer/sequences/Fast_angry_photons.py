# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",1000,1,2e5)
n_loops=self.set_variable("float","n_loops",20,1,500000)
#Trigger_UNI_length=self.set_variable("float","Trigger_UNI_length",10,1,2e5)

# Raman pulse 
#pulse_393=self.set_variable("bool","393_pulse",1)
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)

# Doppler cooling
det_time=self.set_variable("float","det_time",200.000000,1,2e5)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)


# delays during the experiment
#delay=self.set_variable("float","delay",2,0,500000)
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)
mes_type=self.set_variable("float","mes_type",0,0,2e5)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))



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
InitPulse()


delay = 2.0
#rf_on(150, -100, dds_address=0, start_time = 0)
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    DopplerCooling(det_time*0.5, is_last=True)
    #PMTDetection(det_time)
    seq_wait(1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump_length,is_last=True)
        #ttl_pulse(["854"],repump_length,is_last=False)
    seq_wait(0.1)
    #if pulse_393:
    seq_wait(delay)
    seq_wait(1)
    #RamanPulse_start-------------------------------------------
    setTTLOn("393DP",0,is_last=False)
    setTTLOff("729_not_393second",0,is_last=True)
    setTTLOn("31",245,is_last=False)
    ttl_pulse("854 sw",raman_length+5,is_last=False)
    ttl_pulse("866 sw",raman_length+5,is_last=False)
    rf_pulse(raman_length, 0., ion=1, transition_param='393_Init', start_time=0.0, is_last=False, address=0)
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #rf_bichro_pulse(raman, 0, ion = 1, transition_param='393_Init', transition2_param='393_Init2',start_time=0.0, is_last=True, address=0, address2=1)
    seq_wait(delay)
    setTTLOff("393DP",0,is_last=False)
    setTTLOn("729_not_393second",0,is_last=True)
    setTTLOff("31",245,is_last=True)
    seq_wait(delay)
    #Raman_pulse end ------------------------------------------
ttl_pulse(["Pi397","dp397","866 sw"],det_time,is_last=False)
PMTDetection(det_time)
seq_wait(1)
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
