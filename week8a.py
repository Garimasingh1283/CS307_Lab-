import numpy as np

class Gridworld:
    def __init__(self, rows, cols, terminals, rewards, transition_prob=0.8, gamma=0.9):
        self.rows = rows
        self.cols = cols
        self.terminals = terminals  # Dict of terminal states {state: reward}
        self.rewards = rewards  # Default reward for non-terminal states
        self.transition_prob = transition_prob
        self.gamma = gamma
        self.states = [(i, j) for i in range(rows) for j in range(cols)]
        self.actions = ['up', 'down', 'left', 'right']
        self.value_function = {s: 0 for s in self.states}
    
    def is_terminal(self, state):
        return state in self.terminals

    def get_next_states(self, state, action):
        row, col = state
        intended = {
            'up': (row - 1, col),
            'down': (row + 1, col),
            'left': (row, col - 1),
            'right': (row, col + 1),
        }[action]
        
        def valid(s):
            return 0 <= s[0] < self.rows and 0 <= s[1] < self.cols
        
        next_states = {intended if valid(intended) else state: self.transition_prob}
        for ortho_action in {'up', 'down', 'left', 'right'} - {action}:
            ortho = {
                'up': (row - 1, col),
                'down': (row + 1, col),
                'left': (row, col - 1),
                'right': (row, col + 1),
            }[ortho_action]
            next_states[ortho if valid(ortho) else state] = 0.1
        
        return next_states

    def value_iteration(self, epsilon=1e-4):
        while True:
            delta = 0
            new_values = self.value_function.copy()
            for state in self.states:
                if self.is_terminal(state):
                    continue
                
                values = []
                for action in self.actions:
                    value = 0
                    for next_state, prob in self.get_next_states(state, action).items():
                        reward = self.terminals.get(next_state, self.rewards)
                        value += prob * (reward + self.gamma * self.value_function[next_state])
                    values.append(value)
                new_values[state] = max(values)
                delta = max(delta, abs(new_values[state] - self.value_function[state]))
            
            self.value_function = new_values
            if delta < epsilon:
                break
        return self.value_function

# Initialize the gridworld
gridworld = Gridworld(
    rows=4,
    cols=3,
    terminals={(0, 3): 1, (1, 3): -1},
    rewards=-0.04,
    transition_prob=0.8
)

# Perform value iteration
optimal_values = gridworld.value_iteration()
for state, value in sorted(optimal_values.items()):
    print(f"State {state}: Value = {value:.3f}")
