#DDS addresses:
#dds729 = 0
#bichromred = 1
#dds729tipsport = 1
#bichromblue = 2
#dds2670 = 3
# 729, tips, bichrom_red, bichrom_blue, 2670, 2674, 2670_east, 2670_west

global dds
dds = { \
    "729": 0, \
    "729_tips": 1, \
    "bichrom_blue": 1, \
    "bichrom_red": 2, \
    "2670": 3, \
    "2670_east": 4, \
    "2670_west": 5, \
    "2674": 6, \
    "ben8": 8 \
    }

# Workaround for damaged DDS boards (0, 2, 3, 4)
# dds["729"] = 7

global rf_729
def rf_729(theta, phi, transition, start_time=0.0, is_last=True):
    rf_pulse(theta, phi * 0.5 * math.pi, ion=1, transition_param=transition, start_time=start_time, is_last=is_last, address=dds["729"])

def rf_729_on(freq, power_dB, start_time=0.0):
    rf_on(freq / 2, power_dB, dds_address=dds["729_tips"], start_time = start_time)

global rf_2670
def rf_2670(theta, phi, transition, start_time=0.0, is_last=True):
    rf_pulse(theta, phi * 0.5 * math.pi, ion=1, transition_param=transition, start_time=start_time, is_last=is_last, address=dds["2670"])

def rf_2670_on(freq, power_dB, start_time=0.0):
    rf_on(freq / 2, power_dB, dds_address=dds["2670"], start_time = start_time)

global rf_2674
def rf_2674(theta, phi, transition, start_time=0.0, is_last=True):
    rf_pulse(theta, phi * 0.5 * math.pi, ion=1, transition_param=transition, start_time=start_time, is_last=is_last, address=dds["2674"])

def rf_2674_on(freq, power_dB, start_time=0.0):
    rf_on(freq / 2, power_dB, dds_address=dds["2674"], start_time = start_time)

global rf_729_tips_on
def rf_729_tips_on(freq=80., power_dB=0., start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["729_tips"], start_time = start_time)

global rf_729_test_on
def rf_729_test_on(freq=10., power_dB=0., start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["729"], start_time = start_time)

global rf_729_bichromat_blue_on
def rf_729_bichromat_blue_on(freq, power_dB, start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["bichrom_blue"], start_time = start_time)

global rf_729_bichromat_red_on
def rf_729_bichromat_red_on(freq, power_dB, start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["bichrom_red"], start_time = start_time)

global rf_2670_east_on
def rf_2670_east_on(freq=200., power_dB=0., start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["2670_east"], start_time = start_time)

global rf_2670_west_on
def rf_2670_west_on(freq=200., power_dB=0., start_time=0.0):
    rf_on(freq, power_dB, dds_address=dds["2670_west"], start_time = start_time)

global switch_729_port
def switch_729_port(port, state = "on", is_last=False):
    if "diag" in port:
        if state == "on":
            setTTLOn("729 diag", is_last=is_last)
        else:
            setTTLOff("729 diag", is_last=is_last)

    if "tips" in port:
        if state == "on":
            setTTLOn("729 tips", is_last=is_last)
            rf_729_tips_on()
        else:
            setTTLOff("729 tips", is_last=is_last)
            rf_729_tips_on(0., -100.)

    if "bichro" in port:
        if state == "on":
            setTTLOn("729 tips", is_last=is_last)
            rf_729_bichromat_blue_on(81.6, -3)
            rf_729_bichromat_red_on(78.4, -3)

def switch_2670_port(port, state = "on"):
    if "west" in port:
        if state == "on":
            rf_2670_west_on()
        else:
            rf_2670_west_on(0., -100.)

    if "east" in port:
        if state == "on":
            rf_2670_east_on()
        else:
            rf_2670_east_on(0., -100.)
