
% initialize
find_ts;
new_t_steps = (t1_st:t2_st);
new_steps = steps(t1_st:t2_st);

std_err = zeros(1,10);
max_err = zeros(1,10);
rms_err = zeros(1,10);
pearson_corr = zeros(1,10);
n_steps = linspace(1,10,10);

refKnee_new = interp1(t_ref,refKnee,t_angle,'linear');

% for each step
for i = 1:10
	% finding index in steps
    t1_st0 = find(new_steps == i, 1, 'first');
    t1_st1 = find(new_steps == i, 1, 'last');
    
    % finding index in err
    i_0 = find(t_angle>t_steps(t1_st0),1,'first');
    i_1 = find(t_angle>t_steps(t1_st1),1,'first');
    
    % calculate std, RMSE, e_max
    std_err(i) = std(err_angle(i_0:i_1));
    max_err(i) = max(abs(err_angle(i_0:i_1)));
    rms_err(i) = sqrt(mean((err_angle(i_0:i_1)).^2));  % Root Mean Squared Error
    
    % pearson
    r = corr([angle(i_0:i_1)',refKnee_new(i_0:i_1)']);
    
    pearson_corr(i) = r(1,2);
    
end

%% plot
figure();

    subplot(2,1,1);
    hold on;
        plot(n_steps,std_err,'ro-');
        plot(n_steps,max_err,'bs-');
        plot(n_steps,rms_err,'gx-');
    hold off;
    legend('std','max','rmse');
    
    subplot(2,1,2);
        plot(n_steps,pearson_corr,'ko-');
        legend('pearson corr');
%         ylim([0.8,1]);
    
    name_them;

