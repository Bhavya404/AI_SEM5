import heapq
import sys

# Define the goal state
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class PuzzleState:
    """
    Represents a state of the 8-puzzle.
    """
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.g_cost = 0 if parent is None else parent.g_cost + 1
        self.h_cost = self.calculate_manhattan_distance()
        self.f_cost = self.g_cost + self.h_cost

    def __lt__(self, other):
        """
        Compare states based on their f_cost for the priority queue.
        """
        return self.f_cost < other.f_cost

    def calculate_manhattan_distance(self):
        """
        Calculates the Manhattan distance heuristic for the current board state.
        """
        distance = 0
        for i in range(9):
            if self.board[i] != 0:
                current_row, current_col = divmod(i, 3)
                goal_index = self.board[i] - 1
                goal_row, goal_col = divmod(goal_index, 3)
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def is_goal(self):
        """
        Checks if the current state is the goal state.
        """
        return self.board == GOAL_STATE

    def get_neighbors(self):
        """
        Generates all possible next states (neighbors) from the current state.
        """
        neighbors = []
        zero_index = self.board.index(0)
        
        # Possible moves for the blank space
        moves = []
        if zero_index % 3 > 0:  # Move left
            moves.append(-1)
        if zero_index % 3 < 2:  # Move right
            moves.append(1)
        if zero_index // 3 > 0:  # Move up
            moves.append(-3)
        if zero_index // 3 < 2:  # Move down
            moves.append(3)

        for move in moves:
            new_board_list = list(self.board)
            new_index = zero_index + move
            new_board_list[zero_index], new_board_list[new_index] = new_board_list[new_index], new_board_list[zero_index]
            neighbors.append(PuzzleState(tuple(new_board_list), self, move))
        return neighbors

def is_solvable(board):
    """
    Checks if the 8-puzzle board is solvable.
    A board is solvable if the number of inversions is even.
    An inversion is when a tile is followed by a smaller tile.
    """
    inversions = 0
    for i in range(len(board)):
        if board[i] == 0:
            continue
        for j in range(i + 1, len(board)):
            if board[j] != 0 and board[i] > board[j]:
                inversions += 1
    return inversions % 2 == 0

def get_user_input_board():
    """
    Prompts the user to enter the initial state of the puzzle.
    Performs validation to ensure the input is valid.
    """
    while True:
        try:
            print("Enter the 8-puzzle board configuration as 9 numbers separated by spaces.")
            print("Use '0' to represent the blank space. Example: 1 2 3 4 5 6 7 8 0")
            user_input = input("> ")
            numbers = [int(n) for n in user_input.split()]
            
            if len(numbers) != 9:
                print("Invalid input. Please enter exactly 9 numbers.")
                continue

            if sorted(numbers) != [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                print("Invalid input. The numbers must be 0-8 with no duplicates.")
                continue

            initial_board = tuple(numbers)
            if not is_solvable(initial_board):
                print("This puzzle configuration is not solvable. Please try a different one.")
                continue

            return initial_board

        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

def solve_puzzle(initial_board):
    """
    Solves the 8-puzzle using the A* search algorithm.
    """
    start_state = PuzzleState(initial_board)
    
    # Priority queue for open nodes
    open_list = [start_state]
    heapq.heapify(open_list)
    
    # Set to store visited boards to avoid cycles
    closed_list = {initial_board}

    while open_list:
        current_state = heapq.heappop(open_list)
        
        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state.board)
                current_state = current_state.parent
            return path[::-1]

        for neighbor in current_state.get_neighbors():
            if neighbor.board not in closed_list:
                closed_list.add(neighbor.board)
                heapq.heappush(open_list, neighbor)
    
    return None # No solution found

def print_solution(path):
    """
    Prints the step-by-step solution path.
    """
    for step, board in enumerate(path):
        print(f"--- Step {step} ---")
        for i in range(0, 9, 3):
            print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |".replace("0", " "))
    print("\nPuzzle solved!")

if __name__ == "__main__":
    initial_board = get_user_input_board()
    print("\nSolving the puzzle...")
    
    solution_path = solve_puzzle(initial_board)
    
    if solution_path:
        print_solution(solution_path)
    else:
        print("A solution path could not be found.")

