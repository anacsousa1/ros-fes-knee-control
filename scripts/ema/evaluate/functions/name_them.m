    if ((control_sel(end-1)) == 0)
        str_control = 'BB';
    elseif ((control_sel(end-1)) == 1)
        str_control = 'PID';
    elseif ((control_sel(end-1)) == 2)
        str_control = 'ILC';
    elseif ((control_sel(end-1)) == 3)
        str_control = 'ES';   
    else
        str_control = 'ES'; 
    end
    
    if channels_sel(end) == 0 
        str_leg = 'L-';
    elseif channels_sel(end) == 1
        str_leg = 'R-';        
    end
    
%     str_coact = ' CA - ';
    
%     suptitle(strcat(str_leg,str_coact,str_control));
    
    currentFigure = gcf;
    name_x =  strcat(str_leg,str_coact,str_control)
    title(currentFigure.Children(end),name_x);
    
    % save fig
    savefig(strcat(name_x,'.fig'));
    
    % save workspace
    save(strcat(name_x,'.mat')); %, 'std_err', 'max_err', 'rms_err', 'pearson_corr');
    