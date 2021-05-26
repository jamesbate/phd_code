def bichromat_729_old(length, phi, transition, sideband_freq, power_blue, power_red, start_time=0.0, is_last=True):
    blue_sb = 80. + sideband_freq
    red_sb = 80. - sideband_freq

    #create_transition('blue', {1:1.}, blue_sb, amplitude=power_blue, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
    #create_transition('red', {1:1.}, red_sb, amplitude=power_red, slope_type="blackman", ion_list={1:0.}, amplitude2=-100, multiplier=1)
    #create_transition('blue', {1:1.}, blue_sb, amplitude=power_blue, multiplier=1)
    #create_transition('red', {1:1.}, red_sb, amplitude=power_red, multiplier=1)

    ttl_pulse(["31"], length, is_last=False)
    #rf_bichro_pulse(length + 3, 0, 1, 'bichromat_blue', 'bichromat_red', \
    #                start_time=start_time, is_last=False, address=1, address2=2)
    #rf_pulse(length, 0, ion=1, transition_param='myTrans', 
    #start_time=start_time, is_last=False, address=2)
    #rf_pulse(length, 0, ion=1, transition_param='myTrans', 
    #start_time=start_time+1, is_last=True, address=1)
    #rf_729(length, phi, transition, start_time=start_time + 2, is_last=is_last)
    
    #seq_wait(500)
    #rf_pulse(length, 0, ion=1, transition_param='myTrans', is_last=True, address=0)
    rf_pulse(length, 0, ion=1, transition_param='myTrans', is_last=True, address=1)
    rf_pulse(length, 0, ion=1, transition_param='BSB', is_last=True, address=2)
    rf_pulse(length, 0, ion=1, transition_param='RSB', is_last=True, address=3)

def bichromat_729(length, phi, transition, blue_trans, red_trans, start_time=0.0, is_last=True):
    set_transition(blue_trans, "bichro")
    set_transition(red_trans, "bichro")
    switch_729_port(["diag", "tips"], "off")
    seq_wait(0.1)
    ttl_pulse(["729 tips"], length + 3, is_last=False)
    rf_bichro_pulse(length + 3, 0, 1, blue_trans, red_trans, \
                    start_time=start_time, is_last=False, address=1, address2=2)
    rf_729(length, phi, transition, start_time=start_time + 2, is_last=is_last)
    switch_729_port("diag", "on")

