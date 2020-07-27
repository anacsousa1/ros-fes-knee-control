
find_ts;

figure();

angle_int = interp1(t_angle,angle, t_steps);
a = 1;
c_coef = zeros(1,11);

t_x2 = t1_st;
for i = 1:11
    t_x1 = t_x2+1; t_x2 = find( steps(t1_st:t2_st) == i, 1);
    v1 = refKnee(t_x1:t_x2); v2 = angle_int(t_x1:t_x2);
    x = corrcoef(v1,v2);
    c_coef(i) = x(2,1);
    
end

plot(c_coef, 'r*-');
ylim([0,1])