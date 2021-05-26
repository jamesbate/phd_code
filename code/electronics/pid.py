import numpy as np 
from scipy.integrate import trapezoid  
import matplotlib.pyplot as plt

##-------------------------PARAMETERS------------------------##

K_p = 0.9
K_i = 0.1
K_d = 0

t_0 = 0
dt = 0.1
step_num = 100

def SP(t):
    if t > 2:
        return 50
    return 0

def process_from_controller(controller, current_process):
    # return current_process + controller #if want to remove steady state error
    return controller

controller_output_init = 0
process_variable_init = 0

##-----------------------INITIALISATION------------------------##

controller_output = np.array([0]*(step_num+1), dtype = float)
process_variable = np.array([0]*(step_num+1), dtype = float)
error = np.array([0]*(step_num+1), dtype = float)
set_points = np.array([0]*(step_num+1), dtype = float)

time_array = np.arange(t_0, dt*step_num, dt)

def calculate_variables(step_index):
    t = t_0 + dt*step_index
    set_points[step_index] = SP(t)
    if step_index == 0:
        controller_output[0] = controller_output_init
        process_variable[0] = process_variable_init
    
    error[step_index] = set_points[step_index] - process_variable[step_index]
    controller_output[step_index+1] = PID_update(step_index, K_p, K_i, K_d)
    process_variable[step_index + 1] = process_from_controller(controller_output[step_index+1], process_variable[step_index])
    print_variables(step_index)


def PID_update(step_index, K_p, K_i, K_d):
    error_array = error[:step_index+1]
    return K_p*error[step_index] + K_i*integral_term(error_array) + K_d*derivative_term(step_index)

def integral_term(error_array):
    return trapezoid(error_array, dx = dt)

def derivative_term(step_index):
    return (error[step_index] - error[step_index - 1])/dt

def print_variables(step_index):
    print('=================TIME {}=================='.format(t_0 + dt*step_index))
    print('\nController Output:\t\t{}\nProcess Variables:\t\t{}\nErrors:\t\t\t\t{}\nSet Points:\t\t\t{}'.format(controller_output[:step_index+1], process_variable[:step_index+1], error[:step_index+1], set_points[:step_index+1]))

##------------------------------NUMERICAL INTEGRATION---------------------------##


for step_index in range(step_num):
    calculate_variables(step_index)

plt.plot(time_array, controller_output[:-1], label = 'Control')
plt.plot(time_array, process_variable[:-1], label = 'Process')
#plt.plot(time_array, error[:-1], label = 'Error')
plt.plot(time_array, set_points[:-1], label = 'Set point')
plt.legend()
plt.show()