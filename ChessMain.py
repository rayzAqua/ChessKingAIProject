"""
Day la File dieu khien chinh cua chuong trinh, no chiu trach nhiem cho viec dieu khien du lieu vao cua
nguoi dung và hien thi trang thai tro choi
"""

import pygame as pg
import sys
from config import *
import ChessEngine
import Board
import ChessBot as AI

class Main():
    def __init__(self, player1, player2):
        pg.init()
        pg.display.set_caption('Chess King')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(pg.Color('white'))
        self.gs = ChessEngine.GameState()  # Trang thai ban co
        self.clock = pg.time.Clock()
        self.board = Board.Board()
        self.player1 = player1
        self.player2 = player2

    '''
    Phan main cua chuong trinh, no co nhiem vu xu li input cua nguoi dung va cap nhat lai hinh anh
    '''
    def mainloop(self):
        # Lay nuoc di hop le - lay mot lan truoc khi vao vong lap
        validMoves = self.gs.getValidMove()
        moveMake = False  # Neu tao nuoc di roi thi False

        # Lay toa do con tro chuot
        sqSelected = ()  # Giu lai vi tri cua o vuong dc chon - chi chua 1 toa do
        playerClick = []  # Giu lai vi tri hai o vuong ma nguoi choi chon de di nuoc co. VD: [(0, 7), (3, 1)] - chua 2 toa do

        # Luot nguoi choi la may hay la nguo
        player1 = self.player1 # True = Human, False = AI
        player2 = self.player2 #False = AI, True = Human

        # Vong lap game
        running = True
        gameOver = False
        while running:
            humanTurn = (self.gs.whiteToMove and player1) or (not self.gs.whiteToMove and player2) # Luot cua nguoi choi di truoc hoac di sau phu thuoc vao player
            for e in pg.event.get():  # Bat su kien
                if e.type == pg.QUIT:
                    sys.exit()
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if not gameOver and humanTurn:
                        location = pg.mouse.get_pos()  # toa do x, y cua chuot
                        col = location[0] // SQ_SIZE  # Vi tri cua o vuong vua chon
                        row = location[1] // SQ_SIZE
                        if sqSelected == (row, col) or row >= 8 or col >= 8:  # Kiem tra xem co phai player bam 2 lan cung 1 o giong nhau ko
                            sqSelected = ()  # Reset
                            playerClick = []  # Reset]
                        else:
                            sqSelected = (row, col)
                            playerClick.append(sqSelected)  # Luu lai 2 toa do 2 o vuong da click
                        if len(playerClick) == 2:
                            move = ChessEngine.Move(playerClick[0], playerClick[1], self.gs.board)
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
                                    if self.gs.isPawnPromote:
                                        pieceName = input('Phong tuoc thanh gi: R, N, B or Q: ')
                                        if pieceName == "Q":
                                            self.gs.makeMove(validMoves[i], isQueen=True)
                                        elif pieceName == "B":
                                            self.gs.makeMove(validMoves[i], isBishop=True)
                                        elif pieceName == "N":
                                            self.gs.makeMove(validMoves[i], isKnight=True)
                                        elif pieceName == "R":
                                            self.gs.makeMove(validMoves[i], isRook=True)
                                    else:
                                        self.gs.makeMove(validMoves[i])
                                    moveMake = True
                                    sqSelected = ()  # Reset
                                    playerClick = []  # Reset
                            if not moveMake:
                                playerClick = [sqSelected]

                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        self.gs.undoMove()
                        moveMake = True
                        gameOver = False
                    elif e.key == pg.K_r:
                        self.gs = ChessEngine.GameState()
                        validMoves = self.gs.getValidMove()
                        moveMake = False
                        sqSelected = ()
                        playerClick = []
                    elif e.key == pg.K_ESCAPE:
                        running = False

            # AI MOVE FINDER
            if not gameOver and not humanTurn:
                AIMove = AI.findRandomMoves(validMoves)
                self.gs.makeMove(AIMove)
                moveMake = True

            if moveMake:
                validMoves = self.gs.getValidMove()
                moveMake = False

            self.board.drawGameState(self.screen, self.gs, validMoves, sqSelected)

            if self.gs.checkMate:
                gameOver = True
                if self.gs.whiteToMove:
                    self.board.drawText(self.screen, 'QUAN DEN THANG BOI CHIEU TUONG', "Gray", "Black")
                else:
                    self.board.drawText(self.screen, 'QUAN TRANG THANG BOI CHIEU TUONG', "Black", "White")
            elif self.gs.staleMate:
                gameOver = True
                self.board.drawText(self.screen, 'Chieu bi', "Black", "Red")

            self.clock.tick(MAX_FPS)  # 1 giay co max_fps khung hinh
            pg.display.flip()

'''
Chay chuong trinh
'''
# main = Main()
# main.mainloop()
