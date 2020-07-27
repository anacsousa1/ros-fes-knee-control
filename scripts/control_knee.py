#!/usr/bin/env python
import rospy
import ema.modules.control as control
import numpy as np
import dynamic_reconfigure.client as reconfig
import scipy.io as sio
import datetime
import time as tempo

from sensor_msgs.msg import Imu
from ema_common_msgs.msg import Stimulator
# from std_msgs.msg import Int8
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import String

# import utilities
from math import pi
from tf import transformations

# global variables
global angle
global t_angle
global t_ref
global t_curve
global t_gui
global err_angle
global time
global thisKnee
global refKnee
global curveRecr
global integralError
global u
global freq
global pw_q
global pw_h
global current_q
global current_h
global pw_min_q
global pw_min_h
global ESC_init
global ilc_memory
global ilc_i
global control_sel
global channels_sel
global control_onoff
global count_steps
global t_steps

global gui_enable_c
global gui_control_sel
global gui_channels_sel
global gui_step_time
global gui_step_count
global gui_pw_min_q
global gui_pw_min_h
global gui_ref_param
global gui_save_param
global gui_kp
global gui_ki
global gui_kd
global gui_alpha
global gui_beta
global gui_gama
global gui_A
global gui_omega
global gui_phase
global gui_RC
global gui_K
global initTime
global ID_path

gui_enable_c = [False]
gui_control_sel = [0]
gui_pw_min_q = [0]
gui_pw_min_h = [0]
gui_channels_sel = [0]
gui_step_time = [3]
gui_ref_param = ['']
gui_save_param = ['']
gui_kp = [0]
gui_ki = [0]
gui_kd = [0]
gui_alpha = [0]
gui_beta = [0]
gui_gama = [0]
gui_A = [0]
gui_omega = [0]
gui_phase = [0]
gui_RC = [0]
gui_K = [0]
ID_path = "/home/ema/git/ema_controllers/data/00_RC/inverse_dynamics.mat"

current_q = [0, 0]
current_h = [0, 0]
pw_q = [0, 0]
pw_h = [0, 0]
control_sel = 0
pw_min_q = 0
pw_min_h = 0
channels_sel = 0
control_onoff = False


# on_off = False
err_angle = [0]
angle = [0]
refKnee = [0]
curveRecr = [0]
count_steps = [0]

t_angle = [0]
t_ref = [0]
t_curve = [0]
t_gui = [0]
t_steps = [0]
time = [0]

freq = 150.0
thisKnee = [0, 0]
u = [0, 0]
integralError = [0, 0]
ESC_init = [2, 10 * 2 * pi, 0]  # A, freq, phase
ilc_memory = [0, 0]
ilc_i = 0

new_current_quad = 0
new_current_hams = 0
u_i = 0
Kp_vector = [0, 0]
Ki_vector = [0, 0]
Kd_vector = [0, 0]
Kp_hat_vector = [0, 0]
Ki_hat_vector = [0, 0]
Kd_hat_vector = [0, 0]
jcost_vector = [0, 0]
HP_beta = 0.001
ILC_init = [0.2, 0.8, 0.75]  # alpha, beta, gama
ilc_send = [0, 0]
initTime = 0


# get information from GUI
def server_callback(config):
    global new_current_quad
    global new_current_hams
    global control_sel
    global pw_min_q
    global pw_min_h
    global channels_sel
    global control_onoff
    global control_enable_quad
    global control_enable_hams
    global co_activation
    global ilc_memory
    global Kp_now
    global Ki_now
    global Kd_now
    global ES_A_now
    global ES_omega_now
    global ES_phase_now
    global ES_K_now
    global ES_RC_now
    global ILC_alpha_now
    global ILC_beta_now
    global ILC_gama_now

    # get other parameters
    step_time = config['step_time']
    ref_path = config['ref_path']
    save_path = config['save_path']
    co_activation = config['co_activation']

    # get PID parameters
    Kp_now = config['Kp']  # type: object
    Ki_now = config['Ki']
    Kd_now = config['Kd']

    # get ES parameters
    ES_A_now = config['ES_A']
    ES_omega_now = config['ES_omega']
    ES_phase_now = config['ES_phase']
    ES_K_now = config['ES_K']
    ES_RC_now = config['ES_RC']

    # get ILC parameters
    ILC_alpha_now = config['ILC_alpha']
    ILC_beta_now = config['ILC_beta']
    ILC_gama_now = config['ILC_gama']

    # is the controller on?
    if config['enable_control']:

        control_onoff = True
        # consider if muscle is enable
        if config['enable_quad']:
            # update current, odd or even
            if (config['current_quad'] % 2) == 0:
                new_current_quad = config['current_quad']
            else:
                new_current_quad = config['current_quad'] - 1
            control_enable_quad = 1
        else:
            new_current_quad = 0
            control_enable_quad = 0

        if config['enable_hams']:
            # update current, odd or even
            if (config['current_hams'] % 2) == 0:
                new_current_hams = config['current_hams']
            else:
                new_current_hams = config['current_hams'] - 1
            control_enable_hams = 1
        else:
            new_current_hams = 0
            control_enable_hams = 0

        # get ref to get size of memory
        ilc_memory = [[0] * int(step_time * freq), [0] * int(step_time * freq)]

    else:
        control_onoff = False
        new_current_quad = 0
        new_current_hams = 0
        ilc_memory = [0]

    # define controller and leg
    control_sel = config['control_sel']
    channels_sel = config['channels_sel']

    # define min pw
    pw_min_q = config['min_pw_q']
    pw_min_h = config['min_pw_h']

    # update saving vectors
    ts = tempo.time()
    t_gui.append(ts)
    gui_enable_c.append(control_onoff)
    gui_control_sel.append(control_sel)
    gui_pw_min_h.append(pw_min_h)
    gui_pw_min_q.append(pw_min_q)
    gui_channels_sel.append(channels_sel)
    gui_step_time.append(step_time)
    gui_ref_param.append(ref_path)
    gui_save_param.append(save_path)
    gui_kp.append(Kp_now)
    gui_ki.append(Ki_now)
    gui_kd.append(Kd_now)
    gui_alpha.append(ILC_alpha_now)
    gui_beta.append(ILC_beta_now)
    gui_gama.append(ILC_gama_now)
    gui_A.append(ES_A_now)
    gui_omega.append(ES_omega_now)
    gui_phase.append(ES_phase_now)
    gui_K.append(ES_K_now)
    gui_RC.append(ES_RC_now)

    Kp_vector[-1] = Kp_now
    Ki_vector[-1] = Ki_now
    Kd_vector[-1] = Kd_now
    Kp_hat_vector[-1] = Kp_now
    Ki_hat_vector[-1] = Ki_now
    Kd_hat_vector[-1] = Kd_now

# IMU sensor
def imu_callback(data):
    # get timestamp
    time.append(data.header.stamp)

    # get angle position
    qx, qy, qz, qw = data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w
    euler = transformations.euler_from_quaternion([qx, qy, qz, qw], axes='rzyx')

    # z = euler[0]
    y = euler[1]
    x = euler[2]

    # roll: correct issues with more than one axis rotating
    if y >= 0:
        y = (y/pi) * 180  # deg2rad
        if abs(x) > (pi*0.5):
            y = 180-y
    else:
        y = (y/pi) * 180  # deg2rad
        # if abs(x) > (pi*0.5):
        #     y = 180 - y
        # else:
        #     y = 360 + y

    # pitch: correct issues with more than one axis rotating
    x = (x / pi) * 180  # deg2rad/

    # # yaw: correct issues with more than one axis rotating
    # z = (z/pi) * 180  # deg2rad

    # angle error
    err = refKnee[-1] - x
    # err = refKnee[-1] - y

    # append
    ts = tempo.time() - initTime
    angle.append(x)
    # angle.append(y)
    err_angle.append(err)
    t_angle.append(ts)

    # print y


# reference
def reference_callback(data):
    ref = data.data
    refKnee.append(ref)
    ts = tempo.time() - initTime
    t_ref.append(ts)


# reference
def steps_callback(data):
    steps = data.data
    count_steps.append(steps)
    ts = tempo.time() - initTime
    t_steps.append(ts)


# curve recruitment
def curve_callback(data):
    curve = data.data
    curveRecr.append(curve)
    ts = tempo.time() - initTime
    t_curve.append(ts)


def control_knee():
    global t_control
    global stimMsg
    global update_values
    global co_activation
    global new_current_quad
    global new_current_hams
    global control_sel
    global pw_min_h
    global pw_min_q
    global channels_sel
    global control_onoff
    global control_enable_quad
    global control_enable_hams
    global ilc_memory
    global ilc_i
    global Kp_now
    global Ki_now
    global Kd_now
    global ES_A_now
    global ES_omega_now
    global ES_phase_now
    global ES_K_now
    global ES_RC_now
    global ILC_alpha_now
    global ILC_beta_now
    global ILC_gama_now
    global initTime

    # init_variables
    t_control = [0, 0]

    # init control node
    controller = control.Control(rospy.init_node('control', anonymous=False))

    # communicate with the dynamic server
    dyn_params = reconfig.Client('server', config_callback=server_callback)

    # subscribed topics
    sub = dict()
    sub.update({
        'pedal': rospy.Subscriber('imu/pedal', Imu, callback=imu_callback),
        'ref': rospy.Subscriber('ref_channel', Float64, callback=reference_callback),
        'steps': rospy.Subscriber('steps_channel', Float64, callback=steps_callback),
        'curve': rospy.Subscriber('calibration_channel', Float64, callback=curve_callback)
    })
    # sub = {}
    # sub['pedal'] = rospy.Subscriber('imu/pedal', Imu, callback=imu_callback)
    # sub['ref'] = rospy.Subscriber('ref_channel', Float64, callback=reference_callback)
    # sub['steps'] = rospy.Subscriber('steps_channel', Float64, callback=steps_callback)

    # published topics
    pub = dict()
    pub.update({
        'talker': rospy.Publisher('chatter', String, queue_size=10),
        'control': rospy.Publisher('stimulator/ccl_update', Stimulator, queue_size=10),
        'angle': rospy.Publisher('control/angle', Float64, queue_size=10),
        'signal': rospy.Publisher('control/stimsignal', Int32MultiArray, queue_size=10)
    })

    # define loop rate (in hz)
    rate = rospy.Rate(freq)

    # build basic angle message
    angleMsg = Float64()
    # errMsg = Float64()

    # build basic stimulator message
    stimMsg = Stimulator()
    stimMsg.mode = ['single', 'single', 'single', 'single']
    stimMsg.pulse_width = [0, 0, 0, 0]
    stimMsg.pulse_current = [0, 0, 0, 0]
    stimMsg.channel = [1, 2, 3, 4]

    control_sel = 0
    pw_min_h = 0
    pw_min_q = 0
    channels_sel = 0
    control_onoff = False
    ESC_now = [0, 0, 0, 0, 0]
    ILC_now = [0, 0, 0]
    co_activation = False
    initTime = tempo.time()

    # load inverse dynamics
    try:
        ID_data = sio.loadmat(ID_path)
        id_pw = ID_data['id_pw'][0]
        id_angle = ID_data['id_angle'][0]
        # knee_ref = reference_data['knee_ref'][0]
        # loaded = 1
    except:
        print("Ooops, the file you tried to load is not in the folder.")
        # knee_ref = [0, 0, 0, 0]


    # ---------------------------------------------------- start
    while not rospy.is_shutdown():

        thisKnee = angle[-1]
        thisError = err_angle[-1]
        thisRef = refKnee[-1]
        thisTime = tempo.time() - initTime

        # ============================== >controllers start here
        new_kp = Kp_vector[-1]
        new_ki = Ki_vector[-1]
        new_kd = Kd_vector[-1]
        new_kp_hat = Kp_hat_vector[-1]
        new_ki_hat = Ki_hat_vector[-1]
        new_kd_hat = Kd_hat_vector[-1]
        newIntegralError = 0
        new_u = 0
        jcost = controller.jfunction(thisError, freq)  # cost function

        if not co_activation:
            co_act_h = 0
            co_act_q = 0
        else:
            co_act_h = pw_min_h
            co_act_q = pw_min_q

        if control_onoff:

            # Open-loop inverse dynamics
            if control_sel == 0:

                try:
                    res = next(x for x in id_angle if x > thisRef)
                    # print list(id_angle).index(res)
                except StopIteration:
                    res = 0
                    print "Not in recruitment curve"

                new_u = res/500

                # if thisError < 0:
                #     new_u = -1
                # else:
                #     new_u = 1

            # PID
            elif control_sel == 1:
                new_kp = Kp_now
                new_ki = Ki_now
                new_kd = Kd_now

                new_u, newIntegralError = controller.pid(thisError, u[-1], u[-2], integralError[-1], freq, [new_kp,
                                                                                                            new_ki,
                                                                                                            new_kd])

            # PID-ILC
            elif control_sel == 2:
                new_kp = Kp_now
                new_ki = Ki_now
                new_kd = Kd_now

                # first do PID
                thisU_PID, newIntegralError = controller.pid(thisError, u[-1], u[-2], integralError[-1], freq, [new_kp,
                                                                                                                new_ki,
                                                                                                                new_kd])

                # then ILC
                ilc_send[0] = ilc_memory[0][ilc_i]
                ilc_send[1] = ilc_memory[1][ilc_i]

                # only change new_u after the second cycle
                if ilc_memory[0][ilc_i] == 0:
                    new_u = thisU_PID
                else:
                    ILC_now[0] = ILC_alpha_now
                    ILC_now[1] = ILC_beta_now
                    ILC_now[2] = ILC_gama_now
                    new_u = controller.pid_ilc(ilc_send, ILC_now, thisU_PID, ilc_i)

                if new_u > 1:
                    new_u = 1
                elif new_u < -1:
                    new_u = -1

                # update ilc_memory
                ilc_memory[0][ilc_i] = thisError
                ilc_memory[1][ilc_i] = new_u

                # update counter
                if ilc_i < len(ilc_memory[0]) - 1:
                    ilc_i = ilc_i + 1
                else:
                    ilc_i = 0

            # PID-ES
            elif control_sel == 3:
                # calculate new pid parameters using ES
                ESC_now[0] = ES_A_now
                ESC_now[1] = ES_omega_now
                ESC_now[2] = ES_phase_now
                ESC_now[3] = ES_RC_now
                ESC_now[4] = ES_K_now

                new_kp, new_kp_hat = controller.pid_es2(jcost, jcost_vector[-1], Kp_vector[-1], Kp_hat_vector[-1],
                                                        1/freq, thisTime, ESC_now)  # new kp


                ESC_now[0] = ES_A_now/4  # ES_A_now
                # ESC_now[1] = ES_omega_now-2
                ESC_now[2] = ES_phase_now + 0.1745
                # ESC_now[3] = ES_RC_now/2
                # ESC_now[4] = ES_K_now/2
                new_ki, new_ki_hat = controller.pid_es2(jcost, jcost_vector[-1], Ki_vector[-1], Ki_hat_vector[-1],
                                                        1/freq, thisTime, ESC_now)  # new ki

                ESC_now[0] = ES_A_now/16  # ES_A_now
                # ESC_now[1] = ES_omega_now-3
                ESC_now[2] = ES_phase_now + 0.523
                # ESC_now[3] = ES_RC_now/8
                # ESC_now[4] = ES_K_now/8

                new_kd, new_kd_hat = controller.pid_es2(jcost, jcost_vector[-1], Kd_vector[-1], Kd_hat_vector[-1],
                                                        1/freq, thisTime, ESC_now)  # new kd

                # do PID
                new_u, newIntegralError = controller.pid(thisError, u[-1], u[-2], integralError[-1], freq, [new_kp,
                                                                                                            new_ki,

                                                                                                            new_kd])
            # CR
            elif control_sel == 4:  # curve recruitment
                if control_enable_quad == 1:
                    new_u = curveRecr[-1]
                elif control_enable_hams == 1:
                    new_u = -curveRecr[-1]

            # no controller
            else:
                print("No controller was selected.")

                new_kp = 0
                new_ki = 0
                new_kd = 0
                new_kp_hat = 0
                new_ki_hat = 0
                new_kd_hat = 0
                jcost = 0
                newIntegralError = 0
                new_u = 0

        if new_u > 1:
            new_u = 1
        elif new_u < -1:
            new_u = -1

        # update vectors
        Kp_vector.append(new_kp)
        Ki_vector.append(new_ki)
        Kd_vector.append(new_kd)
        Kp_hat_vector.append(new_kp_hat)
        Ki_hat_vector.append(new_ki_hat)
        Kd_hat_vector.append(new_kd_hat)
        jcost_vector.append(jcost)
        integralError.append(newIntegralError)
        u.append(new_u)

        # print refKnee[-1]

        # ============================== controllers end here

        # u to pw
        # new_pw = round(abs(u[-1] * 500) / 10) * 10

        # define pw for muscles
        if u[-1] < 0:
            # new_pw = round(abs(u[-1]) * (500-pw_min_h) + pw_min_h) / 10 * 10  # u to pw
            new_pw = round(abs(u[-1]) * (500-pw_min_h) + pw_min_h)  # u to pw
            pw_h.append(new_pw)
            pw_q.append(co_act_q)
            controlMsg = "angle: %.3f, error: %.3f, u: %.3f (pw: %.1f) (Q), kp,ki,kd = { %.5f, %.5f, %.5f} : "\
                         % (thisKnee, thisError, u[-1], pw_q[-1], Kp_vector[-1], Ki_vector[-1], Kd_vector[-1])

        else:
            new_pw = round(abs(u[-1]) * (500-pw_min_q) + pw_min_q)  # u to pw
            pw_q.append(new_pw)
            pw_h.append(co_act_h)
            controlMsg = "angle: %.3f, error: %.3f, u: %.3f (pw: %.1f) (H), kp,ki,kd = { %.5f, %.5f, %.5f} : "\
                         % (thisKnee, thisError, u[-1], pw_h[-1], Kp_vector[-1], Ki_vector[-1], Kd_vector[-1])

        print(controlMsg)

        # define current for muscles
        current_q.append(new_current_quad)
        current_h.append(new_current_hams)

        # update topics
        if channels_sel == 1:  # right leg
            stimMsg.pulse_width = [0, 0, pw_q[-1], pw_h[-1]]
            stimMsg.pulse_current = [0, 0, current_q[-1], current_h[-1]]
        else:  # left leg
            stimMsg.pulse_width = [pw_q[-1], pw_h[-1], 0, 0]
            stimMsg.pulse_current = [current_q[-1], current_h[-1], 0, 0]

        pub['control'].publish(stimMsg)  # send stim update

        angleMsg.data = thisKnee
        pub['angle'].publish(angleMsg)  # send imu update

        # update timestamp
        # ts = tempo.time()
        t_control.append(thisTime)

        # next iteration
        rate.sleep()

    # ---------------------------------------------------- save everything
    # recreate vectors
    angle_err_lists = [angle, err_angle, t_angle]
    pid_lists = [Kp_vector, Ki_vector, Kd_vector, integralError, t_control]
    stim_lists = [current_q, current_h, pw_q, pw_h, t_control]
    ref_lists = [refKnee, t_ref, curveRecr, t_curve]
    ilc_lists = [ilc_memory, ILC_now, t_control]
    esc_lists = [ESC_now, t_control, Kp_hat_vector, Ki_hat_vector, Kd_hat_vector, jcost_vector]
    control_lists = [u, t_control]
    gui_lists = ([t_gui, gui_enable_c, gui_control_sel, gui_step_time, gui_kp, gui_ki, gui_kd, gui_alpha,
                 gui_beta, gui_gama, gui_A, gui_omega, gui_phase, gui_channels_sel, gui_pw_min_q, gui_pw_min_h, gui_K, gui_RC])
    path_lists = ([gui_ref_param])
    steps_lists = ([t_steps, count_steps])

    # create name of the file
    currentDT = datetime.datetime.now()
    # path_str = "/home/bb8/Desktop/gait_"
    path_str = gui_save_param[-1]
    if channels_sel == 1:  # right leg
        leg_str = '_R_'
    else:  # left leg
        leg_str = '_L_'

    if control_sel == 0:
        control_str = '0_'
    elif control_sel == 1:
        control_str = '1_'
    elif control_sel == 2:
        control_str = '2_'
    elif control_sel == 3:
        control_str = '3_'
    elif control_sel == 4:
        control_str = '4_'
    else:
        control_str = 'x_'

    if not co_activation:
        coact_str = "_noCA"
    else:
        coact_str = "_CA"

    currentDT_str = str(currentDT)
    name_file = path_str + coact_str + leg_str + control_str + currentDT_str + ".mat"

    # save .mat
    sio.savemat(name_file, {'angle_err_lists': angle_err_lists, 'pid_lists': pid_lists, 'stim_lists': stim_lists,
                            'ref_lists': ref_lists, 'ilc_lists': ilc_lists, 'control_lists': control_lists,
                            'esc_lists': esc_lists, 'gui_lists': gui_lists, 'path_lists': path_lists,
                            'steps_lists': steps_lists})


if __name__ == '__main__':
    try:
        control_knee()
    except rospy.ROSInterruptException:
        pass
