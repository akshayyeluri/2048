# Name: Akshay Yeluri
# Login: ayeluri

# Please don't grade this one, I just thought it was pretty cool that it worked.
# Basically, it has the same sliding feature and scoring the original game has.
# The code is a lot messier because I didn't have time to clean it up.
# I also could not make this happen with old midterm code, because many
# functions had to be rewritten.

from tkinter import *
import random, sys

class GUIBoard:
    def __init__(self, board, canvas):
        self.canvas = canvas
        self.board = board
        for i in range(200,700,100):
            self.canvas.create_line(i,200,i,600, width=4, fill='#c0c0c0')
            self.canvas.create_line(200,i,600,i, width=4, fill='#c0c0c0')
            self.textHandle = None
        self.score = 0
        self.scoreHandle = None

    def getLoc(self, pos):
        posToPixelPos = { 0: 250,
                          1: 350,
                          2: 450,
                          3: 550 }
        yCoor, xCoor = pos
        yCoor, xCoor = posToPixelPos[yCoor], posToPixelPos[xCoor]
        return (xCoor, yCoor)

    def displayText(self, text):
        self.canvas.delete(self.textHandle)
        self.canvas.delete(self.scoreHandle)
        self.textHandle = self.canvas.create_text((400, 100), \
                                              font=('Verdana',40), text=text)
        self.scoreHandle = self.canvas.create_text((400, 700), \
                              font=('Verdana',40), text=f'Score : {self.score}')

    def keyHandler(self, event):
        movesDict = { 'Left': 'a',
                      'Right': 'd',
                      'Up': 'w',
                      'Down': 's' }
        if event.keysym not in ['Left', 'Right', 'Up', 'Down', 'q']:
            self.displayText('Invalid move! Try again...')
            return
        if event.keysym == 'q':
            quit()
        move = movesDict[event.keysym]
        update(self.board, move, self.canvas, self)
        guiBoard.displayText('Enter move: ')
        if game_over(self.board):
            self.displayText('Game over!')
            quit()

class Square:
    def __init__(self, canvas, pos, value, board, guiBoard):
        self.value = value
        colorValueDict = { 2: '#ffffff',
                           4: '#f6fcfb',
                           8: '#e0ffff',
                           16: '#d4f2ef',
                           32: '#b2ffff',
                           64: '#b1e7e2',
                           128: '#ace5ee',
                           256: '#8edcd5',
                           512: '#6bd2c8',
                           1024: '#48c7bb',
                           2048: '#34aea2', }
        self.color = colorValueDict.get(value, 2)
        self.canvas = canvas
        self.board = board
        self.pos = pos
        self.size = 96
        self.gui = guiBoard
        x1, y1 = self.gui.getLoc(self.pos)
        x2, y2 = x1, y1
        self.handle = self.canvas.create_rectangle(x1, y1, \
                                   x2, y2, fill=self.color, outline=self.color)
        self.textHandle = self.canvas.create_text((x1,y1), \
                                      font=('Verdana', 0), text=str(self.value))
        self.grow()
    
    def glide(self, pos):
        del self.board[self.pos]
        x1, y1 = self.gui.getLoc(self.pos)
        x2, y2 = self.gui.getLoc(pos)
        incrementerX, incrementerY = 20, 20
        amountToMoveX = x2 - x1
        amountToMoveY = y2 - y1
        if amountToMoveX < 0:
            incrementerX = - incrementerX
        if amountToMoveY < 0:
            incrementerY = - incrementerY
        while amountToMoveX:
            self.canvas.after(1, self.canvas.move(self.handle, incrementerX, 0))
            self.canvas.move(self.textHandle, incrementerX, 0)
            amountToMoveX -= incrementerX
            self.canvas.update()
        while amountToMoveY:
            self.canvas.after(1, self.canvas.move(self.handle, 0, incrementerY))
            self.canvas.move(self.textHandle, 0 , incrementerY)
            amountToMoveY -= incrementerY
            self.canvas.update()
        self.pos = pos
        self.board[pos] = self

    def grow(self, rev=False):
        x1o, y1o = self.gui.getLoc(self.pos)
        x2o, y2o = x1o, y1o
        sizes = list(range(0, self.size // 2 + 1, 12))
        if rev:
            sizes.reverse()
        for i in sizes:
            x1, y1 = x1o - i, y1o - i
            x2, y2 = x2o + i, y2o + i
            self.canvas.after(1, self.canvas.coords(self.handle, x1, \
                                                        y1, x2, y2))
            self.canvas.itemconfig(self.textHandle, font=('Verdana', i))
            self.canvas.update()
    
    def __del__(self):
        self.grow(rev=True)
        self.canvas.delete(self.handle)
        self.canvas.delete(self.textHandle)

def make_board(canvas):
    '''
    Create a game board in its initial state.
    The board is a dictionary mapping (row, column) coordinates 
    (zero-indexed) to Square objects whose values are powers of two (2, 4, ...).
    Exactly two locations are filled.
    Each contains a square with
    a value of 2 or 4, with an 80% probability of it being 2.

    Arguments: none
    Return value: the board
    '''
    
    possibleLocs = []
    board = {}
    guiBoard = GUIBoard(board, canvas)
    for row in range(4):
        for col in range(4):
            possibleLocs.append((row,col))
    random.shuffle(possibleLocs)
    for i in range(2):
        initLoc = possibleLocs[i]
        if random.random() < 0.8:
            board[initLoc] = Square(canvas, initLoc, 2, board, guiBoard)
        else:
            board[initLoc] = Square(canvas, initLoc, 4, board, guiBoard)
    return (board, guiBoard)

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
        whichSquare = board.get((row_n, col_n), 0)
        if whichSquare:
            locValue = whichSquare.value
            row.append(locValue)
        else:
            row.append(0)
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
        whichSquare = board.get((row_n, col_n), 0)
        if whichSquare:
            locValue = whichSquare.value
            col.append(locValue)
        else:
            col.append(0)
    return col

def put_row(board, row, row_n):
    '''
    Given a row as a list of integers, moves the square objects previously in
    that row, and combines them if necessary
        
    Arguments:
    board -- the game board
    row   -- the row (a list of integers)
    row_n -- the row number
        
    Return value: false if the row is same as before, true if row changed.
    '''
    
    assert 0 <= row_n < 4
    assert len(row) == 4
    findSquareDict = {}
    oldRow = []
    for col_n in range(4):
        whichSquare = board.get((row_n, col_n), 0)
        if whichSquare:
            oldRow.append(whichSquare.value)
            findSquareDict[len(oldRow)-1] = whichSquare
    if get_row(board, row_n) == row:
        return False
    indexes = list(range(len(oldRow)))
    newRowIndexer, incrementer = 0, 1
    if row[0] == 0:
        indexes.reverse()
        newRowIndexer, incrementer = 3, -1
    oldRowIndexer = indexes[0]
    while oldRowIndexer in indexes:
        if oldRow[oldRowIndexer] == row[newRowIndexer]:
            squareToMove = findSquareDict[oldRowIndexer]
            squareToMove.glide((row_n, newRowIndexer))
        else:
            squareToMerge1 = findSquareDict[oldRowIndexer]
            oldRowIndexer += incrementer
            squareToMerge2 = findSquareDict[oldRowIndexer]
            combine(squareToMerge1, squareToMerge2, board, \
                    (row_n, newRowIndexer))
        newRowIndexer += incrementer
        oldRowIndexer += incrementer
    return True

def put_column(board, col, col_n):
    '''
    Given a column as a list of integers, moves the square objects previously in
    that column, and combines them if necessary
        
    Arguments:
    board -- the game board
    col   -- the column (a list of integers)
    col_n -- the column number
    
    Return value: false if the row is same as before, true if row changed.
    '''
    
    assert 0 <= col_n < 4
    assert len(col) == 4
    findSquareDict = {}
    oldCol = []
    for row_n in range(4):
        whichSquare = board.get((row_n, col_n), 0)
        if whichSquare:
            oldCol.append(whichSquare.value)
            findSquareDict[len(oldCol)-1] = whichSquare
    if get_column(board, col_n) == col:
        return False
    indexes = list(range(len(oldCol)))
    newColIndexer, incrementer = 0, 1
    if col[0] == 0:
        indexes.reverse()
        newColIndexer, incrementer = 3, -1
    oldColIndexer = indexes[0]
    while oldColIndexer in indexes:
        if oldCol[oldColIndexer] == col[newColIndexer]:
            squareToMove = findSquareDict[oldColIndexer]
            squareToMove.glide((newColIndexer, col_n))
        else:
            squareToMerge1 = findSquareDict[oldColIndexer]
            oldColIndexer += incrementer
            squareToMerge2 = findSquareDict[oldColIndexer]
            combine(squareToMerge1, squareToMerge2, board, \
                    (newColIndexer, col_n))
        newColIndexer += incrementer
        oldColIndexer += incrementer
    return True

def combine(squareA, squareB, board, mergeLoc):
    '''
    Combine 2 square objects and update the score
    '''
    squareA.glide(mergeLoc)
    canvas, guiBoard = squareA.canvas, squareA.gui
    squareB.glide(mergeLoc)
    newVal = squareB.value + squareA.value
    squareA.gui.score += newVal
    del squareA
    del squareB
    board[mergeLoc] = Square(canvas, mergeLoc, newVal, board, guiBoard)

def make_move_on_list(numbers):
    '''
    Make a move given a list of 4 numbers using the rules of the
    2048 game.

    Argument: numbers -- a list of 4 numbers
    Return value: the list after moving the numbers to the left.
    '''

    assert len(numbers) == 4
    numbers.sort(key=bool, reverse=True) # Saved me like a 4-line for loop :)
    newLst = []
    i = 0 #represents which number in the original list we're looking at moving
    while i < 4:
        newLst.append(numbers[i])
        if not numbers[i] or i == 3:
            break;
        if numbers[i] == numbers[i+1]:
            newLst[-1] += numbers[i]
            i += 1
        # if 2 adjacent numbers are the same, don't have to look at second
        # number, can skip it
        i += 1
    newLst += [0]*(4-len(newLst)) # make the list the right size
    return newLst

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

    Return value: false if move does not change the board, true if move changes
    the board.
    '''

    assert cmd in ['w', 'a', 's', 'd']
    isMove = False
    if cmd in ['w', 's']:
        for col_n in range(4):
            col = get_column(board, col_n)
            if cmd == 's':
                col.reverse()
                col = make_move_on_list(col)
                col.reverse()
            else:
                col = make_move_on_list(col)
            if put_column(board, col, col_n):
                isMove = True
    else:
        for row_n in range(4):
            row = get_row(board, row_n)
            if cmd == 'd':
                row.reverse()
                row = make_move_on_list(row)
                row.reverse()
            else:
                row = make_move_on_list(row)
            if put_row(board, row, row_n):
                isMove = True
    return isMove

def game_over(board):
    '''
    Check to see if the game is over (either 2048 is reached or no moves are
    left.
        
    Arguments:
    board  -- the game board
    Return value: False if game continues, True if game is over.
    '''
    
    for square in board.values():
        if square.value == 2048:
            return True
    cols = []
    rows = []
    for i in range(4):
        cols.append(get_column(board, i))
        rows.append(get_row(board, i))
    for i in range(4):
        for j in range(4):
            if not cols[i][j] or not rows[i][j]:
                return False
            if i < 3:
                if cols[i][j] == cols[i+1][j] or rows[i][j] == rows[i+1][j]:
                    return False
    return True

def update(board, cmd, canvas, guiBoard):
    '''
    Make a move on a board given a movement command.  If the board
    has changed, then add a new square (square has value 2 or 4, 90%
    probability it's a 2) on a randomly-chosen empty place on the board.

    Arguments:
      board  -- the game board
      cmd    -- the command letter

    Return value: none; the board is updated in-place.
    '''

    if make_move(board, cmd):
        possibleLocs = []
        for row in range(4):
            for col in range(4):
                possibleLocs.append((row,col))
        for loc in board:
            possibleLocs.remove(loc)
        locToAddTo = random.choice(possibleLocs)
        if random.random() < 0.9:
            board[locToAddTo] = Square(canvas, locToAddTo, 2, board, guiBoard)
        else:
            board[locToAddTo] = Square(canvas, locToAddTo, 4, board, guiBoard)


if __name__ == '__main__':
    root = Tk()
    root.geometry('800x800')
    canvas = Canvas(root, width=800, height=800)
    canvas.pack()
    board, guiBoard = make_board(canvas)
    root.bind('<Key>', guiBoard.keyHandler)
    guiBoard.displayText('Welcome to better 2048 by Akshay!')
    root.mainloop()

