'''
Ve ban co
'''

import pygame as pg
from config import *

def loadImage():  # Load tung anh
    pieces = ["bR", "bN", "bB", "bK", "bQ", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

class Board():
    def __init__(self):
        loadImage()

    # Ve mot ban co hoan chinh
    def drawGameState(self, screen, gs, validMoves, sqSelected):
        self.drawBoard(screen)  # Ve ra mot ban co voi kich thuoc WIDTH, HEIGHT
        self.drawPieces(screen, gs.board)  # Ve ra quan co tren ban co dua vao gamestate.board hien tai
        self.drawHighLight(screen, gs, validMoves, sqSelected)  # Ve highlight cho lua chon

    # Ve ban co va cac o vuong
    def drawBoard(self, screen):
        colors = [pg.Color('white'), pg.Color('gray')]  # vi tri tuong ung 0, 1
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row + col) % 2]  # tra ve hai so 0, 1 dua tren tong trung binh cua hang va cot va to mau tuong ung
                pg.draw.rect(screen, color, pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Rect(toa do goc x, toa do y, cd, cr)

    # Ve quan co len ban co
    def drawPieces(self, screen, board):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = board[row][col]
                if piece != "--":
                    screen.blit(IMAGES[piece], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Load hinh anh vao mot set

    # Ve chu
    def drawText(self, screen, text, colorOne, colorTwo):
        font = pg.font.SysFont("Helvitca", 32, True, False)
        textObject = font.render(text, 0, pg.Color(colorOne))
        textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, 0, pg.Color(colorTwo))
        screen.blit(textObject, textLocation.move(2, 2))

    # Ve duong di quan co
    def drawHighLight(self, screen, gs, validMoves, sqSelected):
        if sqSelected != ():
            r, c = sqSelected
            if gs.board[r][c][0] == 'w' or gs.board[r][c][0] == 'b':
                # To mau cho o dang chon
                s = pg.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100) # Do trong suot cua mau sac
                s.fill(pg.Color("Orange"))
                screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE)) # Ve lop anh mau cam len odang co toa do chuot dang chon
                # To mau cho cac o duong di
                s.fill(pg.Color("Yellow")) # doi mau tu cam sang vang
                for move in validMoves:
                    if move.startRow == r and move.startCol == c: # Neu dung la quan co minh dang chon
                        screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE)) # Ve lop anh mau vang len duong di cua no

    def drawPromote(self, isPawnPromote):
        pass

    def drawChessNotation(self):
        pass

    def drawConfirmMessage(self, screen):


        screen.blit()
