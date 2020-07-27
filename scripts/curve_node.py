#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
import scipy.io as sio
import dynamic_reconfigure.client as reconfig


def gui_callback(config):
    global control_onoff
    global reference_path
    global step_time

    if config['enable_control']:
        control_onoff = True
    else:
        control_onoff = False

    reference_path = config['curve_path']
    step_time = config['step_time']


def get_curve():
    global control_onoff
    global reference_path
    global step_time

    rospy.init_node('curve_node', anonymous=True)

    # published topics
    pub = {}
    pub['calibration'] = rospy.Publisher('calibration_channel', Float64, queue_size=10)

    # communicate with the dynamic server
    dyn_params = reconfig.Client('server', config_callback=gui_callback)

    step_time = 60  # se eu alterar aqui eu preciso alterar no client_node step_t = 6
    length_reference = 12000
    new_freq = length_reference/step_time

    rate = rospy.Rate(new_freq)

    control_onoff = False
    count = 0
    loaded = 0
    number_steps = 0

    while not rospy.is_shutdown():

        if control_onoff:
            # load reference
            if loaded == 0:
                try:
                    reference_data = sio.loadmat(reference_path)
                    pw_ref = reference_data['pw_ref'][0]
                    loaded = 1
                except:
                    print("Ooops, the file you tried to load is not in the folder.")
                    pw_ref = [0, 0, 0, 0]


            if count > len(pw_ref) - 1:
                count = 0
                number_steps = number_steps + 1

            # send messages
            if number_steps == 0:
                pub['calibration'].publish(pw_ref[count])
            else:
                pub['calibration'].publish(0)

            # update counter
            count = count + 1

        else:
            count = 0
            number_steps = 0
            loaded = 0
            pub['calibration'].publish(0)

        rate.sleep()


if __name__ == '__main__':
    try:
        get_curve()
    except rospy.ROSInterruptException:
        pass
