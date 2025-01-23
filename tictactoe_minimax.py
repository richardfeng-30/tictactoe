#don't need to code in a function to run

#variables don't need to be declared with types

#global variables - same as class variables
#can be used by any function in the file
board = []
piece = "o"
moveRow = -1
moveCol = -1
recursive_calls = 0

def main():
    setupBoard()
    printBoard()

    while not winner() and not tie():
        changePiece()
        makeMove()
        printBoard()

    if winner():
        print(piece + " won!")
    else:
        print("tie game!")

def setupBoard():
    #i iterates 0-1-2
    for i in range (3):
        row = []
        for j in range(3):
            row.append("_")
        board.append(row)

def printBoard():
    #for-each loop
    for row in board:
        # print(row)
        line = ""
        for spot in row:
            line += spot + "  "
        print(line)
    print()

def winner():

    rowCount = 0
    colCount = 0
    d1Count = 0
    d2Count = 0

    for i in range(len(board)):
        if board[moveRow][i] == piece:
            rowCount += 1
        if board[i][moveCol] == piece:
            colCount += 1
        if board[i][i] == piece:
            d1Count += 1
        if board[i][len(board)-1-i] == piece:
            d2Count += 1

    if rowCount == 3 or colCount == 3 or d1Count == 3 or d2Count == 3:
        return True

    return False

def tie():
    #if there are any blank spots, there can't be a tie game
    for row in board:
        for spot in row:
            if spot == "_":
                return False
    return True

def changePiece():
    #if a function needs to check or change a global (class) var, use this:
    global piece

    if piece == "o":
        piece = "x"
    else:
        piece = "o"

def makeMove():
    global moveRow
    global moveCol

    #only need the global line if the function is changing or checking the value of the var??
    print(piece + "'s turn")

    #human player is x
    if piece == "x":

        moveRow = int(input("Enter row: "))
        moveCol = int(input("Enter col: "))

        #len(list) is list length
        while(moveRow < 0 or moveRow > 2 or moveCol < 0 or moveCol >= len(board)
               or board[moveRow][moveCol] != "_"):
            print("invalid coordinate")
            moveRow = int(input("Enter row: "))
            moveCol = int(input("Enter col: "))

    else:
        moveRow, moveCol = ai_turn()

    board[moveRow][moveCol] = piece

def ai_turn():
    global recursive_calls
    recursive_calls = 0
    row = -1
    col = -1

    #your logic goes here
    global moveRow
    global moveCol
    global piece

    # loop through board and check the score of any blank space
    # pick move with highest score
    hiScore = -10
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                piece = "o"
                moveRow = i
                moveCol = j
                board[i][j] = piece
                score = evaluate("ai")
                print(f"row {i} col {j} score {score}")
                # undo the move after simulating its placement and getting its score
                board[i][j] = "_"
                if score > hiScore:
                    hiScore = score
                    row = i
                    col = j
    

    # evaluate() may alternate turns and pieces multiple times
    # set piece back to o to make sure it's correct when ai move is finalized
    piece = "o"
    print(recursive_calls)
    return row, col

def evaluate(currentPlayer):
    global recursive_calls
    global moveRow
    global moveCol
    global piece

    recursive_calls += 1

    # game over situations where currentPlayer's move ends the game
    if currentPlayer == "ai" and winner():
        return 1
    elif currentPlayer == "other" and winner():
        return -1
    elif tie():
        return 0
    
    # ai just went but did not reach game over situation so other player needs to go
    # simulate other player making best move to minimize AI score
    elif currentPlayer == "ai":
        bestScore = 10
        for i in range(3):
            for j in range(3):
                if board[i][j]:
                    if board[i][j] == "_":
                        piece = "x"
                        moveRow = i
                        moveCol = j
                        board[i][j] = piece
                        score = evaluate("other")
                        # undo the move and update bestscore
                        board[i][j] = "_"
                        if score < bestScore:
                            bestScore = score
        return bestScore
    
    # other player just went and now need to simulate an ai next turn
    elif currentPlayer == "other":
        bestScore = -10
        for i in range(3):
            for j in range(3):
                if board[i][j]:
                    if board[i][j] == "_":
                        piece = "o"
                        moveRow = i
                        moveCol = j
                        board[i][j] = piece
                        score = evaluate("ai")
                        # undo the move and update bestscore
                        board[i][j] = "_"
                        if score > bestScore:
                            bestScore = score
        return bestScore
    
main()