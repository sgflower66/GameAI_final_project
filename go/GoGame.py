from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .GoLogic import Board
import numpy as np


class GoGame(Game):
    def __init__(self, n = 8):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # print(action)
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        # print(move)
        # display(b.pieces)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, history_board, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        valids[-1] = 1
        if len(legalMoves)==0:
            return np.array(valids)
        for x, y in legalMoves:
            temp_board = np.copy(b.pieces)
            b.execute_move((x,y), player)
            # TODO
            valids[self.n*x+y]=1
            for _ in range(len(history_board)):
                if (np.array(b.pieces) == history_board[_]).all():
                    valids[self.n*x+y] = 0
                    # break;
                if (np.array(b.pieces) == -1*history_board[_]).all():
                    valids[self.n*x+y] = 0
                    # break;
                
            b.pieces = np.copy(temp_board)

        return np.array(valids)

    def getGameEnded(self, history_board, board, player, action):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)

        move = (-1,-1) if action==self.n*self.n else (int(action/self.n),action%self.n)


        if action == self.n*self.n and (board==-1*history_board[-1]).all():
            return np.sign(b.countDiff(player) - 0.75)

        if action == self.n*self.n and (board==history_board[-1]).all():
            return np.sign(b.countDiff(player) - 0.75)

        if (not b.has_legal_moves(player)) and (not b.has_legal_moves(-player)):
            return np.sign(b.countDiff(player) - 0.75)

        return 0
        

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

def display(board):
    n = board.shape[0]
    print ("   ",end="")
    for y in range(n):
        print (y,"",end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|",end="")    # print the row #
        for x in range(n):
            piece = board[y][x]    # get the piece to print
            if piece == -1: print("b ",end="")
            elif piece == 1: print("W ",end="")
            else:
                if x==n:
                    print("-",end="")
                else:
                    print("- ",end="")
        print("|")

    print("   -----------------------")
