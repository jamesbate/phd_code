'''
Created on Feb 6, 2014

Authors:
    Daniel Heinrich
    Michael Guggemos

@brief: This script is used to measure the deviation of the 729 laser with
respect to the quadrupole transition in Ca40. By measuring two different lines
the magnetic field and offset frequency can be calculated and fed back to the
TrICS GUI.
'''

import logging.handlers
import os
import pickle
from time import time

from configobj import ConfigObj

import numpy as np
import trixit as trx


__updated__ = '2015-11-10'


try:
    config = ConfigObj(os.path.dirname(os.path.realpath(__file__)) +
                       '\manager.conf', file_error=True)
except IOError:
    print 'Error: config file not found!'
    raise

script_config = config['ClockScript']

trx.initTrixit()

FITHISTORY = int(script_config["fithistory"])  # minutes
HISTORYFILE = script_config["history_file"]
MAX_RAMSEY_TIME = int(script_config["max_ramsey_time"])
MIN_RAMSEY_TIME = int(script_config["min_ramsey_time"])
P_MAX_DEV = 0.2
B_MIN = 2  # Gauss
B_MAX = 5  # Gauss
B_MAX_DEVIATION = 0.1  # Gauss
B_POLYNOMIAL_ORDER = int(script_config["b_polynomial_order"])
OFFSET_MIN = 400  # MHz
OFFSET_MAX = 500  # MHz
OFFSET_MAX_DEVIATION = 0.1  # MHz
OFFSET_POLYNOMIAL_ORDER = int(script_config["offset_polynomial_order"])
FEEDBACK = True  # should we update the b-field and f_0?
fit_polys_file = script_config["last_fit_polynomials_file"]

clock1 = script_config["clock_transition_name1"]
clock2 = script_config["clock_transition_name2"]

try:
    with open(fit_polys_file, "rb") as f:
        last_parameter_dict = pickle.load(f)
except IOError:
    last_parameter_dict = {}

# Load the last fits polynomials, check the age of the last fit
try:
    last_b_field_poly = last_parameter_dict["last_b_field_poly"]
    last_offset_poly = last_parameter_dict["last_offset_poly"]
    last_fit_time = last_parameter_dict["last_fit_time"]
    ramsey_time = last_parameter_dict["next_ramsey_time"]
    last_reset_time = last_parameter_dict["last_reset_time"]
except KeyError:
    last_b_field_poly = (0,)
    last_offset_poly = (0,)
    last_fit_time = 0
    last_reset_time = time()
    ramsey_time = 10.

if last_fit_time < time() - FITHISTORY * 60:
    ramsey_time = 10.

gS = 2.00225664
gP = 2. / 3.
gD = 1.2003340
muB = 1.3996246

# Get some experimental data from the GUI:
transitions = trx.getTransitions()

clock1_pi_time = float(transitions[clock1].parameters["pi_times"]["0"])
clock2_pi_time = float(transitions[clock2].parameters["pi_times"]["0"])

clock1_m_s = float(transitions[clock1].parameters["mi"])
clock2_m_s = float(transitions[clock2].parameters["mi"])
clock1_m_d = float(transitions[clock1].parameters["mf"])
clock2_m_d = float(transitions[clock2].parameters["mf"])

clock1_freq = float(transitions[clock1].parameters["frequency"])
clock2_freq = float(transitions[clock2].parameters["frequency"])

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t%(message)s\t%(created)f')

# File handler for logging every single clock measurement
fh = logging.FileHandler(script_config['full_history_file'], mode='a')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Rotating file handler for logging successful clock measurements.
# The log is rotated every Sunday (W6).
rfh = logging.handlers.TimedRotatingFileHandler(HISTORYFILE,
                                                when='W6', backupCount=4)
rfh.setFormatter(formatter)


def delta_nu(ramsey_time, pi_time, phi1, phi2):
    '''This function calculates the frequency difference between the laser and
    the probed transition. See e.g. PhD thesis Gerhard Kirchmair, p. 51.
    '''
    return 1 / (2 * np.pi * (ramsey_time + 2 * pi_time / np.pi)) * \
        np.arcsin((phi1 - phi2) / (phi1 + phi2))


def calculate_b_field(f1, mS1, mD1, f2, mS2, mD2):
    '''Calculates the magnetic field from the magnetic quantum numbers and
    frequencies of two transitions.
    '''
    return (f1 - f2) / (muB * ((mD1 - mD2) * gD - (mS1 - mS2) * gS))


def calculate_f_offset(f1, mS1, mD1, f2, mS2, mD2):
    '''Calculates the frequency offset from the magnetic quantum numbers and
    frequencies of two transitions.
    '''
    return f1 - muB * (mD1 * gD - mS1 * gS) * \
        calculate_b_field(f1, mS1, mD1, f2, mS2, mD2)


def get_clock_data(ramsey_time):
    refreeze = trx.getGuiFieldValue("Refreeze_shutter", "channel")

    if refreeze == "1":
        trx.setGuiFieldValue("Refreeze_shutter", "0", "channel")

    trx.loadSequence(script_config["sequence_file"])

    trx.setSeqProp("cycles", "100")
#    trx.setSeqProp("trigger", "line")

    trx.setSeqParam("wait_time", ramsey_time)
    trx.setSeqParam("det_time", 5000.0)

    scan_settings = trx.ScanParamSettings()
    scan_settings.paramName = "seq.meas_type"
    scan_settings.start = 1
    scan_settings.stop = 4
    scan_settings.points = 4

    # Write the transitions to the daemon:
    trx.setTransitionsDaemon(transitions.itervalues())

    data = trx.scan(scan_settings)
    # =========================================================================
    # clock1_p1, clock2_p2, clock2_p1, clock1_p2 = data.meanExcitation
    #
    # print "Probability values:"
    # print clock1_p1
    # print clock1_p2
    # print clock2_p1
    # print clock2_p2
    # =========================================================================

    if refreeze == "1":
        trx.setGuiFieldValue("Refreeze_shutter", "1", "channel")

    return data.meanExcitation

i = 10
while i > 0:
    # This loop is repeated untill we have a successful clock measurement
    i -= 1

    print ramsey_time
    clock1_p1, clock2_p2, clock2_p1, clock1_p2 = get_clock_data(ramsey_time)

    all_checks_passed = True
    raise_ramsey_time = True
    next_ramsey_time = ramsey_time

    try:
        delta_nu1 = delta_nu(ramsey_time, clock1_pi_time, clock1_p1, clock1_p2)
        delta_nu2 = delta_nu(ramsey_time, clock2_pi_time, clock2_p1, clock2_p2)
    except ZeroDivisionError:
        delta_nu1, delta_nu2 = 0, 0

    # print "Deltas:"
    # print delta_nu1
    # print delta_nu2

    freq1 = clock1_freq + delta_nu1
    freq2 = clock2_freq + delta_nu2

    b_field = calculate_b_field(freq1, clock1_m_s, clock1_m_d,
                                freq2, clock2_m_s, clock2_m_d)
    f_offset = calculate_f_offset(freq1, clock1_m_s, clock1_m_d,
                                  freq2, clock2_m_s, clock2_m_d)

    # print "Bfield = ", b_field, "; Offset = ", f_offset

    # Check whether we can raise or should lower the Ramsey time:
    for clock in [clock1_p1, clock1_p2, clock2_p1, clock2_p2]:
        if clock < 2 * P_MAX_DEV or clock > 1 - 2 * P_MAX_DEV:
            raise_ramsey_time = False

        if clock < P_MAX_DEV or clock > 1 - P_MAX_DEV:
            all_checks_passed = False
            print("At least one clock measurement is too close to 0 or 1.")
            next_ramsey_time = int(next_ramsey_time / 2.)
            break

    if raise_ramsey_time:
        next_ramsey_time = int(next_ramsey_time * 1.5)

    if next_ramsey_time > MAX_RAMSEY_TIME:
        next_ramsey_time = MAX_RAMSEY_TIME

    # Check whether the measured b-field is within limits:
    if b_field < B_MIN or b_field > B_MAX:
        all_checks_passed = False
        print("Calculated b field is out of bounds.")

    # Check whether the measured offset is within limits:
    if f_offset < OFFSET_MIN or f_offset > OFFSET_MAX:
        all_checks_passed = False
        print("Calculated offset frequency is out of bounds.")

    now = time()

    if now - last_fit_time < FITHISTORY * 60:
        # The last fit occured just recently, make sure the new values are
        # within its prediction:
        b_field_fit = np.polyval(last_b_field_poly, now)
        offset_fit = np.polyval(last_offset_poly, now)

        if np.abs(b_field_fit - b_field) > B_MAX_DEVIATION:
            all_checks_passed = False
            print("Calculated b field deviates too much from the fit.")

        if np.abs(offset_fit - f_offset) > OFFSET_MAX_DEVIATION:
            all_checks_passed = False
            print(
                "Calculated offset frequency deviates too much from the fit.")

    if all_checks_passed:
        logger.addHandler(rfh)

    logger.critical((
        '{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:+.3f}\t{5:+.3f}\t' +
        '{6:.6f}\t{7:.6f}\t{8:.6f}\t{9:.6f}\t{10:.0f}\t{11}'
    ).format(clock1_p1, clock1_p2, clock2_p1, clock2_p2,
             delta_nu1 * 1000, delta_nu2 * 1000, b_field, f_offset,
             clock1_freq, clock2_freq, ramsey_time, all_checks_passed))

    if all_checks_passed:
        break

    if next_ramsey_time < MIN_RAMSEY_TIME:
        next_ramsey_time = MIN_RAMSEY_TIME
        print "Ramsey time too small, measurement canceled"
        break

    ramsey_time = next_ramsey_time
    print "Bad clock measurement, repeating"

if not all_checks_passed:
    FEEDBACK = False

if FEEDBACK:
    b_field_history, offset_history, ramsey_history, logtime = \
        np.loadtxt(HISTORYFILE, delimiter='\t',
                   usecols=(7, 8, 11, 13), unpack=True, ndmin=2)

    # We only want to use data from the last FITHISTORY minutes or since the
    # last reset for the fit:
    fit_since = max(now - FITHISTORY * 60, last_reset_time)
    index = np.nonzero(logtime > fit_since)
    logtime = logtime[index]
    b_field_history = b_field_history[index]
    offset_history = offset_history[index]
    ramsey_history = ramsey_history[index]

    # Add our new values:
    np.append(logtime, now)
    np.append(b_field_history, b_field)
    np.append(offset_history, f_offset)
    np.append(ramsey_history, ramsey_time)

    # After FITHISTORY minutes, the weight drops exponentially to 0.1:
    alpha = np.log(0.1) / (FITHISTORY * 60)
    exp_weight = np.exp(-alpha * (logtime - now))
    ramsey_weight = ramsey_history / 100
    weight = exp_weight * ramsey_weight

    print "Anzahl fit punkte: {}".format(len(logtime))

    # We want many more points than neccesarry for the fit
    # before we do the fit and update the B field and offset frequency
    # in the GUI:
    max_poly_order = int((len(logtime) - 5) / 5)
    b_poly_order = min(B_POLYNOMIAL_ORDER, max_poly_order)
    offset_poly_order = min(OFFSET_POLYNOMIAL_ORDER, max_poly_order)

    if max_poly_order >= 0:
        b_field_poly = np.polyfit(logtime, b_field_history,
                                  b_poly_order, w=weight)
        offset_poly = np.polyfit(logtime, offset_history,
                                 offset_poly_order, w=weight)

        b_field_fit = np.polyval(b_field_poly, now)
        offset_fit = np.polyval(offset_poly, now)

        last_fit_time = now

        trx.setGuiFieldValue('bField', b_field_fit, 'common_param')
        trx.setGuiFieldValue('offset', offset_fit, 'common_param')

parameter_dump = {}
parameter_dump["last_fit_time"] = last_fit_time
parameter_dump["last_reset_time"] = last_reset_time
parameter_dump["next_ramsey_time"] = next_ramsey_time
try:
    parameter_dump["last_b_field_poly"] = b_field_poly
    parameter_dump["last_offset_poly"] = offset_poly
    parameter_dump["fit_since"] = fit_since
except NameError:
    parameter_dump["last_b_field_poly"] = last_b_field_poly
    parameter_dump["last_offset_poly"] = last_offset_poly

with open(fit_polys_file, "wb") as f:
    pickle.dump(parameter_dump, f)
