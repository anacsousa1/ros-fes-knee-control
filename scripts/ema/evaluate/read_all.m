clear;clc; addpath('functions');

print_control = 1;
print_kp = 0;print_gui = 0;
print_err = 0;
print_corr = 1;

str_coact = 'CA-';
    read_data_gait;

% str_coact = 'CA-';
% for i = 1:6
%     read_data_gait;
% end
% 
% str_coact = 'noCA-';4.4
% for i = 1:8
%     read_data_gait;
% endend

% plot(jcost_vector)

