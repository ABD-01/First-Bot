# Highest power of two less than or equal to a numebr
def Powerof2(n):
    power = 1
    for i in range(n, 0, -1):
        if not i & (i - 1):
            power = i
            break
    return power


# Inserting 2 in random in board
from random import randrange


def insert_two(board):
    i = randrange(len(board))
    j = randrange(len(board))
    while board[i][j] != 0:
        i = randrange(len(board))
        j = randrange(len(board))
    board[i][j] = 2
    return board


# Function to Transpose a 2D List
def transpose(board):
    return [list(row) for row in zip(*board)]


# Function to Flip the 2D List
def invert(board):
    return [row[::-1] for row in board]


# Validating the Move
def isValid(move, gboard):
    # Orienting as the convinience
    if move in ['w', 's']:
        board = transpose(gboard)
    else:
        board = gboard

    # Checking for any consecutive equal values
    for row in board:
        if any(row[i] == row[i + 1] and row[i] != 0 for i in range(len(row) - 1)):
            ##print("Found consecutive equal value")
            return True

    if move in ['a', 'w']:
        board = invert(board)

    for row in board:
        nrow = sorted(row, key=bool)
        # Else checking is the previous state and state after the move is same or different
        if row != nrow:
            ##print("Check here", row)
            return True

    # If none of the above case happens then move in Invalid
    ##print("Cannot move in given Direction", move)
    return False


# Pretty Printing the Game Board
def printboard(gboard):
    board = []
    for row in gboard:
        board.append([i if i != 0 else "  " for i in row])
    boardstr = '-' + '-------' * len(board) + '\n'
    for row in board:
        # s = ' | '.join(['`%4s`' %str(cell) for cell in row])
        s = ' | '.join(['%4s' % str(cell) for cell in row])
        boardstr = boardstr + f"| {s} |\n"
        boardstr = boardstr + '-' + '-------' * len(board) + '\n'
    print(boardstr)
    return '`' + boardstr + '`'


# Checking if users lost or not
def didLose(board):
    # Check for any zero present
    if any(0 in row for row in board) == True:
        ##print("There is still zero present,You didn't lose")
        return False

    # Checking for any eual consecutive Values in rows
    for row in board:
        if any(row[i] == row[i + 1] for i in range(len(row) - 1)):
            ##print("consecutive equal values exists, Didn'i lose")
            return False

    # Checking for any equal consecutive Values in columns
    board = transpose(board)
    for row in board:
        if any(row[i] == row[i + 1] for i in range(len(row) - 1)):
            ##print("consecutive equal values exists, Didn'i lose")
            return False

    ##print("No move is Possible")
    return True
