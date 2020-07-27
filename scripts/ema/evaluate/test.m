% n = length(t_angle)
% length(refKnee)


[r,p] = corrcoef([angle_new;refKnee_new]);

% hold on;
% plot(t_ref(t1_r:t2_r),refKnee(t1_r:t2_r));
% plot(t_angle(t1_a:t2_a),angle(t1_a:t2_a));
% hold off;