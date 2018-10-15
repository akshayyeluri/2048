# Name: Akshay Yeluri
# Login: ayeluri

# ---------------------------------------------------------------------- 
# Part 1: Pitfalls
# ---------------------------------------------------------------------- 

# 1.1: 1) In the list of arguments, the variable 'lst' is given as a string.
#      it should be lst, not 'lst'.
#      2) In the docstring for the function, double quotes are used instead of
#      triple quotes.
#      3) In the first if statement, the assignment operator (=) is used, but
#      it should really be the comparison operator (==).
#      4) The while statement for the while loop is missing the colon after it.
#      5) The else statement inside the while loop is indented one space too
#      many.
#
# 1.2: 1) s should be an argument to the function, not a variable assigned to
#      whatever a user inputs. s = input() is wrong, should be isPalindrome(s)
#      2) The statement lst == lst.reverse() is wrong because lst.reverse()
#      changes a list in place and returns None. Instead, the function should
#      make a copy of list (perhaps with slice notation), and then just run
#      lst.reverse(), and then compare the copy to lst (which) is now flipped.
#      3) The print function call is wrong, instead, there should be if/else
#      statement checking the condition described in 2). If the condition is
#      met, return True, else return False.
#      4) The statement ps += word is wrong because it tries to add a string to
#      a list. In this case, one would instead use ps.append(word) to make the
#      word the next element of the list.
#      5) The statement palindrome.append(ps) is also wrong because this would
#      make the list ps an element of palindrome, instead of combining the two
#      lists. Here the '+' operator would be better, or the method palindromes.
#      extend.
#
# 1.3: 1) The function and variable names should be more descriptive / not one
#      letter / not a meaningless combination of numbers and letters.
#      2) The docstring is incorrectly formatted, should be triple quotes
#      before and after the string.
#      3) There should be a consistent one space before and after every
#      operator (no random large spaces either).
#      4) Lines longer than 80 characters should be either shortened or put on
#      different lines.
#      5) The indent after the if and elif statements should be consistent.

# ---------------------------------------------------------------------- 
# Part 2: Simple functions.
# ---------------------------------------------------------------------- 

import random, sys

#
# Problem 2.1
#

def draw_box(n):
    '''

    Return a string which, if printed, would draw a box on the terminal.  The
    exterior of the box should be made from '+' '-' and '|' characters.  The
    interior will have dimensions nxn and the characters will be one of the
    characters 'x', 'y', 'o', or '.', which will occur in order (even between
    lines).  There is a blank line before and after the box contents in the
    returned string.

    Examples:

    >>> print(draw_box(1))

    +-+
    |x|
    +-+

    >>> print(draw_box(2))

    +--+
    |xy|
    |o.|
    +--+

    >>> print(draw_box(3))

    +---+
    |xyo|
    |.xy|
    |o.x|
    +---+

    >>> print(draw_box(4))

    +----+
    |xyo.|
    |xyo.|
    |xyo.|
    |xyo.|
    +----+

    >>> print(draw_box(5))

    +-----+
    |xyo.x|
    |yo.xy|
    |o.xyo|
    |.xyo.|
    |xyo.x|
    +-----+

    >>> print(draw_box(10))

    +----------+
    |xyo.xyo.xy|
    |o.xyo.xyo.|
    |xyo.xyo.xy|
    |o.xyo.xyo.|
    |xyo.xyo.xy|
    |o.xyo.xyo.|
    |xyo.xyo.xy|
    |o.xyo.xyo.|
    |xyo.xyo.xy|
    |o.xyo.xyo.|
    +----------+

    Arguments:
      n -- a positive integer representing the side length of the box.

    Return value: the string representing the box.
    '''
    
    assert n > 0
    topOfBoxString = '\n' + '+' + (n * '-') + '+' + '\n'
    bottomOfBoxString = '+' + (n * '-') + '+' + '\n'
    centerOfBoxString = ''
    charsLst = 'xyo.'
    whichChar = 0
    for i in range(n):
        centerOfBoxString += '|'
        for j in range(n):
            centerOfBoxString += charsLst[whichChar]
            whichChar += 1
            whichChar %= 4
        centerOfBoxString += '|' + '\n'
    boxString = topOfBoxString + centerOfBoxString + bottomOfBoxString
    return boxString

def test_draw_box():
    print(draw_box(1))
    print(draw_box(2))
    print(draw_box(3))
    print(draw_box(4))
    print(draw_box(5))
    print(draw_box(10))

#
# Problem 2.2
#

def roll():
    '''
    Roll two six-sided dice and return their result.
    Arguments: none
    Return value: the result (an integer between 2 and 12).
    '''
    
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    return dice1 + dice2

def craps(verbose):
    '''
    Play one round of craps.

    Arguments: 
      verbose: print out the progress of the game while playing

    Return value: 
      True if the player wins, else False
    '''
    
    # I understand that this is not very DRY code, but I feel it's a lot more
    # readable. The other way I thought about doing it was to save a bunch of
    # strings as the game progressed, and then print them all simultaneously if
    # verbose, but not only did it make the code more complicated, albeit DRYer,
    # it also would not be like printing the progress as the game happened, but
    # would rather display the whole game at once, which did not feel like what
    # we were supposed to do.
    initialRoll = roll()
    if initialRoll in [7, 11]:
        if verbose:
            print(f'You rolled {initialRoll}. You win!')
        return True
    elif initialRoll in [2, 3, 12]:
        if verbose:
            print(f'You rolled {initialRoll}. You lose!')
        return False
    if verbose:
        print(f'Your point is: {initialRoll}')
    while True:
        newRoll = roll()
        if verbose:
            print(f'You rolled {newRoll}')
        if newRoll == initialRoll:
            if verbose:
                print('You hit your point! You win!')
            return True
        elif newRoll == 7:
            if verbose:
                print('You missed your point! You lose!')
            return False

def craps_edge(n):
    '''
    Estimate and return the house edge for craps.
    See https://wizardofodds.com/games/craps/appendix/1/ for an
    analytical derivation.  The result is 1 41/99 % or 1.4141... %.

    Argument: n: the number of rounds played (>= 0)
    Return value: the house edge in percent
    '''
    
    assert n >= 0
    wins = 0
    for round in range(n):
        if craps(False):
            wins += 1
    (pwin, plose) = (wins / n, (n - wins) / n)
    edge = - (pwin - plose) * 100
    return edge

#
# Problem 2.3
#

def remove_indices(lst, indices):
    '''
    Return a copy of a list with the elements at the given indices removed.
    Valid negative indices (between -1 and -(length of list)+1) can be used.
    Out-of-bound indices are ignored.

    Argument:
      lst -- the input list
      indices -- a list of integers representing locations in the list to remove

    Return value:
      The new list.  The old list is not altered in any way.
    '''
    
    newLst = []
    for i, value in enumerate(indices):
        if value < 0:
            indices[i] += len(lst)
    for i, element in enumerate(lst):
        if i not in indices:
            newLst.append(element)
    return newLst

def get_bet_info(bets, cwins):
    '''
    Select the next bet information for a gambling system.

    Arguments:
      bets  -- the list of bets set by the gambling system
      cwins -- the consecutive wins (0, 1) previously

    Result:
      a two tuple containing:
      -- the bet amount;
      -- the indices of the 'bets' array where the bet amount was taken from
    '''
    
    assert len(bets) > 0
    for bet in bets:
        assert bet > 0
    assert cwins in [0, 1, 2]
    betIndices = [0]
    if cwins in [1, 2] and len(bets) > 1:
        betIndices.append(-1)
    if cwins == 2 and len(bets) > 2:
        betIndices.append(1)
    sumOfBet = 0
    for index in betIndices:
        sumOfBet += bets[index]
    return (sumOfBet, betIndices)

def make_one_bet(bankroll, bets, cwins, next_is_win):
    '''
    Play a gambling system for a single bet.

    Arguments:
      bankroll    -- the player's money
      bets        -- the list of bets set by the gambling system
      cwins       -- the consecutive wins previously
      next_is_win -- the next result of the game being played

    Result:
       A tuple consisting of:
       1) the updated bankroll
       2) the updated bets list
       3) the updated consecutive wins (max 2)
    '''

    assert bankroll >= 0
    assert len(bets) > 0
    for bet in bets:
        assert bet > 0
    assert cwins in [0, 1, 2]
    assert next_is_win in [True, False]

    bankrollChange, betIndices = get_bet_info(bets, cwins)
    if bankroll < bankrollChange:
        return (bankroll, [], 0)
    if next_is_win:
        bankroll += bankrollChange
        bets = remove_indices(bets, betIndices)
        if cwins != 2:
            cwins += 1
    else:
        bankroll -= bankrollChange
        bets.append(bankrollChange)
        cwins = 0
    return (bankroll, bets, cwins)


#
# Test code supplied to students.
#

def random_bool():
    '''Return a random True/False value.'''
    return random.choice([True, False])

def one_round(bankroll, bets, verbose):
    '''
    Play a gambling system for a single round.
    Halt if either the desired amount of money is made, or if
    the player's bankroll hits zero.  Return the final bankroll.

    Arguments:
      bankroll    -- the player's money
      bets        -- the list of bets set by the gambling system
      verbose     -- if True, print out debugging information

    Return value: total profit (negative if there was a loss)
    '''

    assert bankroll >= 0
    assert len(bets) > 0
    for bet in bets:
        assert bet > 0

    orig_bankroll = bankroll
    cwins = 0

    if verbose:
        print('bankroll: {}, bets: {}, cwins: {}'.format(bankroll, bets,
            cwins))

    while True:
        # Test the gambling system on craps.
        #result = craps(False)
        # Alternatively, test it on a random uniformly-distributed boolean 
        # result (like flipping heads or tails).
        result = random_bool()
        if verbose:
            print('result: {}'.format(result))
        (bankroll, bets, cwins) = make_one_bet(bankroll, bets, cwins, result)
        if verbose:
            print('bankroll: {}, bets: {}, cwins: {}'.format(bankroll, bets,
                cwins))
        if bets == []:
            break
    profit = bankroll - orig_bankroll
    return profit

def run_gambling_system(verbose):
    '''
    Run multiple iterations of the gambling system,
    carrying on the bankroll from one iteration to the next.
    '''

    niters = 1000
    bankroll = 700
    orig_bankroll = bankroll
    for _ in range(niters):
        bets = [10, 10, 15]
        profit = one_round(bankroll, bets, verbose)
        if verbose:
            print('PROFIT: {}\n'.format(profit))
        bankroll += profit
        if verbose:
            print('BANKROLL: {}'.format(bankroll))
        if bankroll <= 0:
            break
    total_profit = bankroll - orig_bankroll
    if verbose:
        print('TOTAL PROFIT: {}'.format(total_profit))
    return total_profit

def run_gambling_system_multiple_times(n, verbose):
    '''
    Run multiple independent iterations of the gambling system,
    estimating and printing the average profit.
    '''

    total_profit = 0
    for _ in range(n):
        net_profit = run_gambling_system(verbose)
        if verbose:
            print(net_profit)
        total_profit += net_profit
    avg_profit = total_profit / n
    print('AVERAGE PROFIT: {}'.format(avg_profit))

# Example of use:
# run_gambling_system_multiple_times(10000, False)

# ---------------------------------------------------------------------- 
# Miniproject: 2048 game.
# ---------------------------------------------------------------------- 

#
# Problem 3.1
#

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
