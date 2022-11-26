"""
Day la file dieu khien chinh cua chuong trinh, no chiu trach nhiem cho viec dieu khien du lieu vao cua
nguoi dung và hien thi trang thai tro choi
"""

import pygame as pg
from ChessPackage import ChessEngine, ThisIsOurAI

WIDTH = HEIGHT = 812  # Kich thuoc ban co la 512x512
DIMENSION = 8  # Khong gian ban co la 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # Toc do khung hinh
IMAGES = {}

def drawChessNotation():
    pass

#Ve chu
def drawText(screen, text, color1, color2):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pg.Color(color1))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color(color2))
    screen.blit(textObject, textLocation.move(2, 2))

# Load hinh anh vao mot list
def loadImage():  # Load tung anh
    pieces = ["bR", "bN", "bB", "bK", "bQ", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))


# Ve ban co va cac o vuong
def drawBoard(screen):
    colors = [pg.Color('white'), pg.Color('gray')]  # vi tri tuong ung 0, 1
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]  # tra ve hai so 0, 1 dua tren tong trung binh cua hang va cot va to mau tuong ung
            pg.draw.rect(screen, color, pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Rect(toa do x, toa do y, cd, cr)


# Ve quan co len ban co
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Ve duong di quan co
def drawHighLight(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == 'w' or gs.board[r][c][0] == 'b':
            # To mau cho o dang chon
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Do trong suot cua mau sac
            s.fill(pg.Color("Orange"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # To mau cho cac o duong di
            s. fill(pg.Color("Yellow")) # doi mau tu cam sang vang
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


# Ve mot ban co hoan chinh
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # Ve ra mot ban co voi kich thuoc WIDTH, HEIGHT
    drawPieces(screen, gs.board)  # Ve ra quan co tren ban co dua vao gamestate.board hien tai
    drawHighLight(screen, gs, validMoves, sqSelected) # Ve highlight cho lua chon


'''
Phan main cua chuong trinh, no co nhiem vu xu li input cua nguoi dung va cap nhat lai hinh anh
'''


def main():
    pg.init()
    pg.display.set_caption('Chess King')
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
 
    gs = ChessEngine.GameState()  # Trang thai ban co
    loadImage()  # Chi load 1 lan duy nhat, load truoc khi vao vong lap

    # Get the validMoves
    validMoves = gs.getValidMove()
    moveMake = False  # Kiem tra xem co nuoc di nao duoc tao ra chua

    #Get the mouse positions
    sqSelected = ()  # Giu lai vi tri cua o vuong cuoi cung dc chon
    playerClick = []  # Giu lai vi tri hai o vuong ma nguoi choi chon de di nuoc co. VD: [(0, 7), (3, 1)]

    player1 = True # True = Human, False = AI
    player2 = True #False = AI, True = Human

    running = True
    gameOver = False
    while running:
        humanTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2) # Luot cua nguoi choi di truoc hoac di sau phu thuoc vao player
        for e in pg.event.get():  # Bat su kien
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = pg.mouse.get_pos()  # toa do x, y cua chuot
                    col = location[0] // SQ_SIZE  # Vi tri cua o vuong vua chon
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):  # Kiem tra xem co phai player bam 2 lan cung 1 o giong nhau ko
                        sqSelected = ()  # Reset
                        playerClick = []  # Reset]
                    else:
                        sqSelected = (row, col)
                        playerClick.append(sqSelected)  # Luu lai 2 toa do 2 o vuong da click
                    if len(playerClick) == 2:
                        move = ChessEngine.Move(playerClick[0], playerClick[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(move.getChessNotation(move))
                                # Vi nguoi choi thuc hien nuoc di enpassant hay castling thi may' se khong hieu
                                # cho nen ta co y tuong la thuc hien nuoc di trong validMoves chu khong thuc hien
                                # nuoc di move do nguoi choi tao ra.
                                # Muc tieu cua dieu nay la de khac phuc viec may' khong phan biet duoc luc nao la true, false
                                # cua nuoc di enpassant, castling.
                                # Neu la nuoc di cua nguoi choi tao ra thi se luon luon la isEnpassant = False
                                # Neu la nuoc di trong validMoves thi neu la en passant thi thi en passant luon luon la True
                                gs.makeMove(validMoves[i])
                                moveMake = True
                                sqSelected = ()  # Reset
                                playerClick = []  # Reset
                        if not moveMake:
                            playerClick = [sqSelected]

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMake = True
                elif e.key == pg.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMove()
                    moveMake = False
                    sqSelected = ()
                    playerClick = []

        # AI MOVE FINDER
        if not gameOver and not humanTurn:
            AIMove = ThisIsOurAI.findRandomMoves(validMoves)
            gs.makeMove(AIMove)
            moveMake = True

        if moveMake:
            validMoves = gs.getValidMove()
            moveMake = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'QUAN DEN THANG', "Gray", "Black")
            else:
                drawText(screen, 'QUAN TRANG THANG', "Black", "White")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Chieu bi', "Black", "Red")

        clock.tick(MAX_FPS)  # 1 giay co max_fps khung hinh
        pg.display.flip()


if __name__ == '__main__':
    main()
