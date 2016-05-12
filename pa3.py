#!/usr/bin/env python

#Megan Conlon, Ryan Miller, Sebastian Garcia 
#All group members were present and contributing during all work on this project.

import struct, string, math, time, copy
from copy import *


class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size  # the size of the board
      self.CurrentGameBoard = board  # the current state of the game board
      self.startTime = 0.0

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""
    f = open(filename, 'r')
    BoardSize = int(f.readline())
    NumVals = int(f.readline())

    # initialize a blank board
    board = [[0 for i in range(BoardSize)] for j in range(BoardSize)]

    # populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1] = val
    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    # check each cell on the board for a 0, or if the value of the cell
    # is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            # determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def MRV(board, domain_array):
    """ Takes a board and an array of all of the domains of every box.
    Looks through the board and for every space that has not yet been
    assigned a value, examines the domains for the lowest value. Once that
    domain has been located, returns the x and y values to the solve function."""
    lowest_length = len(board) # sets lowest length of domains = to size of board
    target_row = 0
    target_column =0
    for i in range (0,len(board)):
        for j in range (0, len(board)):
            if board[i][j] == 0:  # if there is no value in the current box
                if len(domain_array[i][j]) < lowest_length:  # AND if the current box's domain has less possible values than the lowest one we've looked at
                    lowest_length = len(domain_array[i][j])  # we set lowest length = to that box's length of domain
                    target_row = i  # index the row coordinate
                    target_column = j  # index the column coordinate
    return target_row, target_column  # return the row and column of the unassigned square with the minimum remaining values

def LCV(board_class, domain_array, row, col):
    #Takes a square and returns the domain ordered by assignment values that
    #leave the most options for affected squares
    board = board_class.CurrentGameBoard
    size = board_class.BoardSize
    # How large each quadrant is and which one we're in
    quadlen = int(math.sqrt(size))
    quadnumrow = int(math.floor(row / quadlen))
    quadnumcol = int(math.floor(col / quadlen))
    D = domain_array[row][col]  # domain of our square
    numremvals = []  # will hold the sum of all domain lengths of squares affected by each move
    for v in D:
        # create copy of the domain array so we can make an assignment and forward check it
        domainscopy = domain_array
        domainscopy = forward_checking(board_class, domainscopy, row, col, v)
        s = 0
        # add up the domain length for each square in the same row and column as our square
        for i in range(len(D)):
            if (not (i == col)):
                s += len(domainscopy[row][i])
            if (not (i == row)):
                s += len(domainscopy[i][col])
        # add up the domain length for each square in the same quadrant as our square
        for j in range(quadlen):
            for i in range(quadlen):
                s += len(domainscopy[quadlen * quadnumrow + j][quadlen * quadnumcol + i])
        # store sum in this array, matched by index to it's value assignment in D
        numremvals.append(s)
    dsorted = []
    for i in range(len(D)):
        # Place the D value at index number of each numremvals entry into dsorted in a sorted order
        for j in range(len(D)):
            x = 0
            if numremvals[j] > x:
                x = numremvals[j]
                ind = j
        numremvals[ind] = 0
        dsorted.append(D[ind])
    print "row, col = " + str(row) + ", " + str(col)
    print "d sorted is"
    print dsorted
    return dsorted

def forward_checking(board_class, domains, row, col, val):
    """Takes a value assignment and removes that value from the domains
    of all the squares in the same row, same column, and same quadrant"""
    board = board_class.CurrentGameBoard
    size = board_class.BoardSize
    quadlen = int(math.sqrt(size))  # size of the quadrant
    for j in range(size):  # traversing the row and column of our square
    # ignoring the chosen square, remove value from domain of each square
        if (not (j == col)) and domains[row][j].count(val)== 1:
            domains[row][j].remove(val)
        if (not (j == row)) and domains[j][col].count(val) == 1:
            domains[j][col].remove(val)
    # Find which quadrant we are in
    quadnumrow = int(math.floor(row / quadlen))
    quadnumcol = int(math.floor(col / quadlen))
    # Remove value from domain of each square in quadrant
    for j in range(quadlen):
        for i in range(quadlen):
            if domains[quadlen * quadnumrow + j][quadlen * quadnumcol + i].count(val) == 1:
                domains[quadlen * quadnumrow + j][quadlen * quadnumcol + i].remove(val)
    return domains

def degree_heuristic(board):
    """Most Constrained Variable: Chooses the variable that is involved in the
       largest number of constraints with other unassigned variables"""
    maxConstraints = -1
    target_row=-1
    target_col=-1
    mcv_count = 0
    size = len(board.CurrentGameBoard)
    subsquare = int(math.sqrt(size))
    board_size = board.BoardSize
    #board.print_board()
    ##test = [ [ 0 for i in range(size) ] for j in range(size) ]

    for row in range(0,board_size):
        for col in range(0,board_size):
            mcv_count = 0
            if (board.CurrentGameBoard[row][col] == 0):

                #Check rows and columns for conflicts
                for i in range(board_size):
                    if ((board.CurrentGameBoard[row][i]==0) and i != col and i//subsquare!=subsquare):
                        mcv_count += 1
                    if ((board.CurrentGameBoard[i][col]==0) and i != row and i//size!=subsquare):
                        mcv_count += 1

                #determine which square the cell is in and find conflicts
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((board.CurrentGameBoard[SquareRow*subsquare+i][SquareCol*subsquare+j])==0
                            and (SquareRow*subsquare + i != row)
                            and (SquareCol*subsquare + j != col)):
                                mcv_count += 1
                if maxConstraints < mcv_count:
                    maxConstraints = mcv_count
                    target_row = row
                    target_col = col
                #test[row][col]=mcv_count
    #print test
    return target_row, target_col


def solve(initial_board, myForward_checking = False, myMRV = False, myDegree = False, myLCV = False):
    """Calls solve_helper. This adds an extra layer before we call the recursive
    function so we can create an array that holds the domains of all squares
    and update it as we go"""

    s = initial_board.BoardSize
    initial_board.startTime = time.time()
    domain_array = [[0 for x in range(s)] for y in range(s)]

    for i in range(s):
        for j in range(s):
            domain_array[i][j] = range(1, s + 1)
    for i in range(s):
        for j in range(s):
            val = initial_board.CurrentGameBoard[i][j]
            if (val != 0):
                domain_array = forward_checking(initial_board, domain_array, i, j, val)
    res = solver_helper(initial_board, domain_array, myForward_checking, myMRV, myDegree, myLCV)
    print time.clock()
    return res


def solver_helper(initial_board, domain_array, myForward_checking, myMRV, myDegree, myLCV):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    BoardArray = initial_board.CurrentGameBoard
    if is_complete(initial_board):
        print "Board completed"
        return initial_board
    row, col = -1, -1

    if myMRV:
        row, col = MRV(BoardArray, domain_array)  # select an unassigned square using the MRV heuristic
    elif myDegree:
        row, col = degree_heuristic(initial_board)
        print row, col # select an unassigned square using the Degree heuristic
    else:
        for i in range(len(BoardArray)):
            for j in range(len(BoardArray)):
                if BoardArray[i][j] == 0:
                    row, col = i, j
                    break
            if not (row == -1):
                break     # find the first unassigned square in the board
        if row == -1:
            print "Return A"
            return initial_board   # all squares are full, board unable to solve
    if myLCV:
        domain_test = deepcopy(domain_array)
        D = LCV(initial_board, domain_test, row, col)  # select an ordering for the domain of X(the chosen unassigned square) using LCV
    else:
        D = domain_array[row][col]  # use unordered domain of X (the chosen unassigned square)
   ## print range(len(D))
    iterate = range(len(D))
    for i in iterate:
        print "Iterate = " + str(iterate)
        print "i = " + str(i)
        domain_copy = deepcopy(domain_array)
        new_board = deepcopy(initial_board)
        if conflict_checker(new_board, D[i], row, col):
            new_board.set_value(row, col, D[i])  # assign value to the selected square
            new_board.print_board()
            if myForward_checking:
                domain_copy = forward_checking(new_board, domain_copy, row, col, D[i])  # update domains of all squares
            else:
                domain_copy[row][col] = [D[i]]
            result = solver_helper(new_board, domain_copy, myForward_checking, myMRV, myDegree, myLCV) # assign the rest of the unassigned squares in the board
            if not (result == "failure"):
                print "Return B"
                return result    # no more moves, board is completed
        print range(len(D))

    print "Return C"
    return "failure"

def conflict_checker(board, val, row, col):
    """ looks at the row and col and subsaquare of a certain square for duplicate values.
    returns fizzity-false if returns, #truuuu if no conflict was found"""
    current_board = board.CurrentGameBoard
    size = board.BoardSize
    quadlen = int(math.sqrt(size))
    subsquare_row = row / quadlen
    subsquare_col = col / quadlen

    i = 0

    while i < size:
        if ((current_board[row][i] == val) and i != col):
            return False
        if ((current_board[i][col] == val) and i != row):
            return False
        i += 1

    i = 0

    while i < quadlen:
        j = 0
        while j < quadlen:
            if ((current_board[subsquare_row*quadlen+i][subsquare_col*quadlen+j] == val)
                and (subsquare_row*quadlen != row)
                and (subsquare_col*quadlen != col)):
                    return False
            j+= 1
        i +=1
    return True
