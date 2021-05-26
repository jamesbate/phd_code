# Simple Fluorescence experiment
# 19.1.06 TK
# Description: Do nothing to the ions, look with PMT for 
# specified time (Duration)


<VARIABLES>
det_time=self.set_variable("float","det_time",100000.000000,0.01,2e7)
freq=self.set_variable("float","freq",200,100,300)
power_dB=self.set_variable("float","power_dB",0.000000,-100,1)
pulse_length=self.set_variable("float","pulse_length",1,0,1000000)

switchDDS=self.set_variable("bool","switchDDS",0)
</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(1:N);		%1.0f
</SAVE FORM>

<TRANSITIONS>
#t_carr={1 : 1.0, 2: 1.0, 3 : 1.0}
#Carrier=sequence_handler.transition(transition_name="Carrier",t_rabi=t_carr,
#                 frequency=freq,amplitude=power) 
#set_transition(Carrier,"729")

#self.chandler.get_transition(["TRANSITION", "myTrans"])
#self.chandler.get_transition(["RABI", "1:"+str(pulse_length)])
#self.chandler.get_transition(["FREQ", freq*2])
#self.chandler.get_transition(["AMPL", power_dB])

</TRANSITIONS>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode fluorescence
DOasTTLword 1
TTLword 0
Cycles 100
</PARAMS OVERRIDE>

<SEQUENCE>

if switchDDS: rf_729(1, 0, "myTrans")
#if switchDDS: rf_pulse(0, 0, 0, "trans")
else: rf_on(freq,-100, dds_address=0, start_time = 0.0)
# if switchRaman: rf_setRaman(freqRaman,powerRaman)
# else: rf_setRaman(freqRaman,-100)

# incl.PMTDetection(det_time,no_lasers=True)
# ttl_pulse(["866 sw","mon 2"],det_time, is_last=True)

PMTDetection(det_time)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
