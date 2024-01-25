% 定义参数
step_size = 10;         % 基础移动步长（水平和垂直通用）
x_range = [-230, 80];  % 水平移动范围 [x_start, x_end]
y_start = -300;          % 起始y坐标
y_end = 300;            % 结束y坐标
vertical_stride = 100;   % 每段蛇形线的垂直总间距

% 初始化轨迹和当前坐标
trajectory = [];
current_x = x_range(1);
current_y = y_start;

% 生成蛇形轨迹
while current_y < y_end  % 关键修改：严格小于终止条件
    % 水平向右移动（严格限制到x_end）
    x_steps = current_x : step_size : x_range(2);
    trajectory = [trajectory; x_steps', repmat(current_y, length(x_steps), 1)];
    current_x = x_range(2);  % 更新到右边界
    
    % 垂直向下移动（带强制约束）
    remaining_vertical = min(vertical_stride, y_end - current_y);  % 关键修改：避免越界
    if remaining_vertical <= 0  % 提前终止条件
        break;
    end
    while remaining_vertical > 0
        step = min(step_size, remaining_vertical);
        current_y = current_y + step;
        trajectory = [trajectory; current_x, current_y];
        remaining_vertical = remaining_vertical - step;
    end
    if current_y >= y_end  % 再次检查是否越界
        break;
    end
    
    % 水平向左移动（严格限制到x_start）
    x_steps = current_x : -step_size : x_range(1);
    trajectory = [trajectory; x_steps', repmat(current_y, length(x_steps), 1)];
    current_x = x_range(1);  % 更新到左边界
    
    % 再次垂直向下移动（同上）
    remaining_vertical = min(vertical_stride, y_end - current_y);
    if remaining_vertical <= 0
        break;
    end
    while remaining_vertical > 0
        step = min(step_size, remaining_vertical);
        current_y = current_y + step;
        trajectory = [trajectory; current_x, current_y];
        remaining_vertical = remaining_vertical - step;
    end
end


% 保存数据文件（路径需要根据实际修改）
save('F:\capstone2025\small_myRIO_Helmholtz BP_rbf controller\snake_trajectory.mat', 'trajectory');
dlmwrite('F:\capstone2025\small_myRIO_Helmholtz BP_rbf controller\snake_trajectory.txt', trajectory, 'delimiter', ' ', 'precision', '%.2f');

% 可视化轨迹
figure;
plot(trajectory(:,1), trajectory(:,2), 'b-o');
xlabel('X Coordinate'); ylabel('Y Coordinate');
title('Continuous Snake Trajectory with Vertical Steps');
axis equal; grid on;