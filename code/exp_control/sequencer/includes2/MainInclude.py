global oldPMTDetection
def oldPMTDetection(length, doppler=False, no866=False, sigma_mode=False):
    """generate PMT detection event"""

    if sigma_mode:
        ttl_pulse(["397 double", "397 sigma", "mon 2"], length, is_last=False)
    else:
        ttl_pulse(["397 double", "397 pi", "mon 2"], length, is_last=False)
    if doppler:
        ttl_pulse(["397 doppler"], length, is_last=False)
    if not no866:
        ttl_pulse(["866 double", "866 single", "mon 3"], length + 20, is_last=False)
    getPMTcounts(length)

global PMTDetection
def PMTDetection(length, power="detection", background=False, take_counts=True, *args, **kwargs):
    """
    Switch on the dipole lasers and take PMT counts

    Args:
        length: Detection length (time between PMT triggers).
        power: Should be one of "detection", "doppler" or "off". "off" leaves the cooling laser off,
               "doppler" switches it to (usually) lower power for doppler cooling, anything else
               switches it to the power for detection.
        background: If true leaves the repumper off for taking the background noise.
    """

    if args or kwargs:
        print "WARNING: sequence uses old PMTDetection syntax, falling back for compatibility."
        oldPMTDetection(length, *args, **kwargs)
        return

    if power == "off":
        pass
    else:
        ttl_pulse(["397 double", "397 pi"], length, is_last=False)
        if power == "doppler":
            ttl_pulse(["397 doppler"], length, is_last=False)

    if background is False:
        ttl_pulse(["866 double", "866 single", "mon 3"], length + 20, is_last=False)

    if take_counts:
        getPMTcounts(length)
    else:
        seq_wait(length)

global getPMTcounts
def getPMTcounts(length):
    """generate PMT detection event"""
    current_pm_counts = get_return_var("PM Count")
    if current_pm_counts == None:
        current_pm_counts = 0
    add_to_return_list("PM Count", current_pm_counts + 2)

    ttl_pulse(["PMT trigger"], 10, is_last=False)
    ttl_pulse(["PMT trigger"], 10, start_time=length, is_last=True)

def DopplerCooling(length=3000, repump_866 = 20, start_time=0.0, take_counts=True, is_last=True):
    # short repump
    #ttl_pulse(["854 double", "854 single", "mon 4"], repump + length, is_last=False)
    ttl_pulse(["Pi397", "dp397"], length, start_time=start_time, is_last=False)
    ttl_pulse(["866 sw"], length + repump_866, start_time=start_time, is_last=is_last)
    #PMTDetection(length, power="doppler", take_counts=take_counts)

global OpticalPumping
def OpticalPumping(length=50, start_time=0.0, is_last=True):
    ttl_pulse(["dp397", "Sigma397"], length, start_time=start_time, is_last=False)
    ttl_pulse("854 sw",length-10, start_time=start_time, is_last=False)
    ttl_pulse(["866 sw"], length + 20, start_time=start_time, is_last=is_last)
    #ttl_pulse(["Pi397", "dp397"], length, start_time=start_time, is_last=False)
    #ttl_pulse(["866 sw"], length + 20, start_time=start_time, is_last=is_last)
    
def SBCooling(length=1000, reps=10, pumptime=200, repumptime=100, transition="SBC_COM"):
    switch_729_port("diag", "on")
    ttl_pulse(["854 double", "854 single", "mon 4"], length + repumptime, is_last=False)
    ttl_pulse(["854 sbc"], length, is_last=False)
    rf_729(length, 0, transition, is_last=False)
    
    if reps > 1:
        if (reps * pumptime) > length:
            pumptime = length / reps #this should never happen!
        for i in range(1, int(reps) + 1):
            # optical pumping during sbcooling
            OpticalPumping(length=pumptime, start_time=(float(length)/(reps+1))*i, is_last=False)
    
    # after sbcooling once more optical pumping
    OpticalPumping(length=pumptime, start_time=length)
    switch_729_port("diag", "off", is_last=True)
    seq_wait(1)
    
def OpticalPumping729(length, is_last=True, repumptime=100):
    switch_729_port("diag", "on")
    ttl_pulse(["854 double", "854 single", "866 double", "866 single", "mon 3", "mon 4"], length + repumptime, is_last=False)
    rf_729(length, 0, "PumpBoost", is_last=True)
    switch_729_port("diag", "off", is_last=is_last)
    seq_wait(1)
