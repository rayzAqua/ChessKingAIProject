'''
Ve ban co
'''

import pygame as pg
import sys

import pygame.font

from config import *
from Button import Button
import FormMainMenu

def loadImage():  # Load tung anh
    pieces = ["bR", "bN", "bB", "bK", "bQ", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load('images/' + piece + '.png'), (SQ_SIZE - 15, SQ_SIZE - 15))


# Ve mot ban co hoan chinh
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # Ve ra mot ban co voi kich thuoc WIDTH, HEIGHT
    drawChessNotation(screen)
    drawPieces(screen, gs.board)  # Ve ra quan co tren ban co dua vao gamestate.board hien tai
    drawHighLight(screen, gs, validMoves, sqSelected)  # Ve highlight cho lua chon
    drawMoveLog(screen, gs)
    # drawMoveButton(screen, gs, Button)
    drawAvatar(screen, gs)


# Ve ban co va cac o vuong
def drawBoard(screen):
    colors = [pg.Color("#FFFFCC"), pg.Color("#669933")]  # vi tri tuong ung 0, 1
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[
                (row + col) % 2]  # tra ve hai so 0, 1 dua tren tong trung binh cua hang va cot va to mau tuong ung
            pg.draw.rect(screen, color, pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE,
                                                SQ_SIZE))  # Rect(toa do goc x, toa do y, cd, cr)


# Ve quan co len ban co
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE).move(5, 5))


# Load hinh anh vao mot set

# Ve chu
def drawText(screen, text, color1, color2, gameOver):

    endGame = pg.Surface((WIDTH/2, HEIGHT/2))
    endGame.fill("Gray32")
    endGame.set_alpha(250)
    screen.blit(endGame, (WIDTH/4, HEIGHT/4))

    decor = pg.Surface((WIDTH/2-50, HEIGHT/7))
    decor.fill("Gray20")
    decor.set_alpha(200)
    screen.blit(decor, (WIDTH/4+25, HEIGHT/4+25))

    font = pg.font.Font("guiPNG/font.ttf", 20)
    textObject = font.render(text, True, pg.Color(color1))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 3 + 5)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, True, pg.Color(color2))
    screen.blit(textObject, textLocation.move(1, 1))

    while gameOver:
        mouse_endgame_pos = pg.mouse.get_pos()
        col = mouse_endgame_pos[0] // SQ_SIZE
        row = mouse_endgame_pos[1] // SQ_SIZE

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                c = mouse_endgame_pos[0] // WIDTH_BUTTON
                r = mouse_endgame_pos[1] // HEIGHT_BUTTON
                if (r, c) == (7, 6):
                    return "undo"
                elif (r, c) == (7, 7):
                    return "reset"
                elif (r, c) == (7, 8):
                    return "back"
        pg.display.update()


# Ve duong di quan co
def drawHighLight(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == 'w' or gs.board[r][c][0] == 'b':
            # To mau cho o dang chon
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200)  # Do trong suot cua mau sac
            s.fill(pg.Color("Orange"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  # Ve lop anh mau cam len odang co toa do chuot dang chon
            # To mau cho cac o duong di
            s.fill(pg.Color("Yellow"))  # doi mau tu cam sang vang
            for move in validMoves:
                if move.startRow == r and move.startCol == c:  # Neu dung la quan co minh dang chon
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))  # Ve lop anh mau vang len duong di cua no


# Ve ky hieu co len ban co
def drawChessNotation(screen):
    font = pg.font.Font("guiPNG/font.ttf", 18)
    drawChessColNotation(screen, font)
    drawChessRowNotation(screen, font)


# Ve ky hieu hang
def drawChessColNotation(screen, font):
    colRank = ["1", "2", "3", "4", "5", "6", "7", "8"]
    colors = [pg.Color('black'), pg.Color('white')]  # vi tri tuong ung 0, 1
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[ (r + c) % 2]  # tra ve hai so 0, 1 dua tren tong trung binh cua hang va cot va to mau tuong ung
            text = font.render(colRank[r], True, pg.Color(color))
            if c == 0:
                screen.blit(text, pg.Rect(0, 0, SQ_SIZE / 4, SQ_SIZE / 4).move(SQ_SIZE * c + 5, SQ_SIZE * r + 5))


# Ve ky hieu cot
def drawChessRowNotation(screen, font):
    rowRank = ["h", "g", "f", "e", "d", "c", "b", "a"]
    colors = [pg.Color('black'), pg.Color('white')]  # vi tri tuong ung 0, 1
    for c in range(DIMENSION):
        for r in range(DIMENSION):
            color = colors[
                (r + c) % 2]  # tra ve hai so 0, 1 dua tren tong trung binh cua hang va cot va to mau tuong ung
            text = font.render(rowRank[c], True, pg.Color(color))
            if r == 7:
                screen.blit(text, pg.Rect(0, 0, SQ_SIZE / 4, SQ_SIZE / 4).move(SQ_SIZE * c + 80, SQ_SIZE * r + 80))


# Ve avatar
def drawAvatar(screen, image):

    # Vẽ một hình chữ nhật có kích thước MOVE_LOG_PANEL_WIDTH, HEIGHT_BUTTON bắt đầu từ
    # vị trí x = WIDTH và y = 0 lên màn hình chinh
    moveLogRect = pg.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, HEIGHT_BUTTON) # Tạo một hình chữ nhật
    pg.draw.rect(screen, pg.Color("#666666"), moveLogRect) # Vẽ nó lên màn hình

    # Load ảnh từ thư mục vào biến avatar
    avatar = pg.image.load("guiPNG/avatarDemo.jpg")
    # Định dạng lại kích cỡ avatar
    avatar = pg.transform.scale(avatar, (64, 64))
    # Vẽ avatar lên hình chữ nhật vừa tạo phía trên và avatar đc vẽ tại vị trí
    # (avatar.get_width()/2-4, HEIGHT_BUTTON/2-avatar.get_height()/2)
    screen.blit(avatar, moveLogRect.move(avatar.get_width()/2-14, HEIGHT_BUTTON/2-avatar.get_height()/2))
    # Load font từ thư mục guiPNG vào biến font và đặt cỡ chữ là 12
    font = pygame.font.Font("guiPNG/font.ttf", 12)
    # Từ biến font tạo ra chuỗi ký tự text
    text_name = font.render("PLAYER NAME", True, pg.Color("Black"))
    text_level = font.render("LEVEL: EASY", True, pg.Color("Black"))
    # Tạo ra một lớp hình chữ nhật để hỗ trợ vẽ chữ
    # Toạ độ x: HEIGHT + avatar.get_width() + 30
    # Toạ độ y: 0
    # Chiều rộng: MOVE_LOG_PANEL_WIDTH - avatar.get_width()/2-54
    # Chiều cao: HEIGHT_BUTTON
    text_rect = pg.Rect(HEIGHT + avatar.get_width() + 30, 0,
                        (MOVE_LOG_PANEL_WIDTH - avatar.get_width()/2-54), HEIGHT_BUTTON)
    # Vẽ chữ lên lớp hình text_rect và dịch chuyển lớp hình vừa vẽ xuống trung tâm
    screen.blit(text_name, text_rect.move(0, HEIGHT_BUTTON/3))
    screen.blit(text_level, text_rect.move(0, HEIGHT_BUTTON/2 + 10))


def drawMoveLog(screen, gs):
    moveLogRect = pg.Rect(WIDTH, HEIGHT_BUTTON, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pg.draw.rect(screen, pg.Color("#EEEEEE"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2+1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "   "
        moveTexts.append(moveString)

    movesPerRow = 4
    padding = 5
    lineSpacing = 2
    textY = padding
    font = pg.font.SysFont("Arial", 20, False, False)
    for i in range(0, len(moveTexts), movesPerRow):
        text = " "
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, pg.Color('black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


# Vi tri dat ham nay co van  de nen k bat su kien code dc, neu muon bat thi rat phuc tap
def drawMoveButton(screen):

    moveLogRect = pg.Rect(WIDTH, MOVE_LOG_PANEL_HEIGHT + HEIGHT_BUTTON, MOVE_LOG_PANEL_WIDTH, HEIGHT_BUTTON) #400 x 100
    pg.draw.rect(screen, pg.Color("#666666"), moveLogRect)

    back = pg.image.load("guiPNG/skip-back.png")
    screen.blit(back, moveLogRect.move(back.get_width()/2-4, HEIGHT_BUTTON/2-back.get_height()/2))

    reset = pg.image.load("guiPNG/reset1.png")
    screen.blit(reset, moveLogRect.move((reset.get_width() + (reset.get_width()/2-8)*4+4), HEIGHT_BUTTON/2-reset.get_height()/2))

    home = pg.image.load("guiPNG/home.png")
    screen.blit(home, moveLogRect.move((home.get_width() + (home.get_width()/2-8)*10), HEIGHT_BUTTON/2-home.get_height()/2))

    # pg.display.update()
