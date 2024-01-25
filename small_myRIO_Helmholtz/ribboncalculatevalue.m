% Sample matrix A (replace this with your n*6 matrix)


% Define the values in the first column that we're interested in
% values_of_interest = [3.5:0.1:7.5];

% Initialize an empty array to store the averages
averages = [];

% Loop through each value of interest
for value = values_of_interest
    % Find the rows where the first column is equal to the current value of interest
    rows = find(A(:, 1) == value);
    
    % If any such rows exist, calculate the average of the corresponding elements in the 4th column
    if ~isempty(rows)
        avg_value = mean(A(rows, 4));
        fprintf('Average for value %.1f in the 1st column is %.2f\n', value, avg_value);
        
        % Store the average in the averages array
        averages = [averages; value, avg_value];
    end
end

% Display the final array of averages
disp('Array of averages:');
disp(averages);
