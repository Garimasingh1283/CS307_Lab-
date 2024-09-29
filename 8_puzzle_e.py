
import random
def get_possible_moves(state):
    blank_position = find_blank_position(state)
    row, col = blank_position
    moves = []
    if row > 0:
        moves.append("up")
    if row < 2:
        moves.append("down")
    if col > 0:
        moves.append("left")
    if col < 2:
        moves.append("right")
    return moves

def perform_move(state, move):
    blank_position = find_blank_position(state)
    new_state = [row.copy() for row in state]  # Create a new 2D list
    row, col = blank_position

    if move == "up":
        new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
    elif move == "down":
        new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
    elif move == "left":
        new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
    else:
        new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]

    return new_state

def find_blank_position(state):
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return i, j

def generate_states_at_depth_d(goal_state, depth):
    states_at_depth = []

    def backtrack(current_state, depth_left):
        if depth_left == 0:
            states_at_depth.append(current_state)
            return

        moves = get_possible_moves(current_state)
        random.shuffle(moves)
        for move in moves:
            new_state = perform_move(current_state, move)
            backtrack(new_state, depth_left - 1)

    backtrack(goal_state, depth)
    return states_at_depth

# Example usage:
goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
depth = 3
states = generate_states_at_depth_d(goal_state, depth)
for i, state in enumerate(states):
    print(f"State {i + 1}:\n", "\n".join(map(str, state)))
    print()