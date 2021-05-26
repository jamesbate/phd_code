# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
MeasPoints=self.set_variable("float","MeasPoints",50,1,2e5)
n_loops=self.set_variable("float","n_loops",1,1,500000)
TTL_pulse_length=self.set_variable("float","TTL_pulse_length",20.000000,0,2e5)
# Raman pulse 
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)
between_raman=self.set_variable("float","between_raman",50.000000,0,2e5)
synch_time=self.set_variable("float","synch_time",50.000000,0,2e5)
before_loops=self.set_variable("float","before_loops",50.000000,0,2e5)
redundant_wait=self.set_variable("float","redundant_wait",50.000000,0,2e5)
# ion analys


# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)
doppler_length_between=self.set_variable("float","doppler_length_between",5000.000000,1,2e5)
# detection time
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)

#optical pumping with 397 sigma
opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",40.000000,1,2e5)
repump866_length=self.set_variable("float","repump_length866",20.000000,1,2e5)
switchSH=self.set_variable("bool","turn_on_SH",1)

# delays during the experiment
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)


# before detecting we can switch on the 854 to see if it can depopulate the D state
#repump_test=self.set_variable("bool","repump_test",0)
#repump_test_length=self.set_variable("float","repump_test_length",20.000000,1,2e5)

#dummy_var=int(self.set_variable("float","maesurement_type",0,0,1e5))
p729_pulse=self.set_variable("bool","p729_pulse",0)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)

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
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw"])
InitPulse(40)#max(20, raman_length)) #393 S&H
ttl_pulse("854 sw",repump_length,is_last=False)
#DopplerCooling(det_time, is_last=False) #Minimum cooling before Trigger
ttl_pulse(["Pi397", "dp397"], det_time, start_time=0., is_last=False)#Doppler cooling pt 1
ttl_pulse(["866 sw"], det_time + 20, start_time=0., is_last=True) #Doppler cooling pt. 2

PMTDetection(det_time) #At least 200 us (TrICS requirement)
TTLsOn(["Pi397","866 sw","dp397"]) #Let's turn Doppler cooling on until the Trigger arrives
sync_trigger(0x4) #Waiting for trigger from UIBK
ttl_pulse("31",10,is_last=True)
TTLsOff(["Pi397","dp397"]) #Turn off the Doppler cooling pt. 1
seq_wait(repump866_length) #Keep 866 longer on to pump out of P1/2. Turn off the Doppler cooling pt. 2
TTLsOff(["866 sw"])#Turn off the Doppler cooling pt. 3
#ttl_pulse("28",TTL_pulse_length,is_last=True)
#seq_wait(before_loops)
seq_wait(before_loops-10)
for i in range(int(n_loops)):
    ttl_pulse("854 sw",repump_length,is_last=False)
    #DopplerCooling(doppler_length, repump866_length, is_last=True)#Paste DopplerCooling function
    ttl_pulse(["Pi397", "dp397"], doppler_length, start_time=0., is_last=False) #Short Doppler cooling pt. 1
    ttl_pulse(["866 sw"], doppler_length + repump866_length, start_time=0., is_last=True) #Short Doppler cooling pt. 2
    #seq_wait(0.1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    seq_wait(synch_time)
    #ttl_pulse("31",5,is_last=True) #Goes to TimeTagger
    ttl_pulse("28",TTL_pulse_length,is_last=False) #Goes to TimeTagger
    RamanV(raman_length) #Photon 1 generation (synchronized)      Paste Raman generation
    ttl_pulse("854 sw",repump_length,is_last=False)
    #DopplerCooling(doppler_length, repump866_length, is_last=True)
    ttl_pulse(["Pi397", "dp397"], doppler_length_between, start_time=0., is_last=False) #Short Doppler cooling pt. 1
    ttl_pulse(["866 sw"], doppler_length_between + repump866_length, start_time=0., is_last=True) #Short Doppler cooling pt. 2
    #seq_wait(0.1)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    #seq_wait(0.1)
    # Here UIBK is waiting for IQOQI to produce THEIR 2nd photon. (raman_length+10)
    ttl_pulse("32",TTL_pulse_length,is_last=False) #In order to make Victors analysis code working, chang this ch 28 to ch 32
    RamanV(raman_length) #2nd photon generation, not overlapped
    seq_wait(raman_length+redundant_wait) #Do nothing while UIBK is producing THEIR 2nd photon


  
if p729_pulse:
    rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
    seq_wait(1)    
    ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
    PMTDetection(det_time)


TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

#Here is the include function for Raman pulse called Raman V:

def RamanV(raman,delay=0.95, start_time=0.0, last=True):
    setTTLOn("393DP",start_time,is_last=False) #Turn on 393 DP AOM
    #setTTLOn("31",start_time,is_last=False)
    setTTLOff("729_not_393second",start_time,is_last=False) #Because we have 1 PB DDS for both 729 and 393 we need to switch from 729 to 393
    #seq_wait(delay)
    rf_pulse(raman, 0., ion=1, transition_param='393_Raman1', start_time=0.0, is_last=True, address=0) #Do the actual pulse using specific transition field.
    #rf_pulse(raman, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
    #seq_wait(delay)
    setTTLOff("393DP",start_time,is_last=False) #Turn off 393 DP
    setTTLOff("31",start_time,is_last=False) #Some TTL for counter, not used.
    setTTLOn("729_not_393second",start_time,is_last=True) #Turn back to 729.
    seq_wait(delay)



<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
