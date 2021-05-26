# General S/D experiment

<VARIABLES>
# initializing the ion to the s state with 854 laser
repump_length=self.set_variable("float","repump_length",20.000000,1,2e5)

# Doppler cooling
doppler_length=self.set_variable("float","doppler_length",5000.000000,1,2e5)


pumplength=self.set_variable("float","pumplength",10.000000,0,2e5)


# wait time before the experiment
wait_time=self.set_variable("float","wait_time",1,0,500000)



# detection time
det_time=self.set_variable("float","det_time",1000.000000,0.01,2e7)

# dummy variable, needed as long as it is not working properly in TrICS
dummy_var=self.set_variable("float","dummy_var",0,0,1e5)

</VARIABLES>

# The save form specifies which data will be saved and how, when a scan is performed.
# If this is omitted a standard form is used
<SAVE FORM>
  .dat   ;   %1.2f
  PMTcounts;   1;sum; 		(1:N);		%1.0f
</SAVE FORM>

# Here the sequence can override program parameters. Syntax follows from "Write Token to Params.vi"
<PARAMS OVERRIDE>
AcquisitionMode fluorescence
#DOasTTLword 1

# 2, 3, 10, 13, 14, 15
# TTLword 29190

# 2, 3, 5, 10, 13, 14, 15
#TTLword 29206

Cycles 250
</PARAMS OVERRIDE>

<TRANSITIONS>
# work around to "error while getting tag" info
</TRANSITIONS>

<SEQUENCE>


DopplerCooling(doppler_length, repump_length)
ttl_pulse(["397 double", "397 pi", "mon 2"], pumplength, is_last=True)


seq_wait(wait_time)

ttl_pulse(["866 double", "866 single"], det_time-1, start_time=1, is_last=False)
#ttl_pulse(["397 double", "397 pi", "mon 2"], 100, is_last=False)

current_pm_counts = get_return_var("PM Count")
if current_pm_counts == None:
    current_pm_counts = 0
add_to_return_list("PM Count", current_pm_counts + 2)

ttl_pulse(["PMT trigger","mon 1"], 5, is_last=False)
ttl_pulse(["PMT trigger","mon 1"], 5, start_time=det_time, is_last=True)

</SEQUENCE>

<AUTHORED BY LABVIEW>
1
</AUTHORED BY LABVIEW>
