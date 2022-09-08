'''
This class is responsible for storing information about the current state of the game. It will determine the possible
legal moves in the position. It will also keep logs of moves played.
'''

import numpy as np

class GameState():
    def __init__(self):
        # The board is an 8x8 2D list
        # Each element has two characters
        # The first character represents the colour of the piece 'b' for Black and 'w' for White
        # The second character represents the piece- 'R':Rook, 'N':Knight, 'B':Bishop, 'Q':Queen, 'K':King, 'p':Pawn
        # '--' marks empty squares of the board
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ])
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'B': self.getBishopMoves,
                              'N': self.getKnightMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False
        self.staleMate = False

    '''
    Lol right now every stupid ass possible move works, Need to take care of en-passant and castling 
    '''
    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

        if move.pieceMoved == 'wK':
            self.whiteKingPosition = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingPosition = (move.endRow, move.endCol)

        self.whiteToMove = not self.whiteToMove

    ''' Undo the previous move made by taking the last log from moveLog '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingPosition = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingPosition = (move.startRow, move.startCol)

            self.checkMate = False
            self.staleMate = False


    ''' All moves considering checks'''
    def getValidMoves(self):
        # 1) Generate all possible moves
        moves = self.allPossibleMoves()
        # 2) Make all the possible moves
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            # 3) Get opponent's all possible moves
            # 4) see if king is under attack
            self.whiteToMove = not self.whiteToMove
            if self.Check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # checking for if checkmate or stalemate
        if len(moves)==0:
            if self.Check():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate, self.staleMate = False, False
        return moves

    def Check(self):
        if self.whiteToMove:
            return self.squareAttacked(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:
            return self.squareAttacked(self.blackKingPosition[0], self.blackKingPosition[1])


    def squareAttacked(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.allPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True
        return False


    ''' All moves without considering checks'''
    def allPossibleMoves(self):

        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        # if self.whiteToMove: print('white turn')
        # elif not self.whiteToMove: print('black turn')
        return moves

    ''' All the moves for a pawn located at (r, c) and add them to the list moves'''
    def getPawnMoves(self, r, c, moves):

        if self.whiteToMove:   # checking to see which colour pawn

            if self.board[r-1][c] == '--':                                    # if the sq. ahead of it is empty
                moves.append(Move((r,c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--':                       # if pawn hasn't moved yet
                    moves.append(Move((r,c),(r-2,c), self.board))            # adds the double sq move of the pawn

            if c!=7 and self.board[r-1][c+1][0] == 'b':  # if there is a black piece to capture
                moves.append(Move((r,c),(r-1,c+1), self.board))                   # on right

            if c!=0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r,c), (r-1, c-1), self.board))                 # on left


        if not self.whiteToMove:

            if self.board[r+1][c] == '--':                                    # if the sq. ahead of it is empty
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--':                       # if pawn hasn't moved yet
                    moves.append(Move((r,c),(r+2,c), self.board))            # adds the double sq move of the pawn

            if c!=7  and self.board[r+1][c+1][0] == 'w':  # if there is a white piece to capture
                moves.append(Move((r,c),(r+1,c+1), self.board))                   # on right

            if c!=0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c), (r+1, c-1), self.board))                 # on left



    ''' All the moves for a Rook located at (r, c) and add them to the list moves'''
    def getRookMoves(self, r, c, moves):
        directions = ((-1,0),(1,0),(0,1),(0,-1))    # up, down, right, left
        enemyPiece = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endRow <8 and 0<= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0]==enemyPiece:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    ''' All the moves for a Knight located at (r, c) and add them to the list moves'''
    def getKnightMoves(self, r, c, moves):
        KMove = ((-2,-1), (-2,1), (2,1), (2,-1),                   # 2up-left, 2up-right, 2down-right, 2down-left
                      (-1,-2),(1,-2),(-1,2),(1,2))                      # 2left-up, 2left-down, 2right-up, 2right-down
        allyPiece = 'w'if self.whiteToMove else 'b'
        for m in KMove:
            endRow = r +m[0]
            endCol = c +m[1]
            if 0<= endRow < 8 and 0<= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!=allyPiece:
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    ''' All the moves for a pawn located at (r, c) and add them to the list moves'''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, 1), (-1, -1), (1, 1), (1, -1))  # up-right, up-left, down-right, down-left
        enemyPiece = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range ( 1, 8 ):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyPiece:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    ''' All the moves for a Queen located at (r, c) and add them to the list moves'''
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)


    ''' All the moves for a King located at (r, c) and add them to the list moves'''
    def getKingMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, 1), (-1, -1), (1, 1), (1, -1))
        allyColour = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColour:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


class Move():

    # mapping the row, column format to rank, file format of chess i.e. (8,7)->(6,5) == G1->F3
    rankToRow = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowToRank = {v:k for k,v in rankToRow.items()}
    colToFile = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    fileToCol = {v:k for k,v in colToFile.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol


    '''
    Need to override the equals method cause python can't tell if two objects of the same class with same para are equal
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colToFile[c] + self.rowToRank[r]

