clear;

%% 0,50,100,150,200,250,300,350,400,450,500

%%
n = 200; t1 = 3; y = 0;
t = linspace(0,t1,n*t1);
ref0 = 0*t;
pw_ref = [];

t2 = 1;

t = linspace(0,t2,n*t2);

for i = 1:10
    x = i*0.1;
    ref_x1 = x*t;
    ref_x2 = x*ones(1,length(t));
    ref_x3 = flip(ref_x1);
    pw_ref = [pw_ref ref_x1 ref_x2 ref_x3 ref0];   
    y = y + 3*t2 + t1;
end
t_total = linspace(0,y,length(pw_ref));
plot(t_total,pw_ref);

save("curve_recruitmentU.mat");