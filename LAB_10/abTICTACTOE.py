import math

# The Tic-Tac-Toe board
board = [' ' for x in range(10)]
player = 'X'
computer = 'O'

def print_board(board):
    """Prints the Tic-Tac-Toe board to the console."""
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])

def is_space_free(pos):
    """Checks if a position on the board is empty."""
    return board[pos] == ' '

def is_winner(bo, le):
    """Checks if a player has won the game."""
    return ((bo[1] == le and bo[2] == le and bo[3] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[7] == le and bo[8] == le and bo[9] == le) or # across the bottom
            (bo[1] == le and bo[4] == le and bo[7] == le) or # down the left side
            (bo[2] == le and bo[5] == le and bo[8] == le) or # down the middle
            (bo[3] == le and bo[6] == le and bo[9] == le) or # down the right side
            (bo[1] == le and bo[5] == le and bo[9] == le) or # diagonal
            (bo[3] == le and bo[5] == le and bo[7] == le)) # diagonal

def is_board_full(board):
    """Checks if the board is full, resulting in a draw."""
    if board.count(' ') > 1:
        return False
    else:
        return True

def insert_letter(letter, pos):
    """Inserts a player's letter into a position on the board."""
    board[pos] = letter

def player_move():
    """Handles the human player's move."""
    run = True
    while run:
        move = input("Please select a position to place 'X' (1-9): ")
        try:
            move = int(move)
            if move > 0 and move < 10:
                if is_space_free(move):
                    run = False
                    insert_letter(player, move)
                else:
                    print('Sorry, this space is occupied!')
            else:
                print('Please type a number within the range!')
        except ValueError:
            print('Please type a number!')

def computer_move():
    """Handles the AI's move using the alpha-beta algorithm."""
    best_score = -math.inf
    best_move = 0
    available_moves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]

    for move in available_moves:
        temp_board = board[:]
        temp_board[move] = computer
        score = alpha_beta(temp_board, 0, -math.inf, math.inf, False)
        temp_board[move] = ' ' # Undo the move
        if score > best_score:
            best_score = score
            best_move = move
    
    insert_letter(computer, best_move)
    return best_move

def alpha_beta(bo, depth, alpha, beta, is_maximizing):
    """
    The core alpha-beta pruning algorithm.
    is_maximizing: True for the maximizing player (AI), False for the minimizing player (human).
    """
    if is_winner(bo, computer):
        return 1
    elif is_winner(bo, player):
        return -1
    elif is_board_full(bo):
        return 0

    if is_maximizing:
        best_score = -math.inf
        available_moves = [x for x, letter in enumerate(bo) if letter == ' ' and x != 0]
        for move in available_moves:
            bo[move] = computer
            score = alpha_beta(bo, depth + 1, alpha, beta, False)
            bo[move] = ' '
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        available_moves = [x for x, letter in enumerate(bo) if letter == ' ' and x != 0]
        for move in available_moves:
            bo[move] = player
            score = alpha_beta(bo, depth + 1, alpha, beta, True)
            bo[move] = ' '
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def main():
    """Main game loop."""
    print("Welcome to Tic Tac Toe! You are 'X' and the computer is 'O'.")
    print_board(board)
    while not is_board_full(board):
        if not is_winner(board, computer):
            player_move()
            print_board(board)
        else:
            print("Sorry, the computer won this time!")
            break

        if not is_winner(board, player):
            move = computer_move()
            if move != 0:
                print('Computer placed an "O" in position', move)
                print_board(board)
        else:
            print("You won!")
            break

    if is_board_full(board) and not is_winner(board, player) and not is_winner(board, computer):
        print("Game Over! It's a tie!")

if __name__ == "__main__":
    main()
