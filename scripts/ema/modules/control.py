#!/usr/bin/env python

import rospy
import numpy as np
from math import pi

class Control:


    def __init__(self, config_dict):
        self.config_dict = config_dict


    # PID
    def pid(self, this_error, lastcontrolaction, last_error, lastintegralerror, freq, pid_param):

        Ts = 1/freq
        # PID parameters
        Kp = pid_param[0]
        Ki = pid_param[1]
        Kd = pid_param[2]

        # compute control action
        newIntegralError = lastintegralerror + this_error * Ts
        new_p = Kp * this_error
        new_i = Ki * newIntegralError
        new_d = Kd*(this_error - last_error)/Ts

        new_u = new_p + new_i + new_d  # PID

        # apply control saturation & anti-windup
        if new_u > 1:
            new_u = 1
            newIntegralError = lastintegralerror
        elif new_u < -1:
            new_u = -1
            newIntegralError = lastintegralerror

        # reset integral term for different muscle excitation
        if not np.sign(lastcontrolaction * new_u):
            newIntegralError = 0

        return new_u, newIntegralError


    # ES
    def pid_es(self, jcost, HPparam, ESC, err, last_theta, t, freq):

        # HP parameters
        beta = HPparam

        # ESC parameters
        A = ESC[0]
        omega = ESC[1]
        phase = ESC[2]

        theta = last_theta - beta*(2/A)*np.sin(2*pi*omega*t + phase) * jcost

        if theta < 0:  # garantee that the parameters do not reach zero
            theta = 0

        return theta

    # ES 2 version
    def pid_es2(self, jcost, last_j_cost, last_y, last_uhat, dt, t, ESCparam):

        # ES parameters
        A = ESCparam[0]
        omega = 2*np.pi*ESCparam[1]
        phase = ESCparam[2]
        RC = ESCparam[3]
        K = ESCparam[4]

        # (1) Filter
        hp_result = self.HP_filter_iterative(jcost, last_j_cost, last_y, RC)

        # hp_result = 1

        # (2) *a.sin(wt - phase)
        xi = hp_result * np.sin(omega * t + phase)

        # (3) integrate and apply gain K
        uhat = last_uhat + xi*K*dt

        # (4) + a.sin(wt)
        u = uhat + A*np.sin(omega*t + phase)

        if u < 0:
            u = 0

        if uhat < 0:
            uhat = 0

        return u, uhat


    # HP filter
    def HP_filter_iterative(self, x, last_x, last_y, a):
        y = a*(last_y + x - last_x)

        return y


    # ILC-PID
    def pid_ilc(self, ilc_memory, ilc_param, thisu_pid, ilc_i):

        err_past = ilc_memory[0]
        u_past = ilc_memory[1]

        alpha = ilc_param[0]
        beta = ilc_param[1]
        gama = ilc_param[2]

        ilc_u = (u_past + gama * err_past)

        if ilc_u > 1.5:
            ilc_u = 1.5
        elif ilc_u < -1.5:
            ilc_u = -1.5

        # if np.sign(thisu_pid) == np.sign(ilc_u):
        #     u = alpha*ilc_u + beta * thisu_pid
        # else:
        #     u = thisu_pid

        u = alpha * ilc_u + beta * thisu_pid

        # if ilc_i == 20:
        #     print u_past, ilc_u, thisu_pid, u

        return u


    #jcost
    def jfunction(self, e, freq):

        Ts = 1/freq
        jcost = Ts*e*e

        return jcost


    #old
    def g(self, error):

        Kp = 1/float(5000)
        Ki = 1/float(100000)
        
        # If there is a change of signal, reset
        if ((error[-2] >= 0) and (error[-1] < 0)) or ((error[-2] < 0) and (error[-1] >= 0)):
            errorTemp = [0 for x in range(len(error))]
            errorTemp[-1] = error[-1]
            error = errorTemp
        
        signal = 0.5 + Kp*error[-1]+Ki*sum(error)
        
        # saturation
        if signal > 1:
            signal = 1
            error[-1] = 0
        elif signal < 0:
            signal = 0
            error[-1] = 0
        
        return signal


    def calculate(self, angle, speed, speed_ref, speed_err):
        
        fx_left = self.fx('left', angle, speed, speed_ref)
        fx_right = self.fx('right', angle, speed, speed_ref)
        
        # g = self.g(speed_err)
        g = 1
        
        bool_left = fx_left*g
        bool_right = fx_right*g

        return bool_left, bool_right


    def fx(self, id, angle, speed, speed_ref):
        
        theta = rospy.get_param('/ema/server/')
        dth = (speed/speed_ref)*theta['shift']

        theta_min = theta["angle_"+id+"_min"] - dth
        theta_max = theta["angle_"+id+"_max"] - dth

        # check if angle in range (theta_min, theta_max)
        if theta_min <= angle and angle <= theta_max:
            return 1
        elif theta["angle_"+id+"_min"] > theta["angle_"+id+"_max"]:
            if angle <= theta_min and angle <= theta_max:
                if theta_min <= angle + 360 and angle <= theta_max:
                    return 1
            elif angle >= theta_min and angle >= theta_max:
                if theta_min <= angle and angle <= theta_max + 360:
                    return 1

        # return 0 otherwise
        return 0
