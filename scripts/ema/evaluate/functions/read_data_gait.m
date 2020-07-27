% clear;clc;
% print_control = 1;
% print_gui = 0;

uiopen;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% adjust parameters
% gui
if isa(gui_lists,'double')
    t_gui = gui_lists(1,:);
    control_enable = gui_lists(2,:);
    control_sel = gui_lists(3,:);
    step_time = gui_lists(4,:);
    kp = gui_lists(5,:);
    ki = gui_lists(6,:);
    kd = gui_lists(7,:);
    alpha = gui_lists(8,:);
    beta = gui_lists(9,:);
    gama = gui_lists(10,:);
    A = gui_lists(11,:);
    omega = gui_lists(12,:);
    phase = gui_lists(13,:);
    channels_sel = gui_lists(14,:);
else
    t_gui = gui_lists{1};
    control_enable = gui_lists{2};
    control_sel = gui_lists{3};
    step_time = gui_lists{4};
    kp = gui_lists{5};
    ki = gui_lists{6};
    kd = gui_lists{7};
    alpha = gui_lists{8};
    beta = gui_lists{9};
    gama = gui_lists{10};
    A = gui_lists{11};
    omega = gui_lists{12};
    phase = gui_lists{13};
    
    t_gui = t_gui(2:end);
end
t0_gui = find(t_gui ~= 0, 1, 'first');
t_gui = t_gui - t_gui(t0_gui);

% angle
if isa(angle_err_lists,'double')
    angle = angle_err_lists(1,:);
    err_angle = angle_err_lists(2,:);
    t_angle = angle_err_lists(3,:);
    
else
    angle = angle_err_lists{1};
    err_angle = angle_err_lists{2};
    t_angle = angle_err_lists{3};
    
    t_angle = t_angle(2:end);
end    
t0_angle = find(t_angle ~= 0, 1, 'first');
t_angle = t_angle - t_angle(t0_angle);
    
% ref
if isa(ref_lists,'double')
    refKnee = ref_lists(1,:);
    t_ref = ref_lists(2,:);
else
    refKnee = ref_lists{1};
    t_ref = ref_lists{2};
    
    t_ref = t_ref(2:end);
end
t0_ref = find(t_ref ~= 0, 1, 'first');
t_ref = t_ref - t_ref(t0_ref);

% pid vectors
if isa(pid_lists,'double')
    Kp_vector = pid_lists(1,:);
    Ki_vector = pid_lists(2,:);
    Kd_vector = pid_lists(3,:);
    integralError = pid_lists(4,:);
    t_control = pid_lists(5,:);
else
    Kp_vector = pid_lists{1};
    Ki_vector = pid_lists{2};
    Kd_vector = pid_lists{3};
    integralError = pid_lists{4};
    t_control = pid_lists{5};
    
    t_pid = t_control(2:end);
end

% es vectors
esc_now = esc_lists{1}; % 2 is t_control
Kp_hat_vector = esc_lists{3};
Ki_hat_vector = esc_lists{4};
Kd_hat_vector = esc_lists{5};
jcost_vector = esc_lists{6};

t0_control = find(t_control ~= 0, 1, 'first');
t_control = t_control - t_control(t0_control);

% stim parameters
if isa(stim_lists,'double')
    current_q = stim_lists(1,:);
    current_h = stim_lists(2,:);
    pw_q = stim_lists(3,:);
    pw_h = stim_lists(4,:);
else
    current_q = stim_lists{1};
    current_h = stim_lists{2};
    pw_q = stim_lists{3};
    pw_h = stim_lists{4};
end

% control
u = control_lists(1,:);
t_u = control_lists(2,:);
t0_u = find(t_u ~= 0, 1, 'first');
t_u = t_u - t_u(t0_u);

% step count
t_steps = steps_lists(1,:);
steps = steps_lists(2,:);
t0_steps = find(t_steps ~= 0, 1, 'first');
t_steps = t_steps - t_steps(t0_steps);

%% plots
% control
if print_control
    plot_control;
end

% pid parameters
if print_gui
    plot_gui;    
end

% err
if print_err
    plot_err;    
end

if print_kp
    plot_kp;
end

if print_corr
    plot_corr;
end

