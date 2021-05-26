# Memory Experiment with switch and conversion and swapping

<VARIABLES>
# initializing the ion to the s state with 854 laser


n_loopsAB=self.set_variable("float","n_loopsAB",1,1,500000)
MeasPoints=self.set_variable("float","MeasPoints",500,1,2e5)
n_loops=self.set_variable("float","n_loops",0,0,500000)

final_settings=self.set_variable("bool","final_settings",1)
# Raman pulse 
raman_1i=self.set_variable("bool","raman_1i",1)
raman_2i=self.set_variable("bool","raman_2i",1)
raman_3i=self.set_variable("bool","raman_3i",1)
raman_length=self.set_variable("float","raman_length",50.000000,0,2e5)

# ion analys
do_pipulse=self.set_variable("bool","do_pipulse",0)
pitime_carrier=self.set_variable("float","pitime_carrier",2.,0,2e5)
#pihalftime_carrier=self.set_variable("float","pihalftime_carrier",2.,0,2e5)

do_pihalf=self.set_variable("bool","do_pihalf",0)
pitime_qubit=self.set_variable("float","pitime_qubit",2.,0,2e5)
pihalftime_qubit=self.set_variable("float","pihalftime_qubit",2.,0,2e5)

sb_cool_com=self.set_variable("bool","sb_cool_com",0)
do_MS=self.set_variable("bool","do_MS",0)
MS_pulselength=self.set_variable("float","MS_pulselength",1000.000000,0,2e5)

p729_pulse=self.set_variable("bool","p729_pulse",0)
pulse729_length=self.set_variable("float","pulse729_length",1000.000000,0,2e5)
pitime_probe=self.set_variable("float","pitime_probe",2.,0,2e5)
pihalftime_probe=self.set_variable("float","pihalftime_probe",2.,0,2e5)

#do_echo=self.set_variable("bool","do_echo",0)
#pitime_echo=self.set_variable("float","pitime_echo",2.,0,2e5)


# Doppler cooling

dc_long=self.set_variable("float","dc_long",8000.000000,0.01,2e7)

# # sideband cooling

# #sb_cool_strech=self.set_variable("bool","sb_cool_strech",0)
SBCool_time=self.set_variable("float","SBCool_time",2000.000000,1,2e5)

# detection time
det_time=self.set_variable("float","det_time",2500.000000,0.01,2e7)




#optical pumping with 397 sigma
#opt_pumping=self.set_variable("bool","opt_pumping",1)
pump_length=self.set_variable("float","pump_length",20.000000,1,2e5)
repump_length=self.set_variable("float","repump_length854",20.000000,1,2e5)
short_cool_length=self.set_variable("float","short_cool_length",50.000000,0,2e5)
# delays during the experiment
#delay=self.set_variable("float","delay",2,0,500000)

#switchSH=self.set_variable("bool","turn_on_SH",1)

#MS gate


phase_MS=self.set_variable("float","phase_MS",0,0,2e5)


#probe pulse



#phase_probe=self.set_variable("float","phase_probe",0,0,2e5)


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


#--------------------------------------------------------------------------------------------------------------
<SEQUENCE>
#--------------------------------------------------------------------------------------------------------------
#INFOs
#used ION's (AOD wise): 1 and 3



#729nm transitions:
#qubit:    -1/2  ->  -5/2
#probe:    +1/2  ->  -3/2
#carrier:  -1/2  ->  -3/2

#Missing:
#729_MS:              -1/2  ->  -5/2   detuned


#USED SYNONYMS:
#S : s-1/2
#S': s+1/2
#D : d-5/2
#D': d-3/2



#--------------------------------------------------------------------------------------------------------------
#INIT
#bring to S and S
#--------------------------------------------------------------------------------------------------------------
if final_settings:
    raman_1i = True
    raman_2i = False
    raman_3i = True
    do_MS = True
    do_pipulse = True
    do_pihalf = False
    sb_cool_com = True
    p729_pulse = False
opt_pumping = True
repump866_length = repump_length
delay =0.1
delay_between = 1
#turning all Lasers off
TTLsOff(["854 sw","Pi397","Sigma397","dp397","397det","866 sw", "729SP1"])
seq_wait(1)
aod_delay = 5
init_length =  150

ttl_pulse("21",5,is_last=True)
#DOPPLER COOLING
ttl_pulse("854 sw",dc_long+repump_length,is_last=False)
DopplerCooling(dc_long, is_last=False)
rf_pulse(dc_long, 0., ion=1, transition_param='393_Init', start_time=0., is_last=False, address=1)
rf_pulse(dc_long, 0., ion=1, transition_param='DP_393', start_time=0., is_last=False, address=3)
#rf_pulse(dc_long, 0., ion=1, transition_param='AOD', start_time=0.0, is_last=False, address=2)

PMTDetection(dc_long)

#init: 393 S&H
rf_pulse(init_length+aod_delay, 0., ion=1, transition_param='AOD', start_time=0.0, is_last=False, address=2)
ttl_pulse("StartSeq",init_length+aod_delay-4,is_last=False)
rf_pulse(init_length, 0., ion=1, transition_param='393_Init', start_time=aod_delay, is_last=False, address=1)
rf_pulse(init_length, 0., ion=1, transition_param='DP_393_3', start_time=aod_delay, is_last=True, address=3)

ttl_pulse("854 sw",repump_length,is_last=False)
DopplerCooling(short_cool_length, is_last=True)

if opt_pumping:
    ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
    ttl_pulse("866 sw",pump_length+repump866_length,is_last=True)
    #ttl_pulse(["854"],repump_length,is_last=False)
seq_wait(1)


if sb_cool_com:
    setTTLOn("729SP2",0,is_last=True)
    SBCooling2(length = SBCool_time, pumptime = pump_length)
    setTTLOff("729SP2",0,is_last=True)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump_length,is_last=True)
seq_wait(1)

if 1:# switchSH:
    setTTLOff("17",0.0,is_last=True) #switch to hold
    seq_wait(2)
    setTTLOff("9",0.0,is_last=True) #switch off 806 SP going to ion cavity
    seq_wait(2)


setTTLOff("393DP",0,is_last=True) #off for using pulsebox dds
seq_wait(delay)
setTTLOff("7",0,is_last=True)# RESET LOGIC




#--------------------------------------------------------------------------------------------------------------
#1st loop
#Both photons tried to be done subsequently
#--------------------------------------------------------------------------------------------------------------

for i in range(int(n_loopsAB)):
    setTTLOff("729_not_393second",0,is_last=True)
    ttl_pulse("854 sw",repump_length,is_last=False)
    #DopplerCooling(short_cool_length, is_last=True)
    if opt_pumping:
        ttl_pulse(["Sigma397","dp397"],pump_length,is_last=False)
        ttl_pulse("866 sw",pump_length+repump_length,is_last=True)
    seq_wait(delay)
    
    setTTLOn("31",0,is_last=True)
    setTTLOn("30",0,is_last=True) # switch
    setTTLOn("27",0,is_last=True)
    seq_wait(delay)
    if raman_1i:
        rf_pulse(raman_length+aod_delay, 0., ion=1, transition_param='AOD', start_time=0.0, is_last=False, address=2)
        rf_pulse(raman_length, 0., ion=1, transition_param='DP_393', start_time=aod_delay, is_last=False, address=3)
        rf_bichro_pulse(raman_length, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=aod_delay, is_last=True, address=0, address2=1)
        #setTTLOff("31",0,is_last=True)
        seq_wait(delay_between)
    setTTLOff("27",0,is_last=True)
    setTTLOff("30",0,is_last=True)  # switch
    if raman_2i:
        #setTTLOn("31",0,is_last=True)
        rf_pulse(raman_length+aod_delay, 0., ion=1, transition_param='AOD2', start_time=0.0, is_last=False, address=2)
        rf_pulse(raman_length, 0., ion=1, transition_param='DP_393_2', start_time=aod_delay, is_last=False, address=3)
        #rf_pulse(raman_length, 0., ion=1, transition_param='393_Raman2', start_time=0.0, is_last=True, address=1)
        rf_bichro_pulse(raman_length, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=aod_delay, is_last=True, address=0, address2=1)
        #setTTLOff("31",0,is_last=True)
        seq_wait(delay_between)
    setTTLOn("29",0,is_last=True)
    seq_wait(delay)
    if raman_3i:
        #setTTLOn("31",0,is_last=True)
        rf_pulse(raman_length+aod_delay, 0., ion=1, transition_param='AOD3', start_time=0.0, is_last=False, address=2)
        rf_pulse(raman_length, 0., ion=1, transition_param='DP_393_3', start_time=aod_delay, is_last=False, address=3)
        rf_bichro_pulse(raman_length, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=aod_delay, is_last=True, address=0, address2=1)
        seq_wait(delay)
    setTTLOff("31",0,is_last=True)
    setTTLOff("29",0,is_last=True)
    seq_wait(1)
    setTTLOn("729_not_393second",0,is_last=True)
    seq_wait(1)

    # jump_trigger('label_photon2',0x1)
    # jump_trigger('label_photon1',0x8)
    # jump_trigger('label_MS',0x9)

jump_label('label_analysis')


#--------------------------------------------------------------------------------------------------------------
#PHOTON 2.1
#most likely in D-D' and D-D'
#--------------------------------------------------------------------------------------------------------------

insert_label('label_photon1')
AOD = 'AOD'
DP393 = 'DP_393'
next_label = 'label_analysis_single1'
jump_label('label_2ndloop')

#--------------------------------------------------------------------------------------------------------------
#PHOTON 2.2
#most likely in D-D' and D-D'
#--------------------------------------------------------------------------------------------------------------

insert_label('label_photon2')
AOD = 'AOD3'
DP393 = 'DP_393_3'
next_label = 'label_analysis_single2'
jump_label('label_2ndloop')

#----------------------------------------------------------------------------------------------
#2nd loop

#729 repump
insert_label('label_2ndloop')
setTTLOn("729_not_393second",0,is_last=True)
seq_wait(0.1)
rf_pulse(pitime_qubit,0, ion=1, transition_param='729_qubit', is_last=True, address=1)
seq_wait(1)
rf_pulse(pitime_probe, 0, ion=1, transition_param='729_Probe', is_last=True, address=1)
seq_wait(0.1)
setTTLOff("729_not_393second",0,is_last=True)


#--------------------
#State: D-D' and S-S'
#--------------------

for i in range(int(n_loops)-1):
    ttl_pulse("854 sw",repump_length,is_last=False)
    ttl_pulse("866 sw",repump_length+5,is_last=True)
	#--------------------
	#State: S-S' and S-S'
	#--------------------
    seq_wait(1)
    ttl_pulse("4",raman_length,is_last=False)
    ttl_pulse('27',raman_length,is_last=False) #GATE 
    #ttl_pulse(["4"],raman_length,is_last=False) # Trigger
    rf_pulse(raman_length+aod_delay, 0., ion=1, transition_param=AOD, start_time=0.0, is_last=False, address=2)
    rf_pulse(raman_length, 0., ion=1, transition_param=DP393, start_time=aod_delay, is_last=False, address=3)
    rf_bichro_pulse(raman_length, 0, ion = 1, transition_param='393_Raman1', transition2_param='393_Raman2',start_time=aod_delay, is_last=True, address=0, address2=1)
    
    seq_wait(delay)
	#--------------------
	#State: D-D' and S-S'
	#--------------------    
    jump_trigger(next_label,0x9)
jump_label('label_analysis')


#--------------------------------------------------------------------------------------------------------------
# Starkshift adressed 729 beam for case 1
#State: D-D' and S-S'
#--------------------------------------------------------------------------------------------------------------
insert_label('label_analysis_single1')
AOD = 'AOD'
#--------------------------------------------------------------------------------------------------------------
# Starkshift adressed 729 beam for case 2
#State: S-S' and D-D'
#--------------------------------------------------------------------------------------------------------------
insert_label('label_analysis_single2')
AOD = 'AOD3'
#--------------------------------------------------------------------
#DO Starkshift
setTTLOn("729_not_393second",0,is_last=True)
rf_pulse(pitime_qubit+aod_delay+10, 0., ion=1, transition_param=AOD, start_time=0.0, is_last=False, address=2)
ttl_pulse("729SP2",pitime_qubit+9,start_time=aod_delay,is_last=False)
rf_pulse(pitime_qubit+10, 0., ion=1, transition_param='DP_393_2', start_time=aod_delay, is_last=False, address=3)
rf_pulse(pitime_qubit+10, 0., ion=1, transition_param='393_Raman1', start_time=aod_delay, is_last=False, address=0)
rf_pulse(pitime_qubit, 0, ion=1, transition_param='729_qubit',start_time=aod_delay+1, is_last=True, address=1)

seq_wait(2)
rf_pulse(pitime_probe+aod_delay+10, 0., ion=1, transition_param=AOD, start_time=0.0, is_last=False, address=2)
ttl_pulse("729SP2",pitime_probe+9,start_time=aod_delay,is_last=False)
rf_pulse(pitime_probe+10, 0., ion=1, transition_param='DP_393_2', start_time=aod_delay, is_last=False, address=3)
rf_pulse(pitime_probe+10, 0., ion=1, transition_param='393_Raman1', start_time=aod_delay, is_last=False, address=0)
rf_pulse(pitime_probe, 0, ion=1, transition_param='729_Probe',start_time=aod_delay+1, is_last=True, address=1)

seq_wait(0.1)
#--------------------
#State: S-S' and S-S'
#--------------------
jump_label('label_MS')
    
#--------------------------------------------------------------------------------------------------------------
#MS - GATE
#State: D-D' and D-D'
#--------------------------------------------------------------------------------------------------------------
insert_label('label_analysis')
ttl_pulse("854 sw",repump_length,is_last=False)
ttl_pulse("866 sw",repump_length+5,is_last=True)

insert_label('label_MS')
setTTLOn("729_not_393second",0,is_last=True)
if do_pipulse:
    setTTLOn("729SP2",0,is_last=True)
    rf_pulse(pitime_carrier, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1) #!! was probe
    setTTLOff("729SP2",0,is_last=True)
seq_wait(1)
#--------------------
#State: D-S and D-S
#--------------------

if do_MS:
    setTTLOn("20",0,is_last=True) #bichro
    setTTLOn("729SP2",0,is_last=True)
    seq_wait(5)
    rf_pulse(MS_pulselength, phase_MS*3.141592653*0.25, ion=1, transition_param='729_MS', is_last=True, address=1)
    seq_wait(5)
    setTTLOff("20",0,is_last=True) #bichro
    setTTLOff("729SP2",0,is_last=True)
seq_wait(delay)
setTTLOff("729_not_393second",0,is_last=True)


#--------------------------------------------------------------------------------------------------------------
#ANALYSIS
#--------------------------------------------------------------------------------------------------------------

#insert_label('label_analysis')
seq_wait(delay)

setTTLOn("7",0,is_last=True)# RESET LOGIC
setTTLOn("729_not_393second",0,is_last=True)

if(do_pihalf):
    setTTLOn("729SP2",0,is_last=True)
    rf_pulse(pihalftime_qubit, 0*3.141592653*0.25, ion=1, transition_param='729_qubit', is_last=True, address=1)	   #sigma y
    setTTLOff("729SP2",0,is_last=True)
seq_wait(1)

if p729_pulse:
    setTTLOn("729SP2",0,is_last=True)
    rf_pulse(pulse729_length, 0, ion=1, transition_param='729_Carrier', is_last=True, address=1)
    setTTLOff("729SP2",0,is_last=True)
    seq_wait(delay)

setTTLOn("9",0.0,is_last=True) #switch on again 806 SP going to ion cavity
seq_wait(2)
setTTLOn("17",0.0,is_last=True) #switch to sampling

seq_wait(0.1)
setTTLOff("729SP1",0,is_last=True)
setTTLOff("729SP2",0,is_last=True)

ttl_pulse(["22"],100,is_last=False) #camera    
ttl_pulse(["Pi397","dp397","866 sw","397det"],det_time,is_last=False)
PMTDetection(det_time)
seq_wait(1)
ttl_pulse("29",20,is_last=True)#Reset
TTLsOff(["Pi397","866 sw"])
</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
