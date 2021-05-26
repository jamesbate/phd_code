# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
Pulse729_1=self.set_variable("bool","Pulse729_1",1)
Pulse729_2=self.set_variable("bool","Pulse729_2",1)
DoRamanV=self.set_variable("bool","DoRamanV",1)




#MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
#n_loops=self.set_variable("float","n_loops",1,1,500000)

# Raman pulse 
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)
#between_raman=self.set_variable("float","between_raman",50.000000,0,2e5)
# ion analys


# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)
#repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)
pulse729_length=self.set_variable("float","pulse729_length",40.000000,1,2e5)
phase2=self.set_variable("float","phase2",1.000000,-2e5,2e5)
# delays during the experiment
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)
half_wait=self.set_variable("float","half_wait",20.000000,0.1,2e5)

# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
#mes_type=self.set_variable("float","mes_type",0,0,2e5)


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
ttl_pulse("StartSeq",10,is_last=True)
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw","729_not_393second"],is_last=True)
seq_wait(0.1)
#det_time=200
#InitPulse(raman_length)
ttl_pulse("854 sw",repump_length+20,is_last=False)
DopplerCooling(doppler_length, is_last=False)
PMTDetection(doppler_length)
seq_wait(0.1)
if opt_pumping:
    ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
    ttl_pulse("866 sw",pump_length+20,is_last=True)
seq_wait(0.1)
if Pulse729_1:
    setTTLOn("729_not_393second",start_time=0,is_last=True)
    rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    seq_wait(0.1)
    #setTTLOff("729_not_393second",start_time=0,is_last=True)
#seq_wait(0.1)
#seq_wait(half_wait)
if DoRamanV:
    #if Pulse729_1:
        #seq_wait(0.1)
        #setTTLOff("729_not_393second",start_time=0,is_last=True)
    RamanV(raman_length)
seq_wait(half_wait-raman_length)
if Pulse729_2:
    if (not Pulse729_1 or DoRamanV):
        setTTLOn("729_not_393second",start_time=0,is_last=True)
    rf_pulse(pulse729_length, phase2*3.14159, ion=1, transition_param='729_Probe', is_last=True, address=1)
    #setTTLOff("729_not_393second",start_time=0,is_last=True)
    
ttl_pulse(["22"],100,is_last=False)
ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)



seq_wait(2)


TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
