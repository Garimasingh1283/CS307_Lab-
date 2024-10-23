function ten_armed_bandit()
    num_arms = 10;  
    num_iterations = 1000;  

    Q = zeros(1, num_arms);  
    N = zeros(1, num_arms);  
    
    mean_rewards = zeros(1, num_arms);  
    rewards = zeros(1, num_iterations);  

    for t = 1:num_iterations
        mean_rewards = mean_rewards + randn(1, num_arms) * 0.01;  
        
        [~, action] = max(Q);  
        
        reward = bandit_nonstat(action, mean_rewards);  
        
        N(action) = N(action) + 1;  
        
        Q(action) = Q(action) + (1 / N(action)) * (reward - Q(action));  
        
        rewards(t) = reward;  
    end
    
    plot(cumsum(rewards) ./ (1:num_iterations));
    xlabel('Time Steps');
    ylabel('Average Reward');
    title('Greedy Approach on 10-Armed Bandit');
end

function [reward] = bandit_nonstat(action, mean_rewards)
    reward = mean_rewards(action) + randn;  
end
