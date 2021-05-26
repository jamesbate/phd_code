# 729 pulse experiment
# 16.2.06 TK

<VARIABLES>

# test-tom=self.set_variable("float","test-tom",9000.123456,0.01,2e7)

phase1=self.set_variable("float","phase1",0,-10,10)
phase2=self.set_variable("float","phase2",0,-10,10)
gl_cam_time=self.set_variable("float","gl_cam_time",5000.000000,0,2e7)
det_time=self.set_variable("float","det_time",5000.000000,0.01,2e7)
doppler_length=self.set_variable("float","doppler_length",3000.000000,1,2e5)
pump_length=self.set_variable("float","pump_length",100.000000,1,2e5)
pump_length_729=self.set_variable("float","pump_length_729",500.000000,1,2e5)

pulse_3=self.set_variable("bool","pulse_3",0)
pulse_4=self.set_variable("bool","pulse_4",0)

</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.6f
  meanExc;     0;               %1.3f
  parity;       0;               %1.3f
  pn;   1;elements; 		(0:N);		%1.3f
  StartTime;     0;               %1.3f
  StopTime;     0;               %1.3f
  PMTcounts;   1;elements; 		(0:N);		%1.0f
</SAVE FORM>

<TRANSITIONS>
t_carr={1 : 1.0, 2: 1.0, 3 : 1.0}
#Carrier=transition(transition_name="Carrier",t_rabi=t_carr,
 #                frequency=freq,sweeprange=sspan,amplitude=power_dB,slope_type="blackman",
 #                slope_duration=slope_dur,amplitude2=-1,frequency2=0,port=port_nr) 
#set_transition(Carrier,"729")

</TRANSITIONS>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode excitation
</PARAMS OVERRIDE>

<SEQUENCE>

incl.DopplerCooling40(doppler_length,repump_length)
if opt_pumping : incl.OpticalPumping40(pump_length)
if sb_cool : incl.SBCooling40(SBCool_time,SBCool_reps)
if opt_pump_729 : incl.OpticalPumping40_729(pump_length_729)
else : seq_wait(pump_length_729)

seq_wait(700)

if pulse_1 :  rf_729(1,0.5,0,"carrier1")
    
if pulse_2 : rf_729(1,1,0,"gate")

seq_wait(wait_time)
    
if pulse_3 : rf_729(1,1,phase2*math.pi,"gate")
    
if pulse_4 : rf_729(1,0.5,phase1*math.pi,"carrier1")

incl.PMTDetection(det_time,gl_cam_time)

</SEQUENCE>


<AUTHORED BY LABVIEW>
3
</AUTHORED BY LABVIEW>
