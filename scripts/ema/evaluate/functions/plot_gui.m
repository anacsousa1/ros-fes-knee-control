figure();
    ax1 = subplot(4,1,1);
    hold on;
        stairs(t_gui,control_enable,'r');
        stairs(t_gui,control_sel,'b');
        stairs(t_gui,step_time,'g');
    hold off;
    xlim([t_gui(t0_gui),t_gui(end)]); legend('enable','sel','step time');
    xlabel('time [s]'); ylabel('control');    
    
    ax2 = subplot(4,1,2);
    hold on;
        stairs(t_gui,kp,'r');
        stairs(t_gui,ki,'g');
        stairs(t_gui,kd,'b');
    hold off;
    xlim([t_gui(t0_gui),t_gui(end)]); legend('kp','ki','kd');
    xlabel('time [s]'); ylabel('PID param');    
    
    ax3 = subplot(4,1,3);
    hold on;
        stairs(t_gui,alpha,'r');
        stairs(t_gui,beta,'g');
        stairs(t_gui,gama,'b');
    hold off;
    xlim([t_gui(t0_gui),t_gui(end)]); legend('alpha','beta','gama');
    xlabel('time [s]'); ylabel('ILC param');    
    
    ax4 = subplot(4,1,4);
    hold on;
        stairs(t_gui,A,'r');
        stairs(t_gui,omega,'g');
        stairs(t_gui,phase,'b');
    hold off;
    xlim([t_gui(t0_gui),t_gui(end)]); legend('A','omega','phase');
    xlabel('time [s]'); ylabel('ESC param');   
    
    
    linkaxes([ax1,ax2,ax3,ax4],'x');