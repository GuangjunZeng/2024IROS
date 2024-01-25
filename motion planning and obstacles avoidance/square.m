% 定义四个角点的坐标
start_point = [350, 180]; % 右上角
bottom_right = [350, 500]; % 右下角
bottom_left = [-350, 500]; % 左下角
top_left = [-350, 180]; % 左上角

% 将四个点按顺时针顺序排列
square_points = [start_point; bottom_right; bottom_left; top_left; start_point];

% 存储坐标点的矩阵
trajectory = [];

% 生成轨迹
step_size = 9; % 定义步长单位
for i = 1:4
    % 计算两个连续点之间的差值
    x_diff = square_points(i+1, 1) - square_points(i, 1);
    y_diff = square_points(i+1, 2) - square_points(i, 2);
    
    % 计算步数（向上取整保证能覆盖全程）
    steps = ceil(max(abs(x_diff), abs(y_diff)) / step_size);
    
    % 计算每一步的增量
    x_step = x_diff / steps;
    y_step = y_diff / steps;
    
    % 确定起始步（第一条边从0开始，其他边从1开始）
    start_j = (i == 1); % 当i=1时返回0，否则返回1
    
    % 生成每一小步的坐标点
    for j = start_j:steps
        new_point = square_points(i, :) + [x_step * j, y_step * j];
        trajectory = [trajectory; new_point];
    end
end

% 保存数据文件
save('F:\capstone2025\small_myRIO_Helmholtz BP_rbf controller\trajectory_data.mat', 'trajectory');
dlmwrite('F:\capstone2025\small_myRIO_Helmholtz BP_rbf controller\trajectory_data.txt',...
          trajectory, 'delimiter', ' ', 'precision', '%.5f');

% 绘制轨迹
figure;
plot(trajectory(:,1), trajectory(:,2), '-o');
xlabel('X'); ylabel('Y');
title('Square Trajectory Tracking');
axis equal; grid on;