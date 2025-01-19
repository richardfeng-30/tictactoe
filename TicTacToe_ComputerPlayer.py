import random

# global
board = []
piece = "x"
turn = 1
move_row = -1
move_col = -1
comp_move_row = -1
comp_move_col = -1
last_row = -1
last_col = -1

def main():
    setup()
    print_board()
    make_move()
    

    while not winner() and not tie():
        change_piece()
        print_board()
        make_move()

def setup():
    for i in range(3):
        row = []
        for j in range(3):
            row.append("_")
        board.append(row)

def print_board():
    for row in board:
        line = ""
        for spot in row:
            line += spot + " "
        print(line)
    print()

def winner():
    row_count = 0
    col_count = 0
    d1_count = 0
    d2_count = 0

    for i in range(len(board)):
        if board[last_row][i] == piece:
            row_count += 1
        if board[i][last_col] == piece:
            col_count += 1
        if board[i][i] == piece:
            d1_count += 1
        if board[i][len(board) - 1 - i]  == piece:
            d2_count += 1
    
    if (row_count == 3 or col_count == 3 or d1_count == 3 or d2_count == 3):
        print_board()
        print(piece + " wins")
        return True
    return False

def tie():
    for row in board:
        for spot in row:
            if spot == "_":
                return False
    print_board()
    print("tie")
    return True

def change_piece():
    global piece
    if piece == "o":
        piece = "x"
    else:
        piece = "o"

def make_move():
    global move_row
    global move_col
    global comp_move_row
    global comp_move_col
    global last_row
    global last_col
    global turn
    print(piece + "'s turn")

    # human player is o
    if piece == "o":
        move_row = int(input("Enter row: "))
        move_col = int(input("Enter col: "))

        while (move_row < 0 or move_row > 2 or move_col < 0 or move_col >= len(board) or board[move_row][move_col] != "_"):
            print("error")
            move_row = int(input("Enter row: "))
            move_col = int(input("Enter col: "))

        board[move_row][move_col] = piece
        last_row = move_row
        last_col = move_col

    else:
        comp_move_row, comp_move_col = ai_turn()
        print(comp_move_row, comp_move_col)
        board[comp_move_row][comp_move_col] = piece
        last_row = comp_move_row
        last_col = comp_move_col

    turn += 1

    # board[move_row][move_col] = piece

def ai_turn():
    # 1. check if can win
    candidate_row, candidate_col = win_or_block("x", "o", comp_move_row, comp_move_col)
    if (candidate_row != -1):
        return candidate_row, candidate_col

    # 2. check if need to block
    candidate_row, candidate_col = win_or_block("o", "x", move_row, move_col)
    if (candidate_row != -1):
        return candidate_row, candidate_col
    
    # 3. check for forking move
    candidate_row, candidate_col = check_fork()
    if (candidate_row != -1):
        return candidate_row, candidate_col
    
    # 4. prevent opponent fork

    # 5. random move
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    while board[x][y] != "_":
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    return x, y



def win_or_block(target_piece, other_piece, last_row, last_col):
    row = -1
    col = -1
    candidate_row = - 1
    candidate_col = -1

    count = 0
    for i in range(3):
        if board[last_row][i] == target_piece:
            count += 1
        elif board[last_row][i] == other_piece:
            count -= 1
        else: # this is empty
            candidate_row = last_row
            candidate_col = i
    if count == 2:
        return candidate_row, candidate_col
    
    count = 0
    for i in range(3):
        if board[i][last_col] == target_piece:
            count += 1
        elif board[i][last_col] == other_piece:
            count -= 1
        else:
            candidate_row = i
            candidate_col = last_col
    if count == 2:
        return candidate_row, candidate_col
    
    # only check if diagonal needs to be blocked if previous move is on diagonal
    if (last_row + last_col) % 2 == 0:
        count = 0
        for i in range(3):
            if board[i][i] == target_piece:
                count += 1
            elif board[i][i] == other_piece:
                count -= 1
            else:
                candidate_row, candidate_col = i, i
        if count == 2:
            return candidate_row, candidate_col
        
        count = 0
        for i in range(3):
            if board[i][2 - i] == target_piece:
                count += 1
            elif board[i][2 - i] == other_piece:
                count -= 1
            else:
                candidate_row, candidate_col = i, 2 - i
        if count == 2:
            return candidate_row, candidate_col
    
    return row, col

def check_fork():
    for i in range(3):
        for j in range(3):
            win_count = 0

            count = 0
            for k in range(3):
                if board[i][k] == "x":
                    count += 1
                elif board[i][k] == "o":
                    break
            if count == 1:
                win_count += 1
            
            count = 0
            for k in range(3):
                if board[k][j] == "x":
                    count += 1
                elif board[k][j] == "o":
                    break
            if count == 1:
                win_count += 1
            
            # check diagonal win case only if last move is on diagonal
            if (last_row + last_col) % 2 == 0:
                count = 0
                for k in range(3):
                    if board[k][k] == "x":
                        count += 1
                    elif board[k][k] == "o":
                        break
                if count == 1:
                    win_count += 1
                
                count = 0
                for k in range(3):
                    if board[k][2 - k] == "x":
                        count += 1
                    elif board[k][2 - k] == "o":
                        break
                if count == 1:
                    win_count += 1
                    
            
            if win_count == 2:
                return i, j
    return -1, -1


main()