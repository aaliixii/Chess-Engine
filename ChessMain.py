'''
main driver file. Responsible for handling user inputs and displaying current GameState
'''

import pygame as p
from PIL import Image
import ChessEngine

p.init()
WIDTH = HEIGHT = 512  # or you can keep it as 512
DIMENSION = 8  # Chess boards are 8x8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = dict.fromkeys(['wR', 'wN', 'wB', 'wQ', 'wK', 'wp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bp'])
SET_FPS = 15


def loadImages ():
    for key in list (IMAGES.keys()):  # Use a list instead of a view
        IMAGES[key] = p.transform.scale(p.image.load('/Users/joshmachado/Desktop/Python_Projects/Chess/images/{}.png'
                                                     .format(key)), (SQ_SIZE, SQ_SIZE))


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('White'))
    loadImages()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False   # flag for when a move is made
    sqSelected = ()    # Empty tuple which will save the position of the last square selected by user
    playerClicks = []  # List of two tuples tracking the clicks eg: [(6,4),(4,4)]

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type ==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row, col):  # If the same square is selected twice, it:
                    sqSelected = ()           # Deselects the square
                    playerClicks = []         # Resets playerClicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks)==2:    # This indicates that 2 clicks have been made (done after second click)
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)

                    if move in validMoves:
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks =[]

                    else:
                        playerClicks = [sqSelected]
            # Key handles
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:      # Undo the move made
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(SET_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

''' 
drawBoard is going to draw just the board without the pieces. 

*Note to self*
Top left square of the chess board is always white irrespective of which colour you're playing with
'''

def drawBoard(screen):
    colours = [p.Color('white'),p.Color('grey')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c)%2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




'''
drawPieces is going to draw the pieces on the board given the current GameState
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
