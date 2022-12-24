"""
Day la File dieu khien chinh cua chuong trinh, no chiu trach nhiem cho viec dieu khien du lieu vao cua
nguoi dung và hien thi trang thai tro choi
"""

import pygame as pg
import sys
from multiprocessing import Process, Queue

import Button
import FormPawnPromote
from config import *
import ChessEngine
import Board
import ChessBot as AI
import FormSignIn

'''
Phan main cua chuong trinh, no co nhiem vu xu li input cua nguoi dung va cap nhat lai hinh anh
'''
def main(player_one, player_two):
    pg.init()
    pg.display.set_icon(pg.image.load("guiPNG/chessIcon.png"))
    pg.display.set_caption("Chess King")
    screen = pg.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    screen.fill(pg.Color("White"))
    gs = ChessEngine.GameState()  # Trang thai ban co
    clock = pg.time.Clock()
    Board.loadImage()

    moveLogFont = pg.font.SysFont("Arial", 12, False, False)
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
                        playerClick = []  # Reset]
                    else:
                        sqSelected = (row, col)
                        playerClick.append(sqSelected)  # Luu lai 2 toa do 2 o vuong da click
                    if len(playerClick) == 2 and humanTurn:
                        move = ChessEngine.Move(playerClick[0], playerClick[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                if move.isPawnPromotion:
                                    pieceName = FormPawnPromote.drawPawnPromote(screen, move.endCol, move.endRow, gs.whiteToMove)
                                    if pieceName != "":
                                        gs.makeMove(validMoves[i], pieceName=pieceName)
                                else:
                                    # print("Player: " + move.getChessNotation())
                                    gs.makeMove(validMoves[i])
                                moveMake = True
                                moveUndo = False
                                sqSelected = ()  # Reset
                                playerClick = []  # Reset
                        if not moveMake:
                            # Bat loi khi nguoi choi da chon 1 con co va sau do con 1 con co khac
                            # khi ng choi lam hanh dong nay thi toa do con list playerClick se la lam chon cuoi cung
                            playerClick = [sqSelected]
                    # Bat su kien cac nut khi dung chuot
                    if location[0]//WIDTH_BUTTON in range(6, 9) and location[1]//HEIGHT_BUTTON == 7:
                        col_btn = location[0]//WIDTH_BUTTON
                        row_btn = location[1]//HEIGHT_BUTTON
                        if (row_btn, col_btn) == (7, 6):
                            gs.undoMove()
                            moveMake = True
                            gameOver = False
                            if aiThingking:
                                moveFinderProcess.terminate()
                                aiThingking = False
                            moveUndo = True
                        elif (row_btn, col_btn) == (7, 7):
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
                            if aiThingking:
                                moveFinderProcess.terminate()
                            running = False
            # Bat su kien cac nut khi dung ban phim
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMake = True
                    gameOver = False
                    if aiThingking:
                        moveFinderProcess.terminate()
                        aiThingking = False
                    moveUndo = True
                elif e.key == pg.K_r:
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
                moveFinderProcess = Process(target=AI.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start() # Goi ham findBestMove(gs, validMoves, returnQueue)

            if not moveFinderProcess.is_alive():
                # Neu process con xu ly thi Ai khong duoc thuc hien nuoc di
                # moveFinderProcess.is_alive() = False -> not -> True: AI duoc thuc hien nuoc di
                print("AI Done Thingking !")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = AI.findRandomMoves(validMoves)
                gs.makeMove(AIMove, isBotPromote=True)
                # print("AI:" + AIMove.getChessNotation())
                moveMake = True
                aiThingking = False

        if moveMake:
            validMoves = gs.getValidMove()
            moveMake = False
            moveUndo = False

        Board.drawGameState(screen, gs, validMoves, sqSelected)
        Board.drawMoveButton(screen)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                case = Board.drawText(screen, "Black Win", "Gray", "Black", gameOver)
                # FormSignIn.updateLevel()
                # return 1
            else:
                case = Board.drawText(screen, "White Win", "Gray", "White", gameOver)
                # FormSignIn.updateLevel()
                # return 2
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

        clock.tick(MAX_FPS)  # 1 giay co max_fps khung hinh
        pg.display.flip()

# def Level():
#     temp, level = FormSignIn.showInformation()
#     if level < 3:
#         if main(True, False) == 1:
#             level += 1
#         elif main(True, False) == 2:
#             level -= 1
#         elif main(False, True) == 1:
#             level -= 1
#         elif main(False, True) == 2:
#             level += 1
#     else:
#         if main(True, False) == 1:
#             pass
#         elif main(True, False) == 2:
#             level -= 1
#         elif main(False, True) == 1:
#             level -= 1
#         elif main(False, True) == 2:
#             pass
#     return level