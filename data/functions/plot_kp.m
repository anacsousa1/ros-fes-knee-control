
find_ts; figure();

t1_c = t1_c + 100;
% t2_c = t2_c - 300;
subplot(3,1,1);
        hold on;
            plot(t_control, Kp_vector);            
            plot(t_control, Kp_hat_vector);
            
        hold off;
        ylim([0,max(Kp_vector)*1.1]);
        
        legend('kp', 'kp_h')
subplot(3,1,2);
        hold on;
            plot(t_control, Ki_vector);            
            plot(t_control, Ki_hat_vector);
            
        hold off;
        ylim([0,max(Kp_vector)*1.1]);
        
        legend('ki', 'ki_h')
subplot(3,1,3);
        hold on;
            plot(t_control, Kd_vector);            
            plot(t_control, Kd_hat_vector);
            
        hold off;
        ylim([0,max(Kp_vector)*1.1]);
        
        legend('kd', 'kd_h')