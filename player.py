import engine
from tkinter import *


# Akshay Yeluri

class GUIBoard:
    '''
    A GUI Board is an object that is visually presented on a tkinter canvas.
    Remembers the board dictionary it is created with, the canvas it's on,
    as well as what text is written on it, and creates a new dictionary
    where the keys are occupied positions on the board, while values are the
    square objects at those positions. Also has a list of dictionaries that are
    previous states of the board, used as a stack to undo moves.
    '''
    
    def __init__(self, board, canvas):
        self.canvas = canvas
        self.board = board
        instructions = 'Press arrow keys to move, q to quit, z to undo.'
        self.canvas.create_text((400,680),font=('Verdana',30),text=instructions)
        for i in range(200,700,100):
            self.canvas.create_line(i,200,i,600, width=4, fill='#c0c0c0')
            self.canvas.create_line(200,i,600,i, width=4, fill='#c0c0c0')
            self.textHandle = None
        self.dictOfSquares = {}
        self.updateGUIBoard()
        self.boardLastStates = []

    def getLoc(self, pos):
        '''Converts a position (a row/column tuple) to a location (a tuple
        of pixel coordinates)
        '''
        posToPixelPos = { 0: 250,
                          1: 350,
                          2: 450,
                          3: 550 }
        yCoor, xCoor = pos
        yCoor, xCoor = posToPixelPos[yCoor], posToPixelPos[xCoor]
        return (xCoor, yCoor)

    def displayText(self, text):
        '''Deletes the old text being displayed, and replaces with new text.'''
        self.canvas.delete(self.textHandle)
        self.textHandle = self.canvas.create_text((400, 100), \
                                              font=('Verdana',40), text=text)

    def keyHandler(self, event):
        '''Event handling function called when a key is pressed. Checks if key
        is a valid move, ends game if q is entered, otherwise makes a move on
        the dictionary board and checks if the game is over. If not,
        sets up for the next move.
        '''

        movesDict = { 'Left': 'a',
                      'Right': 'd',
                      'Up': 'w',
                      'Down': 's' }
        if event.keysym not in ['Left', 'Right', 'Up', 'Down', 'q', 'z']:
            self.displayText('Invalid move! Try again...')
            return
        if event.keysym == 'q':
            quit()
        if event.keysym == 'z':
            lastState = self.boardLastStates.pop()
            self.board = lastState.copy()
            self.updateGUIBoard()
        else:
            cmd = movesDict[event.keysym]
            self.boardLastStates.append(self.board.copy())
            # Save last state of board for undo option.
            engine.update(self.board, cmd)
            self.updateGUIBoard()
            self.displayText('Enter Move: ')
        if engine.game_over(self.board):
            self.displayText('Game over!')
            quit()


    def updateGUIBoard(self):
        '''
        Updates the gui Board based on the board dictionary. First deletes
        all old square objects on the board (found using the dictOfSquare items)
        and then creates new square objects at every position in the board dict.
        '''
        for pos, square in self.dictOfSquares.items():
            del square
            # Delete all the squares on the GuiBoard
        self.dictOfSquares.clear()
            # Clear the dictionary of squares
        for pos, value in self.board.items():
            self.dictOfSquares[pos] = Square(canvas, self.getLoc(pos), value)
            # Rebuild the dictionary of squares and put squares on gui board


class Square:
    '''
    A class of objects called squares that exist also as values in the board
    dictionary, literal square shapes on a canvas.
    '''
    def __init__(self, canvas, loc, value):
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
        self.color = colorValueDict.get(value, '#ffffff')
        self.canvas = canvas
        self.loc = loc #Remember, a loc is pixel coords, a pos is row/column #
        self.size = 96
        x1, y1 = self.loc
        x2, y2 = x1, y1
        self.handle = self.canvas.create_rectangle(x1, y1, \
                                   x2, y2, fill=self.color, outline=self.color)
        self.textHandle = self.canvas.create_text((x1,y1), \
                                      font=('Verdana', 0), text=str(self.value))
        self.grow()

    def grow(self, rev=False):
        '''
        This function will take a square at a given location and slowly grow it
        till its the size specified in the constructor statement.'''
        x1o, y1o = self.loc
        x2o, y2o = x1o, y1o
        sizes = list(range(0, self.size // 2 + 1, 24))
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
        '''
        Will shrink specified square on the canvas, and eventually delete it,
        and will also delete the text number on each square, before destroying a
        square object.
        '''
        self.grow(rev=True)
        self.canvas.delete(self.handle)
        self.canvas.delete(self.textHandle)

if __name__ == '__main__':
    root = Tk()
    root.geometry('800x800')
    canvas = Canvas(root, width=800, height=800)
    canvas.pack()
    guiBoard = GUIBoard(engine.make_board(), canvas)
    root.bind('<Key>', guiBoard.keyHandler)
    guiBoard.displayText("Welcome to Akshay's 2048 GUI!")
    root.mainloop()
