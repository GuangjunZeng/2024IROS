
    % Initial values
    min_avg = Inf;
    selected_num = NaN;

    % Iterate over the numbers from the first to the (414 - 192 + 1)th
    for i = 1:(length(ratio1) - 134 + 1)
        % Calculate the average for the next 192 numbers including the current
        avg = sum(ratio1(i:i+133)) / 134;
        % Update the minimum average and the selected number if a new minimum is found
        if avg < min_avg
            min_avg = avg;
            selected_num = ratio1(i);
        end
    end



    
    