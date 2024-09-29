# Define the goal state for the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# actions
# This function returns a list of possible moves from the current state
def get_possible_moves(state):
    blank_position = find_blank_position(state)
    row, col = blank_position
    moves = []
    if row > 0:  # if moving up is possible
        moves.append("up")
    if row < 2:  # if moving down is possible
        moves.append("down")
    if col > 0:  # if moving left is possible
        moves.append("left")
    if col < 2:  # if moving right is possible
        moves.append("right")
    return moves


# successor function
# This function executes a move on the current state
def perform_move(state, move):
    blank_position = find_blank_position(state)
    new_state = [row.copy() for row in state]  
    row, col = blank_position

    if move == "up":  # Move  blank space up
        new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
    elif move == "down":  # down
        new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
    elif move == "left":  #left
        new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
    else:  # right
        new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]

    return new_state


def find_blank_position(state):
    """ This function finds the position of the blank space (0) in the puzzle state. """
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return i, j



def is_goal_state(state):
    """ Check if the current state is the goal state. """
    return state == GOAL_STATE  