

ax1 = subplot(3,1,1);
    plot(t_curve,curveRecr*500);
    xlim([0,t_curve(end)]);

ax2 = subplot(3,1,2);
    plot(t_angle,angle);
    xlim([0,t_angle(end)]);
    
ax3 = subplot(3,1,3);

    part_angle = angle(2*50:3*50);
    new_angle = angle;
    new_angle(new_angle > 6*std(part_angle)) = 0;
    
    ny = find(new_angle(3*50:end)<0,1)+3*50;

    plot(t_angle,new_angle);hold on; plot(t_angle(ny),new_angle(ny),'r*');
    xlim([0,t_angle(end)]);
    
    linkaxes([ax1,ax2,ax3],'x');