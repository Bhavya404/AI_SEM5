from collections import deque
import copy

# Puzzle size
N = 3

# Directions: (delta_row, delta_col)
DIRECTIONS = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

# Convert 2D list state to tuple of tuples for hashing in sets
def list_to_tuple(state):
    return tuple(tuple(row) for row in state)

# Find the blank tile (0) position in the 2D list state
def find_blank(state):
    for i in range(N):
        for j in range(N):
            if state[i][j] == 0:
                return i, j
    return None

# Generate all valid successor states (as 2D lists) from the current state
def get_successors(state):
    blank_row, blank_col = find_blank(state)
    successors = []

    for action, (dr, dc) in DIRECTIONS.items():
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < N and 0 <= new_col < N:
            new_state = copy.deepcopy(state)
            # Swap blank tile with adjacent tile
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
            successors.append((new_state, action))
    return successors

# Recursive Depth-Limited Search (DLS)
def dls(current_state, goal_state, depth, path, visited):
    if current_state == goal_state:

        return path

    if depth == 0:
        return None

    visited.add(list_to_tuple(current_state))

    for neighbor, action in get_successors(current_state):
        neighbor_tuple = list_to_tuple(neighbor)
        if neighbor_tuple not in visited:
            result = dls(neighbor, goal_state, depth - 1, path + [action], visited)
            if result is not None:
                return result

    return None

# Iterative Deepening DFS (IDDFS)
def iddfs(start, goal, max_depth=50):
    for depth in range(max_depth):
        visited = set()
        result = dls(start, goal, depth, [], visited)
        if result is not None:
            return result
    return None

# Take 2D array input from user
def get_input_state(prompt):
    print(prompt)
    state = []
    for i in range(N):
        while True:
            try:
                row = input(f"Enter row {i+1} (3 numbers space-separated, use 0 for blank): ").strip().split()
                if len(row) != N:
                    raise ValueError("Incorrect number of elements.")
                row = [int(num) for num in row]
                state.append(row)
                break
            except ValueError as e:
                print("Invalid input, please enter exactly 3 integers separated by spaces.")
    return state

def main():
    print("8 Puzzle Solver using IDDFS")
    start = get_input_state("Enter START state:")
    goal = get_input_state("Enter GOAL state:")

    print("\nSolving...\n")
    solution = iddfs(start, goal)

    if solution is not None:
        print("Solution found!")
        print("Moves:", ' -> '.join(solution))
        print(f"Number of steps: {len(solution)}")
    else:
        print("No solution found within depth limit.")

if __name__ == "__main__":
    main()
