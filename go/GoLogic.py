'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

from queue import Queue

class Board():

    # list of all 4 directions on the board, as (x,y) offsets
    __directions = [(1,0),(0,-1),(-1,0),(0,1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        self.prev_x = -1
        self.prev_y = -1

        self.move_count = 0


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        # TODO 
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
                if self[x][y]==-color:
                    count -= 1
        return count

    def is_move_legal(self, move, color):
        x, y = move[0], move[1]

        # piece already exited
        if self.out_of_board(x, y) or self[x][y] != 0:
            return False

        self[x][y] = color

        ok = self.liberty(x, y)
        for d in self.__directions:
            nx, ny = x + d[0], y + d[1]
            if self.out_of_board(nx, ny):
                continue
            if self[nx][ny] == -color and not self.liberty(nx, ny):
                ok = True

        self[x][y] = 0
        return ok

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = []  # stores the legal moves.
        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self.is_move_legal((x, y), color):
                    moves.append((x,y))
        return moves

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self.is_move_legal((x, y), color):
                    return True
        return False


    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        x, y = move[0], move[1]
        if self.prev_x == x and self.prev_y == y:
            self.prev_x, self.prev_y = -2, -2
        else:
            self.prev_x, self.prev_y = x, y
        
        self.move_count += 1

        if move == -1:
            return

        self[x][y] = color
        for d in self.__directions:
            nx, ny = x + d[0], y + d[1]
            if self.out_of_board(nx, ny):
                continue
            if self[nx][ny] == -color and not self.liberty(nx, ny):
                self.liberty(nx, ny, True)
         

    def liberty(self, x, y, take = False):
        color = self[x][y]
        if color == 0:
            return None
        visited = set()
        q = Queue()
        q.put((x,y))
        while not q.empty():
            now = q.get()
            visited.add(now)
            for d in self.__directions:
                nx, ny = now[0] + d[0], now[1] + d[1]
                if (nx, ny) in visited:
                    continue
                if self.out_of_board(nx, ny):
                    continue
                if self[nx][ny] == 0:
                    return True
                elif self[nx][ny] == color:
                    q.put((nx,ny))
        if take:
            for t in visited:
                self[t[0]][t[1]] = 0 
        return False 

    def out_of_board(self, x, y):
        if x<0 or y<0 or x>=self.n or y>= self.n:
            return True
        return False


   

