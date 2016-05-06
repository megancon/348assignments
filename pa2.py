# File: Player.py
# Author(s) names: Ryan Miller, Megan Conlon, Sebastian Garcia
# Date:
# Group work statement: All group members were present and contributing during all work on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        a = -INFINITY
        b = INFINITY
        move = -1
        turn = self
        score = -INFINITY

        for m in board.legalMoves(self):
            if (ply ==0):
                return (self.score(board), m)
                #if we're at ply 0, call eval function & return
            if board.gameOver():
                return (-1,-1)
                #can't make a move, the game is over
            nb = deepcopy(board)
                # Copy the board so that we don't ruin it
            nb.makeMove(self, m)
            #try the move
            s = self.abMin(board, a, b, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            a = max(score, a)
        #returns the score and the associated move
        return (score, move)

    def abMax(self, board, a, b, ply, turn):
        if board.gameOver():
            return turn.score(board)
        v = -INFINITY
        for m in board.legalMoves(self):
            if ply==0:
                return turn.score(board)
            opponent = custom(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.abMin(nextBoard, a, b, ply-1, turn)
            # Keep largest returned result
            v = max(v, s)
            # If greater than beta, it's useless to keep going; Resistance is futile!
            if v >= b:
                return v
            # Otherwise, update alpha if needed and continue
            a = max(a, v)
        return v

    def abMin(self, board, a, b, ply, turn):
        if board.gameOver():
            return turn.score(board)
        v = INFINITY
        for m in board.legalMoves(self):
            if ply==0:
                return turn.score(board)
            opponent = custom(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.abMax(nextBoard, a, b, ply-1, turn)
            # Keep smallest returned result
            v = min(v, s)
            # If less than alpha, it's useless to keep going; Resistance is futile!
            if v <= a:
                return v
            # Otherwise, update beta if needed and continue
            b = min(b, v)
        return v

    def customMove(self, board, ply):
        if board.scoreCups[self.num - 1] == 0:
            cupthree = board.getPlayersCups(self.num)[2] #define the third cup in the board
            cuptwo = board.getPlayersCups(self.num)[1] #define the third cup in the board
            for m in board.legalMoves(self):
                nextBoard = deepcopy(board)
                # Copy the board so that we don't ruin it
                nextBoard.makeMove(self, m)
                # See next board state for current move
                if cupthree == 4 and nextBoard.getPlayersCups(self.num)[2] == 0:
                    return (100, m)
                # if the move is the one we want, choose it
                elif cuptwo == 5 and nextBoard.getPlayersCups(self.num)[1] == 0:
                    return (100, m)
                # if the move is the one we want, choose it
        val, move = self.alphaBetaMove(board, ply)
        return (val, move)

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "Random chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "Mini chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "ABPruner chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.customMove(board, self.ply)
            print "Custom Player chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


class custom(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply=10):
        """Initialize a MancalaPlayer."""
        Player.__init__(self, playerNum, playerType, ply)

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        ret = board.scoreCups[0] - board.scoreCups[1] #find the difference in stones between the mancalas
        numStones = 6 #establish a variable holding the number of stones we want to check for
        for cup in board.getPlayersCups(self.num): #iterate through all of the cups, starting with the furthest cup from our mancala
            if cup == numStones: #if the board contains a state in which we can score an extra turn
                ret += 2 #add two points to that board
            numStones -= 1
        return ret
