# Initial and goal states
initial_state = "WWW_EEE"
goal_state = "EEE_WWW"

# Function to check if a move is valid
def is_valid_move(from_idx, to_idx, state):
    # Ensure that the move is within bounds and valid by the problem's rules
    if to_idx < 0 or to_idx >= len(state):
        return False
    if state[to_idx] == 'E' and state[from_idx] == 'W':
        return False
    # Valid moves are 1 or 2 positions away
    return abs(to_idx - from_idx) == 1 or abs(to_idx - from_idx) == 2

# Function to generate all possible next states
def get_next_states(state):
    next_states = []
    empty_index = state.find('_')
    # Explore all positions for valid moves
    for i in range(len(state)):
        if state[i] != '_':
            if is_valid_move(i, empty_index, state):
                # Swap the positions to create a new state
                new_state = list(state)
                new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
                next_states.append("".join(new_state))
    return next_states

# DFS to find the path to the goal state using a stack
def dfs(start, goal):
    stack = [(start, [start])]  # Stack stores tuples of (current_state, path to reach this state)
    visited = set([start])  # Track visited states

    while stack:
        current_state, path = stack.pop()

        # If the goal state is reached, return the solution path
        if current_state == goal:
            print(f"The Number of steps to find the optimal solution is {len(path) - 1}\n")
            return path

        # Generate and push next possible states onto the stack
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [next_state]))  # Push the new state and its path onto the stack

    return []  # Return an empty list if no solution is found

# Main execution
if __name__ == "__main__":
    solution = dfs(initial_state, goal_state)

    if solution:
        print("Solution found:")
        for state in solution:
            print(state)
    else:
        print("No solution found.")
