# global
board = []
piece = "o"
move_row = -1
move_col = -1

def main():
    setup()
    print_board()
    make_move()

    while not winner() and not tie():
        change_piece()
        make_move()
        print_board()

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
        if board[move_row][i] == piece:
            row_count += 1
        if board[i][move_col] == piece:
            col_count += 1
        if board[i][i] == piece:
            d1_count += 1
        if board[i][len(board) - 1 - i]  == piece:
            d2_count += 1
    
    if (row_count == 3 or col_count == 3 or d1_count == 3 or d2_count == 3):
        return True
    return False

def tie():
    for row in board:
        for spot in row:
            if spot == "_":
                return False
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
    print(piece + "'s turn")
    
    move_row = int(input("Enter row: "))
    move_col = int(input("Enter col: "))

    while (move_row < 0 or move_row > 2 or move_col < 0 or move_col >= len(board) or board[move_row][move_col] != "_"):
        print("error")
        move_row = int(input("Enter row: "))
        move_col = int(input("Enter col: "))
    
    board[move_row][move_col] = piece

main()