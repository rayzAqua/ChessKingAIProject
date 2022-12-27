"""
Day la File dieu khien chinh cua chuong trinh, no chiu trach nhiem cho viec dieu khien du lieu vao cua
nguoi dung và hien thi trang thai tro choi
"""
import time

import pygame as pg
import sys
from multiprocessing import Process, Queue

import FormPawnPromote
from config import *
import ChessEngine
import Board
import ChessBot as AI
import FormSignIn

'''
Phan main cua chuong trinh, no co nhiem vu xu li input cua nguoi dung va cap nhat lai hinh anh
'''


def main(player_one, player_two, level, isTwoMode):
    pg.init()
    pg.display.set_icon(pg.image.load("guiPNG/chessIcon.png"))
    pg.display.set_caption("Chess King")
    screen = pg.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    screen.fill(pg.Color("White"))
    gs = ChessEngine.GameState()  # Trang thai ban co
    clock = pg.time.Clock()
    Board.loadImage()

    # Sound effect
    MOVE_SFX = pg.mixer.Sound("music/move_effect.mp3")
    CAPTURED_SFX = pg.mixer.Sound("music/captured_effect.mp3")
    CHECK_SFX = pg.mixer.Sound("music/check_effect.mp3")
    BUTTON_SFX = pg.mixer.Sound("music/button_effect.mp3")

    # Lay nuoc di hop le - lay mot lan truoc khi vao vong lap
    validMoves = gs.getValidMove()
    moveMake = False  # Neu tao nuoc di roi thi False

    # Lay toa do con tro chuot
    sqSelected = ()  # Giu lai vi tri cua o vuong dc chon - chi chua 1 toa do
    playerClick = []  # Giu lai vi tri hai o vuong ma nguoi choi chon de di nuoc co. VD: [(0, 7), (3, 1)] - chua 2 toa do

    # Luot nguoi choi la may hay la nguoi
    player1 = player_one
    player2 = player_two  # False = AI, True = Human

    aiThingking = False
    moveFinderProcess = None
    moveUndo = False

    # So lan ve canh bao chieu tuong
    draw_times = 3
    count_draw_times = 0

    # Vong lap game
    running = True
    gameOver = False
    while running:
        # Luot cua nguoi choi di truoc hoac di sau phu thuoc vao player
        humanTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2)
        for e in pg.event.get():  # Bat su kien
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pg.mouse.get_pos()  # toa do x, y cua chuot
                    col = location[0] // SQ_SIZE  # Vi tri cua o vuong vua chon
                    row = location[1] // SQ_SIZE
                    # Kiem tra xem co phai player bam 2 lan cung 1 o giong nhau ko
                    if sqSelected == (row, col) or row >= 8 or col >= 8:
                        sqSelected = ()  # Reset
                        playerClick = []  # Reset
                    else:
                        sqSelected = (row, col)
                        playerClick.append(sqSelected)  # Luu lai 2 toa do 2 o vuong da click
                    if len(playerClick) == 2 and humanTurn:
                        move = ChessEngine.Move(playerClick[0], playerClick[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                # Kiem tra phong ham
                                if validMoves[i].isPawnPromotion:
                                    pieceName = FormPawnPromote.drawPawnPromote(screen, move.endCol, move.endRow, gs.whiteToMove)
                                    if pieceName != "":
                                        gs.makeMove(validMoves[i], pieceName=pieceName)
                                        MOVE_SFX.play()
                                # Neu khong la phong ham
                                else:
                                    # print("Player: " + move.getChessNotation())
                                    gs.makeMove(validMoves[i])
                                    if validMoves[i].isCapture or validMoves[i].isEnpassant:
                                        CAPTURED_SFX.play()
                                    else:
                                        MOVE_SFX.play()
                                moveMake = True
                                moveUndo = False
                                sqSelected = ()  # Reset
                                playerClick = []  # Reset
                        if not moveMake:
                            # Bat loi khi nguoi choi da chon 1 con co va sau do con 1 con co khac
                            # khi ng choi lam hanh dong nay thi toa do con list playerClick se la lam chon cuoi cung
                            playerClick = [sqSelected]
                    if not humanTurn:
                        playerClick = []
                    # Bat su kien cac nut khi dung chuot
                    if location[0] // WIDTH_BUTTON in range(6, 9) and location[1] // HEIGHT_BUTTON == 7:
                        col_btn = location[0] // WIDTH_BUTTON
                        row_btn = location[1] // HEIGHT_BUTTON
                        BUTTON_SFX.play()
                        if (row_btn, col_btn) == (7, 6):
                            time.sleep(0.3)
                            gs.undoMove()
                            moveMake = True
                            gameOver = False
                            if aiThingking:
                                moveFinderProcess.terminate()
                                aiThingking = False
                            moveUndo = True

                        elif (row_btn, col_btn) == (7, 7):
                            time.sleep(0.3)
                            gs = ChessEngine.GameState()
                            validMoves = gs.getValidMove()
                            moveMake = False
                            sqSelected = ()
                            playerClick = []
                            gameOver = False
                            moveUndo = False
                            if aiThingking:
                                moveFinderProcess.terminate()
                                aiThingking = False
                                moveMake = True
                                moveFinderProcess = None

                        elif (row_btn, col_btn) == (7, 8):
                            time.sleep(0.3)
                            if aiThingking:
                                moveFinderProcess.terminate()
                            running = False

            # Bat su kien cac nut khi dung ban phim
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    BUTTON_SFX.play()
                    time.sleep(0.3)
                    gs.undoMove()
                    moveMake = True
                    gameOver = False
                    if aiThingking:
                        moveFinderProcess.terminate()
                        aiThingking = False
                    moveUndo = True
                elif e.key == pg.K_r:
                    BUTTON_SFX.play()
                    time.sleep(0.3)
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMove()
                    moveMake = False
                    sqSelected = ()
                    playerClick = []
                    gameOver = False
                    moveUndo = False
                    if aiThingking:
                        moveFinderProcess.terminate()
                        aiThingking = False
                        moveMake = True
                        moveFinderProcess = None
                elif e.key == pg.K_ESCAPE:
                    BUTTON_SFX.play()
                    time.sleep(0.3)
                    if aiThingking:
                        moveFinderProcess.terminate()
                    running = False

        # AI MOVE FINDER
        if not gameOver and not humanTurn and not moveUndo:
            if not aiThingking:
                aiThingking = True
                print("AI Thingking ...")
                # Truyen du lieu giua cac luong de tranh viec xu ly tren cung 1 luong se lam chuong trinh
                # gap loi not responding
                returnQueue = Queue()
                # Khi Process bat dau thi goi ham tim nuoc di cua AI dau tien va xu ly, sau do dua vao returnQueue
                moveFinderProcess = Process(target=AI.findBestMove, args=(gs, validMoves, returnQueue, level))
                moveFinderProcess.start()  # Goi ham findBestMove(gs, validMoves, returnQueue)

            if not moveFinderProcess.is_alive():
                # Neu process con xu ly thi Ai khong duoc thuc hien nuoc di
                # moveFinderProcess.is_alive() = False -> not -> True: AI duoc thuc hien nuoc di
                print("AI Done Thingking !")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = AI.findRandomMoves(validMoves)
                if AIMove.isPawnPromotion:
                    gs.makeMove(AIMove, pieceName="Q")
                else:
                    gs.makeMove(AIMove)
                # SOUND EFFECT
                if AIMove.isCapture or AIMove.isEnpassant:
                    CAPTURED_SFX.play()
                else:
                    MOVE_SFX.play()
                # print("AI:" + AIMove.getChessNotation())
                moveMake = True
                aiThingking = False

        if moveMake:
            validMoves = gs.getValidMove()
            moveMake = False
            moveUndo = False

        Board.drawGameState(screen, gs, validMoves, sqSelected)
        Board.drawMoveButton(screen)
        # Ve canh bao chieu tuong
        if gs.inCheck():
            # Chi cho nhap nhay surface canh bao 1 lan duy nhat
            # Neu so lan ve la lan thu 0 thi dung lai ko ve nua va dat gia tri cua draw_times = 0 de luon ve surface
            # canh bao theo lan thu 0 (lan cuoi cung)
            # Neu so lan ve khong phai lan cuoi cung thi tiep tuc ve~
            # Chi khi nao chua xuat hien hieu ung nhap nhay thi moi phat am thanh
            if count_draw_times == 0 and draw_times == 3:
                CHECK_SFX.play()
            if draw_times < count_draw_times:
                draw_times = 0
            else:
                draw_times -= 1
            # Ve hieu ung nhap nhay khi bi chieu tuong - khi la lan cuoi thi dung lai khong ve nua
            # Dung lai khong ve nua bang cach: Tang gia tri cua bien dem so lan ve canh bao thanh 1
            # Nghia la: Chi duoc ve hieu ung nhap nhay khi chieu tuong 1 lan duy nhat
            if draw_times == 2:
                Board.drawCheckWarning(screen, gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation, alpha=150)
                time.sleep(0.22)
            elif draw_times == 1:
                Board.drawCheckWarning(screen, gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation, alpha=0)
                time.sleep(0.22)
            elif draw_times == 0:
                Board.drawCheckWarning(screen, gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation, alpha=150)
                if count_draw_times == 0:
                    count_draw_times += 1

        # Neu khong la chieu tuong thi dua gia tri dem so lan ve canh bao va so lan ve canh bao ve gia tri goc
        else:
            count_draw_times = 0
            draw_times = 3

        global isWin
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                case = Board.drawText(screen, "Black Win", "Gray", "Black", gameOver)
                isWin = 1
                if not isTwoMode:
                    FormSignIn.updateLevel()
            else:
                case = Board.drawText(screen, "White Win", "Gray", "White", gameOver)
                isWin = 2
                if not isTwoMode:
                    FormSignIn.updateLevel()
                    print("Done")

            if case == "undo":
                gs.undoMove()
                moveMake = True
                gameOver = False

            elif case == "reset":
                gs = ChessEngine.GameState()
                validMoves = gs.getValidMove()
                moveMake = False
                sqSelected = ()
                playerClick = []
                gameOver = False
                moveUndo = False

            elif case == "back":
                gameOver = False
                running = False

            elif case == "update":
                # Update level sau khi xong game
                # Neu khong la che do 2 nguoi thi update
                if not isTwoMode:
                    level = FormSignIn.showLevel()
                    level = ''.join(str(i) for i in level)
                    level = int(level)
                    print(level)

                gs = ChessEngine.GameState()
                validMoves = gs.getValidMove()
                moveMake = False
                sqSelected = ()
                playerClick = []
                gameOver = False
                moveUndo = False

        elif gs.staleMate:
            gameOver = True
            if gs.whiteToMove:
                case = Board.drawText(screen, "Stalemate", "Black", "Red", gameOver)

            else:
                case = Board.drawText(screen, "Stalemate", "Black", "Red", gameOver)

            if case == "undo":
                gs.undoMove()
                moveMake = True
                gameOver = False

            elif case == "reset":
                gs = ChessEngine.GameState()
                validMoves = gs.getValidMove()
                moveMake = False
                sqSelected = ()
                playerClick = []
                gameOver = False
                moveUndo = False

            elif case == "back":
                gameOver = False
                running = False

            elif case == "update":
                gs = ChessEngine.GameState()
                validMoves = gs.getValidMove()
                moveMake = False
                sqSelected = ()
                playerClick = []
                gameOver = False
                moveUndo = False

        clock.tick(MAX_FPS)  # 1 giay co max_fps khung hinh
        pg.display.flip()


# isWin = 1 => black win
# isWin = 2 => white win
def Level():
    temp, level = FormSignIn.showInformation()
    if 0 <= level < 3:
        if isWin == 1:
            if level != 1:
                level -= 1
        elif isWin == 2:
            level += 1
    elif level == 3:
        if isWin == 1:
            level -= 1
        elif isWin == 2:
            pass
    return level
