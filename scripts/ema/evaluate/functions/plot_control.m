figure();

find_ts;

    ax1 = subplot(5,1,1);
        hold on;

            plot(t_control(t1_c:t2_c),Kp_vector(t1_c:t2_c),'b');
            plot(t_control(t1_c:t2_c),Ki_vector(t1_c:t2_c),'r');
            plot(t_control(t1_c:t2_c),Kd_vector(t1_c:t2_c),'g');
            
            plot(t_control(t1_c:t2_c),Kp_hat_vector(t1_c:t2_c),'b','LineWidth',1);
            plot(t_control(t1_c:t2_c),Ki_hat_vector(t1_c:t2_c),'r','LineWidth',1);
            plot(t_control(t1_c:t2_c),Kd_hat_vector(t1_c:t2_c),'g','LineWidth',1);
        hold off;
        
%         Kp_hat_vector(t2_c-2)
%         Ki_vector(t2_c-2)
%         Kd_vector(t2_c-2)
        
        legend('Kp','Ki','Kd');
        xlim([t1_s,t2_s]);
        xlabel('time [s]'); ylabel('PID parameters');

    ax2 = subplot(5,1,2);
        hold on;
            plot(t_u(t1_u:t2_u),u(t1_u:t2_u));
        hold off;
        ylim([-1,1]);
        xlim([t1_s,t2_s]);
        xlabel('time [s]'); ylabel('u');

    ax3 = subplot(5,1,3);
        hold on;
            stairs(t_steps(t1_st:t2_st),steps(t1_st:t2_st));
            plot(t_ref(t1_r:t2_r),refKnee(t1_r:t2_r));
            plot(t_angle(t1_a:t2_a),angle(t1_a:t2_a));
        hold off;
        xlim([t1_s,t2_s]);
        xlabel('time [s]'); ylabel('angle [degrees]');
        legend('steps','ref','meas');

    ax4 = subplot(5,1,4);
        hold on;
            plot(t_angle(t1_a:t2_a),err_angle(t1_a:t2_a));
        xlim([t1_s,t2_s]);
        xlabel('time [s]'); ylabel('error');

    ax5 = subplot(5,1,5);
        hold on;
            plot(t_control(t1_c:t2_c),pw_q(t1_c:t2_c));
            plot(t_control(t1_c:t2_c),pw_h(t1_c:t2_c));
        hold off;
        legend('pw_q','pw_h');
        ylim([0,500]);
        xlim([t1_s,t2_s]);
        xlabel('time [s]'); ylabel('pulse width');
        
        
    linkaxes([ax1,ax2,ax3,ax4,ax5],'x');
    
%     name_them;
    