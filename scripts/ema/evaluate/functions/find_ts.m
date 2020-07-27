
% t1_s = t_gui(end-1);
t1_s = t_gui(3);
t2_s = t_gui(end);

% t1_s = t_gui(end);
% t2_s = t_control(end)-0.2;

dt_s = t2_s-t1_s;

if dt_s > 60    
    t1_c = find(t_control>t1_s,1);
    t2_c = find(t_control>t2_s,1);
    
    t1_r = find(t_ref>t1_s,1);
    t2_r = find(t_ref>t2_s,1);
    
    t1_a = find(t_angle>t1_s,1);
    t2_a = find(t_angle>t2_s,1);
    
    t1_st = find(t_steps>t1_s,1);
    t2_st = find(t_steps>t2_s,1);
    
    t1_u = find(t_u>t1_s,1);
    t2_u = find(t_u>t2_s,1);   
    
else
    
    t1_c = 1;
    t2_c = length(t_control);
    
    t1_r = 1;
    t2_r =  length(t_ref);
    
    t1_a = 1;
    t2_a =  length(t_angle);
    
    t1_st = 1;
    t2_st =  length(t_steps);
    
    t1_u = 1;
    t2_u =  length(t_u);
end