# Control strategies for functional electrical stimulation (FES) knee movement in ROS

This work controls knee movement with four FES knee controllers (bang-bang, PID, PID-ILC and PID-extremum seeking). For a further description of materials, libraries and results, see the [tutorial](https://github.com/anacsousa1/ros-fes-knee-control/blob/master/Tutorial.pdf).

The software was tested with Ubuntu 16.04.6 LTS 64-bit Operating System, Python 2.7, and the Robot Operation System (ROS) kinetic distribution.

# Software requirements

- ROS

# Setup and run

1. Change permissions of the stimulator and IMU ports

    ```bash
    sudo chmod 777 /dev/tty/ACM0
    sudo chmod 777 /dev/tty/USB0
    ```

2. Launch the control system in terminal 1

    ```bash
    roslaunch ema_fes_controllers controllers.launch
    ```

3. Launch the user interface in terminal 2

    ```bash
    rqt
    ```

4. Start recording in terminal 3

    ```bash
    roscore record -a
    ```
