#!/usr/bin/env python
import rospy
import dynamic_reconfigure.client
from std_msgs.msg import String


def client_callback(config):
    rospy.loginfo("Config set to {enable_control}, {control_sel}, {enable_quad},{enable_hams},{current_quad},"
                  "{current_hams},{step_time}, {ref_path}, {Kp}, {Ki}, {Kd}, {ES_A}, {ES_omega}, {ES_phase}, "
                  "{ILC_alpha}, {ILC_beta}, {ILC_gama}, {co_activation}, {ES_RC}, {ES_K}".format(**config))


if __name__ == "__main__":
    # init node
    rospy.init_node("client_node", anonymous=False)

    # # init client
    client1 = dynamic_reconfigure.client.Client("server", timeout=30, config_callback=client_callback)

    # init gui
    current_0 = 0
    enable_0 = True  # type: bool
    str_0 = "/home/ema/git/ema_controllers/scripts/ema/dataset/senoides1600.mat"
    # str_0 = "/home/ema/git/ema_controllers/scripts/ema/dataset/senoides0a15.mat"
    # str_0 = "/home/ema/git/ema_controllers/scripts/ema/dataset/senoides15a30.mat"
    # str_0 = "/home/ema/git/ema_controllers/scripts/ema/dataset/senoides30a45.mat"
    # str_1 = "/home/ema/Documents/Controllers_tests/test"
    str_1 = "/home/ema/git/ema_controllers/data/test"
    str_2 = "/home/ema/git/ema_controllers/scripts/ema/dataset/curve_recruitmentU.mat"
    # str_1 = "/home/bb8/Documents/subject01"
    step_t = 12  # se eu alterar aqui eu preciso alterar no reference_knee step_time

    Kp_init = 0.001500
    Ki_init = Kp_init/4
    Kd_init = Kp_init/16

    # Kp_init = 0
    # Ki_init = 0
    # Kd_init = 0

    # before I find some init values
    # ES_A_init = 0.002/10
    # ES_omega_init = 7  # 7*1.6
    # ES_phase_init = 0
    # ES_RC_init = 0.000048  # 0.000048/10
    # ES_K_init = 200

    # after I find some init values
    ES_A_init = Kp_init/20
    ES_omega_init = 7  # 7*1.6
    ES_phase_init = 0
    ES_RC_init = 0.00009  # 0.000048  # 0.000048/10
    ES_K_init = 200

    ILC_alpha_init = 0.2
    ILC_beta_init = 1 - ILC_alpha_init
    ILC_gama_init = Kp_init

    # # left
    # min_pw_q = 220
    # min_pw_h = 240
    # i_q = 32
    # i_h = 18

    # # right
    min_pw_q = 20  # 200
    min_pw_h = 250  # 250
    i_q = 32  # 32  # 24
    i_h = 0  # 22  # 24

    client1.update_configuration(
        {"control_sel": 3, "channels_sel": 0, "current_quad": i_q, "current_hams": i_h, "enable_control": False,
         "enable_quad": enable_0, "enable_hams": False, "ref_path": str_0, "step_time": step_t, "Kp": Kp_init,
         "Ki": Ki_init, "Kd": Kd_init, "ES_A": ES_A_init, "ES_omega": ES_omega_init, "ES_phase": ES_phase_init,
         "ES_RC": ES_RC_init,"ES_K": ES_K_init, "curve_path": str_2,
         "ILC_alpha": ILC_alpha_init, "ILC_beta": ILC_beta_init, "ILC_gama": ILC_gama_init, "co_activation": False,
         "save_path": str_1, "min_pw_q": min_pw_q, "min_pw_h": min_pw_h})

    # rate
    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        rate.sleep()
