# Name: Akshay Yeluri

# ---------------------------------------------------------------------- 
# Miniproject: 2048 game.
# ---------------------------------------------------------------------- 

import random, sys

def make_board():
    '''
    Create a game board in its initial state.
    The board is a dictionary mapping (row, column) coordinates 
    (zero-indexed) to integers which are all powers of two (2, 4, ...).
    Exactly two locations are filled.
    Each contains either 2 or 4, with an 80% probability of it being 2.

    Arguments: none
    Return value: the board
    '''
    
    possibleLocs = []
    board = {}
    for row in range(4):
        for col in range(4):
            possibleLocs.append((row,col))
    random.shuffle(possibleLocs)
    for i in range(2):
        initLoc = possibleLocs[i]
        if random.random() < 0.8:
            board[initLoc] = 2
        else:
            board[initLoc] = 4
    return board

#
# Problem 3.2
#

def get_row(board, row_n):
    '''
    Return a row of the board as a list of integers.
    Arguments:
      board -- the game board
      row_n -- the row number

    Return value: the row
    '''

    assert 0 <= row_n < 4
    row = []
    for col_n in range(4):
        locValue = board.get((row_n, col_n), 0)
        row.append(locValue)
    return row

def get_column(board, col_n):
    '''
    Return a column of the board as a list of integers.
    Arguments:
      board -- the game board
      col_n -- the column number

    Return value: the column
    '''

    assert 0 <= col_n < 4
    col = []
    for row_n in range(4):
        locValue = board.get((row_n, col_n), 0)
        col.append(locValue)
    return col

def put_row(board, row, row_n):
    '''
    Given a row as a list of integers, put the row values into the board.

    Arguments:
      board -- the game board
      row   -- the row (a list of integers)
      row_n -- the row number

    Return value: none; the board is updated in-place.
    '''

    assert 0 <= row_n < 4
    assert len(row) == 4
    for col_n in range(4):
        newVal = row[col_n]
        if (row_n,col_n) in board:
            del board[(row_n,col_n)]
        if newVal:
            board[(row_n,col_n)] = newVal

def put_column(board, col, col_n):
    '''
    Given a column as a list of integers, put the column values into the board.

    Arguments:
      board -- the game board
      col   -- the column (a list of integers)
      col_n -- the column number

    Return value: none; the board is updated in-place.
    '''

    assert 0 <= col_n < 4
    assert len(col) == 4
    for row_n in range(4):
        newVal = col[row_n]
        if (row_n,col_n) in board:
            del board[(row_n,col_n)]
        if newVal:
            board[(row_n,col_n)] = newVal

#
# Problem 3.3
#

def make_move_on_list(numbers):
    '''
    Make a move given a list of 4 numbers using the rules of the
    2048 game.

    Argument:
      numbers -- a list of 4 numbers

    Return value:
      The list after moving the numbers to the left.  The original list
      is not altered.
    '''

    assert len(numbers) == 4
    numbersC = numbers[:] # Copy numbers cuz not supposed to change list :(
    numbersC.sort(key=bool, reverse=True) # Saved me like a 4-line for loop :)
    newLst = []
    i = 0 #represents which number in the original list we're looking at moving
    while i < 4:
        newLst.append(numbersC[i])
        if not numbersC[i] or i == 3:
            break;
        if numbersC[i] == numbersC[i+1]:
            newLst[-1] += numbersC[i]
            i += 1
        # if 2 adjacent numbers are the same, don't have to look at second
        # number, can skip it
        i += 1
    newLst += [0]*(4-len(newLst)) # make the list the right size
    return newLst

#
# Problem 3.4
#

def make_move(board, cmd):
    '''
    Make a move on a board given a movement command.
    Movement commands include:

      'w' -- move numbers upward
      's' -- move numbers downward
      'a' -- move numbers to the left
      'd' -- move numbers to the right

    Arguments:
      board  -- the game board
      cmd    -- the command letter

    Return value: none; the board is updated in-place.
    '''

    assert cmd in ['w', 'a', 's', 'd']
    if cmd in ['w', 's']:
        for col_n in range(4):
            col = get_column(board, col_n)
            if cmd == 's':
                col.reverse()
                col = make_move_on_list(col)
                col.reverse()
            else:
                col = make_move_on_list(col)
            put_column(board, col, col_n)
    else:
        for row_n in range(4):
            row = get_row(board, row_n)
            if cmd == 'd':
                row.reverse()
                row = make_move_on_list(row)
                row.reverse()
            else:
                row = make_move_on_list(row)
            put_row(board, row, row_n)

#
# Problem 3.5
#

def game_over(board):
    '''
    Check to see if the game is over (either 2048 is reached or no moves are
    left.
        
    Arguments:
    board  -- the game board
    Return value: False if game continues, True if game is over.
    '''
    
    if 2048 in board.values():
        return True
    for move in ['w', 'a', 's', 'd']:
        testBoard = board.copy()
        make_move(testBoard, move)
        if not testBoard == board:
            return False
    return True


#
# Problem 3.6
#

def update(board, cmd):
    '''
    Make a move on a board given a movement command.  If the board
    has changed, then add a new number (2 or 4, 90% probability it's 
    a 2) on a randomly-chosen empty square on the board.

    Arguments:
      board  -- the game board
      cmd    -- the command letter

    Return value: none; the board is updated in-place.
    '''

    oldBoard = board.copy()
    make_move(board, cmd)
    if board != oldBoard:
        possibleLocs = []
        for row in range(4):
            for col in range(4):
                possibleLocs.append((row,col))
        for loc in board:
            possibleLocs.remove(loc)
        locToAddTo = random.choice(possibleLocs)
        if random.random() < 0.9:
            board[locToAddTo] = 2
        else:
            board[locToAddTo] = 4

### Supplied to students:

def display(board):
    '''
    Display the board on the terminal in a human-readable form.

    Arguments:
      board  -- the game board

    Return value: none
    '''

    s1 = '+------+------+------+------+'
    s2 = '| {:^4s} | {:^4s} | {:^4s} | {:^4s} |'

    print(s1)
    for row in range(4):
        c0 = str(board.get((row, 0), ''))
        c1 = str(board.get((row, 1), ''))
        c2 = str(board.get((row, 2), ''))
        c3 = str(board.get((row, 3), ''))
        print(s2.format(c0, c1, c2, c3))
        print(s1)

def play_game():
    '''
    Play a game interactively.  Stop when the board is completely full
    and no moves can be made.

    Arguments: none
    Return value: none
    '''

    b = make_board()
    display(b)
    while True:
        if game_over(b):
            print('Game over!')
            break
        move = input('Enter move: ')
        if move not in ['w', 'a', 's', 'd', 'q']:
            print("Invalid move!  Only 'w', 'a', 's', 'd' or 'q' allowed.")
            print('Try again.')
            continue
        if move == 'q':  # quit
            return
        update(b, move)
        display(b)

#
# Useful for testing:
#

def list_to_board(lst):
    '''
    Convert a length-16 list into a board.
    '''
    board = {}
    k = 0
    for i in range(4):
        for j in range(4):
            if lst[k] != 0:
                board[(i, j)] = lst[k]
            k += 1
    return board


def random_game():
    '''Play a random game.'''
    board = make_board()
    display(board)
    while True:
        print()
        move = random.choice('wasd')
        update(board, move)
        display(board)
        if game_over(board):
            break
