def computer_move():
    best_move = minimax_recurse(game_board, active_player, 0)
    print("The best move is ", best_move)
    make_move(game_board, best_move, active_player)

    print("COMPUTER MOVE DONE")

def minimax_recurse(game_board, player, depth):

    winner = is_winner(game_board)
    if winner == active_player:
        return 1
    elif winner is not None and winner != active_player:
        return -1
    elif len(get_move_list(game_board)) == 0:
        return 0

    if player == player1:
        other_player = player2
    else:
        other_player = player1

    if player == active_player:
        alpha = -1
    else:
        alpha = 1

    movelist = get_move_list(game_board)
    best_move = None

    for move in movelist:
        board2 = [list(row) for row in game_board] # Create a copy of the board

        make_move(board2, move, player)

        subalpha = minimax_recurse(board2, other_player, depth + 1)

        if player == active_player:
            if depth == 0 and alpha <= subalpha:
                best_move = move
            alpha = max(alpha, subalpha)
            if alpha == 1: # Alpha-beta pruning
                if depth == 0:
                  return best_move
                return alpha

        else:
            alpha = min(alpha, subalpha)
            if alpha == -1: # Alpha-beta pruning
                return alpha

    if depth == 0:
      return best_move
    return alpha


# BOARD FUNCTIONS
game_board = [['1','2','3'],['4','5','6'],['7','8','9']] # Changed to strings to avoid confusion with available moves
def print_board(board) :

    for row in board :
        print(row)

def make_move(game_board, player_move, active_player):

    x = 0
    y = 0
    try:
        player_move = int(player_move)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return game_board

    if player_move == 1 :
        x = 0
        y = 0
    elif player_move == 2 :
        x = 0
        y = 1
    elif player_move == 3 :
        x = 0
        y = 2
    elif player_move == 4 :
        x = 1
        y = 0
    elif player_move == 5 :
        x = 1
        y = 1
    elif player_move == 6 :
        x = 1
        y = 2
    elif player_move == 7 :
        x = 2
        y = 0
    elif player_move == 8 :
        x = 2
        y = 1
    elif player_move == 9 :
        x = 2
        y = 2
    else :
        print ("value is out of range")
        return game_board


    if game_board[x][y] == "O" or game_board[x][y] == "X" :
        print("move not available")
        return game_board

    game_board[x][y] = str(active_player)
    return game_board

def is_winner(board):
    for i in range (0,3) :
        if board[i][0] == player1 and board[i][1] == player1 and board[i][2] == player1 :
            return player1

        if board[i][0] == player2 and board[i][1] == player2 and board[i][2] == player2 :
            return player2

    # checking for columns
    for i in range(0,3):
        if board[0][i] == player1 and board[1][i] == player1 and board[2][i] == player1:
            return player1
        if board[0][i] == player2 and board[1][i] == player2 and board[2][i] == player2:
            return player2

    # checking for diagonals
    if board[0][0] == player1 and board[1][1] == player1 and board[2][2] == player1 :
        return player1
    if board[0][0] == player2 and board[1][1] == player2 and board[2][2] == player2 :
        return player2

    if board[2][0] == player1 and board[1][1] == player1 and board[0][2] == player1 :
        return player1
    if board[2][0] == player2 and board[1][1] == player2 and board[0][2] == player2 :
        return player2

    return None


def get_move_list (game_board) :

    move = []

    for row in game_board :
        for i in row :
            if i.isdigit():
                move.append(int(i))
    return move



# Main Loop
player1 = "X"
player2 = "O"
print_board(game_board)
while True :
    active_player = player1
    # this is for player move
    print(get_move_list(game_board))
    player_move = input("Please insert your move >>> ")
    game_board = make_move(game_board,player_move,active_player)
    print_board(game_board)

    if is_winner(game_board) == player1 :
        print("Player1 is the winner")
        break
    if is_winner(game_board) == player2 :
        print("Player2 is the winner")
        break
    if len(get_move_list(game_board)) == 0:
        print("It's a tie!")
        break

    print(get_move_list(game_board))
    # computer time
    active_player = player2
    computer_move()
    print_board(game_board)

    if is_winner(game_board) == player1 :
        print("Player1 is the winner")
        break
    if is_winner(game_board) == player2 :
        print("Player2 is the winner")
        break
    if len(get_move_list(game_board)) == 0:
        print("It's a tie!")
        break
