# 729 pulse experiment
# 2010 AS

<VARIABLES>
det_time=self.set_variable("float","det_time",2000.000000,0.01,2e7)
doppler_length=self.set_variable("float","doppler_length",5.000000,1e-3,2e5)
apd_det_time=self.set_variable("float","apd_det_time",1000.000000,0.01,2e7)
SBCool_time=self.set_variable("float","SBCool_time",7000.000000,1e-3,2e5)
SBCool_reps=self.set_variable("float","SBCool_reps",7.000000,1e-3,2e5)
optpump_lgth=self.set_variable("float","optpump_lgth",5.000000,1e-3,2e5)
#pump729_pi=self.set_variable("float","pump729_pi",10.000000,1e-3,2e5)
pump729_length=self.set_variable("float","pump729_length",10.000000,1e-3,2e5)
#pump729_rep=self.set_variable("float","pump729_rep",10.000000,1e-3,2e5)
#pump729_reps=self.set_variable("float","pump729_reps",10.000000,1e-3,2e5)
p729_length=self.set_variable("float","p729_length",10.000000,1e-3,2e5)
p729_wait=self.set_variable("float","p729_wait",10.000000,1e-3,2e5)
#repump_length=self.set_variable("float","repump_length",5.000000,1e-3,2e5)
marker_length=self.set_variable("float","marker_length",0.1100000,1e-3,2e5)

#
#
#exp_counter=self.set_variable("float","exp_counter",1,1,2e5)

#Booleans
sb_cool=self.set_variable("bool","sb_cool",0)
opt_pumping=self.set_variable("bool","opt_pumping",0)
pumping_729=self.set_variable("bool","pumping_729",0)
carrier1=self.set_variable("bool","carrier1",0)
blue_axial_sb=self.set_variable("bool","blue_axial_sb",0)
red_axial_sb=self.set_variable("bool","red_axial_sb",0)
carrier2=self.set_variable("bool","carrier2",0)
carrier3=self.set_variable("bool","carrier3",0)
</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.6f
  meanExc;     0;               %1.3f
  PMTcounts;   1;sum; 		(0:N);		%1.0f
</SAVE FORM>

#<TRANSITIONS>
#t_carr={1 : 1.0, 2: 1.0, 3 : 1.0}
#Carrier=transition(transition_name="Carrier",t_rabi=t_carr,
#                 frequency=freq/2,sweeprange=sspan,amplitude=power_dB,slope_type="blackman",
#                 slope_duration=slope_dur,amplitude2=-1,frequency2=0,port=diag_port) 
#</TRANSITIONS>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode excitation
</PARAMS OVERRIDE>
#AcquisitionMode excitation
#Cycles 100

<SEQUENCE>

# ttl_set("397main_sw",1)
# incl.DopplerCooling(doppler_length)
# ttl_set("397main_sw",0)
  
# ttl_set("dds_sw_393_729",0)     						# initializing the RF switch at output of PB to send RF to the 729 

# if sb_cool :
    # incl.SBCooling_729optpump_pulsed(SBCool_time,SBCool_reps, pump729_pi, pump729_rep, pump729_reps)
    # incl.SBCooling_729optpump(SBCool_time,SBCool_reps, pump729_length)
    # seq_wait(10)

# This is the blue sigma beam optical pumping
# if opt_pumping : incl.OpticalPumping40(optpump_lgth)

# This is the 729 optical pumping. It is called 'carrier2' in order to recognize that this is the transition to use.
# if pumping_729 : incl.OpticalPumping_729_pulsed(pump729_pi, pump729_rep, pump729_reps)
# if pumping_729 : incl.OpticalPumping_729(pump729_length)

# if carrier1 :
    # seq_wait(p729_wait)
    # cqed.rf_393(1,p729_length,1,"carrier1",1)
    # seq_wait(p729_wait)

# if blue_axial_sb :
    # seq_wait(p729_wait)
    # cqed.rf_393(1,p729_length,1,"blue_axial_sb")

# if red_axial_sb :
    # seq_wait(p729_wait)
    # cqed.rf_393(1,p729_length,1,"red_axial_sb")
    
# if carrier2 :
    # seq_wait(p729_wait)
    # cqed.rf_393(1,p729_length,1,"carrier2")
    # seq_wait(p729_wait)

# if carrier3 :
    # seq_wait(p729_wait)
    # cqed.rf_393(1,p729_length,1,"carrier3")
    # seq_wait(p729_wait)

PMTDetection(det_time)

#incl.Repump854(repump_length) # we don't need this anymore since the 854 is on during doppler cooling

</SEQUENCE>


#<AUTHORED BY LABVIEW>
#3
#</AUTHORED BY LABVIEW>
