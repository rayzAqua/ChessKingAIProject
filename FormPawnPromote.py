import sys
import pygame as pg
from config import *

# Config
WIDTH_PROMOTE = SQ_SIZE
HEIGHT_PROMOTE = SQ_SIZE * 4
ROW = 4

# Dictionary contain promote image
whitePromotes = ["wQ", "wB", "wR", "wN"]
blackPromotes = ["bQ", "bB", "bR", "bN"]
pg.init()

temp = PIECE_NAME


def loadWhitePromoteImage(IMG):
    for whitePromote in whitePromotes:
        IMG[whitePromote] = pg.transform.scale(pg.image.load(
            "images/" + whitePromote + ".png"), (SQ_SIZE, SQ_SIZE))


def loadBlackPromoteImage(IMG):
    for blackPromote in blackPromotes:
        IMG[blackPromote] = pg.transform.scale(pg.image.load(
            "images/" + blackPromote + ".png"), (SQ_SIZE, SQ_SIZE))


def drawPromoteImage(screen, s, col, row, whiteToMove):
    IMG = {}
    if whiteToMove:  # Ve tu hang so 0
        loadWhitePromoteImage(IMG)
        for whitePromote in whitePromotes:
            if row < ROW:
                screen.blit(IMG[whitePromote], (s.get_width()
                            * col, s.get_height() / ROW * row))
                row += 1

    else:  # Ve tu hang so 7
        loadBlackPromoteImage(IMG)
        for blackPromote in blackPromotes:
            if ROW <= row:
                screen.blit(IMG[blackPromote], (s.get_width()
                            * col, s.get_height()/ROW * row))
                row -= 1


def drawPawnPromote(screen, endCol, endRow, whiteToMove):
    col = endCol
    row = endRow

    # Tao ra chu exit
    font = pg.font.Font("guiPNG/font.ttf", 12)
    text = font.render("EXIT", True, pg.Color("Black"))
    # Ve button exit
    if whiteToMove:
        s = pg.Surface((WIDTH_PROMOTE, HEIGHT_PROMOTE))
        s.fill("Green")
        # (SQ_SIZE * 7, SQ_SIZE * 0)
        screen.blit(s, (WIDTH_PROMOTE * col, HEIGHT_PROMOTE / ROW * (ROW-ROW)))
        # Ve hinh anh len surface s
        drawPromoteImage(screen, s, col, row, whiteToMove)
        # Tao ra mot surface chua nut Exit
        recExit = pg.Surface((WIDTH_PROMOTE, SQ_SIZE / 2))
        recExit.fill(pg.Color("Yellow"))
        # Ve surface Exit len man hinh
        screen.blit(recExit, (WIDTH_PROMOTE * col,
                    ((HEIGHT_PROMOTE + SQ_SIZE / 2) / (ROW + 0.5)) * ROW))
        # Ve chu len surface Exit
        text_rect = pg.Rect(WIDTH_PROMOTE * col, ((HEIGHT_PROMOTE + SQ_SIZE / 2) / (ROW + 0.5)) * ROW, WIDTH_PROMOTE,
                            SQ_SIZE / 2).move(WIDTH_PROMOTE / 2 - text.get_width() / 2,
                                              SQ_SIZE / 4 - text.get_height() / 2)
        screen.blit(text, text_rect)
    else:
        s = pg.Surface((WIDTH_PROMOTE, HEIGHT_PROMOTE))
        s.fill("Green")
        # (SQ_SIZE * 7, SQ_SIZE * 0)
        screen.blit(s, (WIDTH_PROMOTE * col, HEIGHT_PROMOTE / ROW * ROW))
        # Ve hinh anh len surface s
        drawPromoteImage(screen, s, col, row, whiteToMove)
        # Tao ra mot surface chua nut Exit
        recExit = pg.Surface((WIDTH_PROMOTE, SQ_SIZE / 2))
        recExit.fill(pg.Color("Yellow"))
        # Ve surface Exit len man hinh
        screen.blit(recExit, (WIDTH_PROMOTE * col,
                    ((HEIGHT_PROMOTE / ROW) * (ROW - 0.5))))
        # Ve chu len surface Exit
        text_rect = pg.Rect(WIDTH_PROMOTE * col, ((HEIGHT_PROMOTE / ROW) * (ROW - 0.5)), WIDTH_PROMOTE,
                            SQ_SIZE / 2).move(WIDTH_PROMOTE / 2 - text.get_width() / 2, SQ_SIZE / 4 - text.get_height() / 2)
        screen.blit(text, text_rect)
    # Tao ra mot surface tren screen
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN:
                MOUSE_POS = pg.mouse.get_pos()
                c = MOUSE_POS[0] // SQ_SIZE  # Tra ve x
                r = MOUSE_POS[1] // SQ_SIZE  # Tra ve y
                if c == col:  # Neu toa do tro chuot bang voi cot dang chon neu ko bang thi la ko tra ve gi
                    if whiteToMove:  # Vi tri trigger phong ham cua quan trang
                        if r == 0:
                            return "Q"
                        elif r == 1:
                            return "B"
                        elif r == 2:
                            return "R"
                        elif r == 3:
                            return "N"
                        elif r >= 4:
                            return ""
                    else:  # Vi tri trigger phong ham cua quan den
                        if r == 7:
                            return "Q"
                        elif r == 6:
                            return "B"
                        elif r == 5:
                            return "R"
                        elif r == 4:
                            return "N"
                        elif r <= 3.5:
                            return ""
                else:  # Neu toa do khong dung voi cot giao dien phong ham
                    return ""
        pg.display.update()

# main()
