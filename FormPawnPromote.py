import sys
import pygame as pg
from config import SQ_SIZE

# Config
WIDTH_PROMOTE = SQ_SIZE
HEIGHT_PROMOTE = SQ_SIZE * 4
ROW = 4

# Dictionary contain promote image
IMG = {}

whitePromotes = ["wQ", "wB", "wR", "wN"]

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font("guiPNG/font.ttf", size)


def loadPromoteImage():
    for promote in whitePromotes:
        IMG[promote] = pg.transform.scale(pg.image.load("images/" + promote + ".png"), (SQ_SIZE, SQ_SIZE))


def drawPromoteImage(screen, rec, col):
    loadPromoteImage()
    i = 0
    for promote in whitePromotes:
        if i < ROW:
            screen.blit(IMG[promote], (rec.get_width() * col, (rec.get_height() - SQ_SIZE / 2) / ROW * i))
            i += 1

def drawPromote(screen, col, row):

    # Tao ra mot surface tren screen
    rec = pg.Surface((WIDTH_PROMOTE, HEIGHT_PROMOTE+SQ_SIZE/2))
    rec.fill("gray")

    screen.blit(rec, (WIDTH_PROMOTE * col, HEIGHT_PROMOTE / ROW * row))  # (SQ_SIZE * 7, SQ_SIZE * 0)

    drawPromoteImage(screen, rec, col)

    # Tao ra mot surface chua nut Exit
    recExit = pg.Surface((WIDTH_PROMOTE, SQ_SIZE/2))
    recExit.fill(pg.Color("White"))
    screen.blit(recExit, (WIDTH_PROMOTE * col, ((HEIGHT_PROMOTE + SQ_SIZE/2)/(ROW + 0.5)) * ROW))
    font = pg.font.Font("guiPNG/font.ttf", 12)
    text = font.render("EXIT", True, pg.Color("Black"))
    text_rect = pg.Rect(WIDTH_PROMOTE * col, ((HEIGHT_PROMOTE + SQ_SIZE/2)/(ROW + 0.5))*ROW, WIDTH_PROMOTE, SQ_SIZE/2).move(WIDTH_PROMOTE / 2 - text.get_width() / 2, SQ_SIZE / 4 - text.get_height() / 2)
    screen.blit(text, text_rect)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        if e.type == pg.MOUSEBUTTONDOWN:
            MOUSE_POS = pg.mouse.get_pos()
            c = MOUSE_POS[0] // SQ_SIZE # Tra ve x
            r = MOUSE_POS[1] // SQ_SIZE # Tra ve y
            if c == col:
                if r == 0:
                    pieceName = "Q"
                    return
                elif r == 1:
                    pieceName = "B"
                    return
                elif r == 2:
                    pieceName = "R"
                    return
                elif r == 3:
                    pieceName = "N"
                    return
                elif r >= 4:
                    return



