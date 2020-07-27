legs = {'right', 'left'};
legs_rand = legs(randperm(length(legs)));

CA = {'CA', 'no CA'};
% CA_rand = CA(randperm(length(CA)));

controllers = {'BB','PID','PID-ILC','PID_ES'};
first_leg_rand = controllers(randperm(length(controllers)));

second_leg_rand = controllers(randperm(length(controllers)));


%% print
clc;

fprintf('\n\n- %s: %s %s\n',legs_rand{1}, first_leg_rand{1}, CA{2});
fprintf('- %s: %s  %s\n',legs_rand{1}, first_leg_rand{2}, CA{2});
fprintf('- %s: %s  %s\n',legs_rand{1}, first_leg_rand{3}, CA{2});
fprintf('- %s: %s %s\n',legs_rand{1}, first_leg_rand{4}, CA{2});

controllers = {'PID','PID-ILC','PID_ES'};
first_leg_rand = controllers(randperm(length(controllers)));

fprintf('\n\n- %s: %s %s\n',legs_rand{1}, first_leg_rand{1}, CA{1});
fprintf('- %s: %s  %s\n',legs_rand{1}, first_leg_rand{2}, CA{1});
fprintf('- %s: %s  %s\n',legs_rand{1}, first_leg_rand{3}, CA{1});