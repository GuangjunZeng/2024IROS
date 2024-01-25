% 设置螺旋参数
radius_start = 0;        % 起始半径
radius_end = 300;       % 结束半径
z_start = 0;             % 起始高度
z_end = 700;             % 结束高度
turns = 2;              % 螺旋圈数
points_per_turn = 80;   % 每圈的点数
total_points = points_per_turn * turns; % 总点数

% 参数化采样设置
num_integration_points = 10000;  % 高密度采样点用于精确积分计算

% 生成参数t的密集采样点
t_sample = linspace(0, 1, num_integration_points);

% 计算各参数随时间的变化率
dr_dt = radius_end - radius_start;
dtheta_dt = 2*pi*turns;
dz_dt = z_end - z_start;

% 预计算各参数值
r_sample = radius_start + t_sample*dr_dt;
theta_sample = t_sample*dtheta_dt;

% 计算弧长微分 (ds/dt)
dsdt = sqrt(dr_dt^2 + (r_sample*dtheta_dt).^2 + dz_dt^2);

% 计算累积弧长
s = cumtrapz(t_sample, dsdt);
total_arc_length = s(end);

% 生成等距弧长采样点
s_values = linspace(0, total_arc_length, total_points);

% 使用插值找到对应的时间参数t
t_i = interp1(s, t_sample, s_values, 'pchip');

% 计算最终轨迹点参数
radii_i = radius_start + t_i*dr_dt;
theta_i = t_i*dtheta_dt;
z_i = z_start + t_i*dz_dt;

% 转换为笛卡尔坐标系
x = radii_i .* cos(theta_i);
y = radii_i .* sin(theta_i) + 250; % 直接进行Y轴偏移

% 新增：设置起点坐标 (x0, y0)
x0 = -100;  % 新起点X坐标
y0 = -70;  % 新起点Y坐标

x = x + x0;
y = y + y0;

% 存储轨迹（二维坐标）
trajectory = [x', y'];

% 保存轨迹文件
save('F:\capstone2025\small_myRIO_Helmholtz BP_rbf controller\trajectory_helix.mat', 'trajectory');

% 可视化结果
figure;
plot(trajectory(:,1), trajectory(:,2), '-o');
xlabel('X坐标');
ylabel('Y坐标');
title('改进后的等距螺旋轨迹');
axis equal;
grid on;

% 计算实际点间距
dx = diff(trajectory(:,1));
dy = diff(trajectory(:,2));
distances = sqrt(dx.^2 + dy.^2);

% 显示间距统计信息
fprintf('间距统计:\n');
fprintf('平均间距: %.4f\n', mean(distances));
fprintf('最大间距: %.4f\n', max(distances));
fprintf('最小间距: %.4f\n', min(distances));
fprintf('间距标准差: %.4f\n', std(distances));
