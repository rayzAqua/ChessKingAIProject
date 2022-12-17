"""
Day la lop chiu trach nhiem chua cac thong tin hien tai cua ban co, dong thoi no cung co nhiem vu
xac dinh cac nuoc di hop le cua ban co hien tai. No cung vo vai tro giu lai mot nhat ky cac nuoc di chuyen.
"""

from Move import Move
class GameState():
    def __init__(self):
        # Ban co 8x8 la mot list 2 chieu, tung phan tu cua list co 2 ky tu
        # Ky tu dau tien the hien mau sac quan co: "b" hoac "w"
        # Ky tu thu hai the hien loai quan co: "K", "Q", "B", "N", "R"
        # Phan tu "--" dai dien cho mot o trong noi khong co quan co nao duoc dat len
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # Luot nguoi choi
        self.whiteToMove = True
        # Luu lai nuoc di cu~
        self.moveLog = []
        # Chieu tuong
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        # en passant
        self.enpassantPossible = ()
        # Danh sach Log luon duoc khoi tao boi gia tri goc vi khi undo se day het toan bo gia tri da tao ra truoc do trong list.
        # The nen neu khong co gia tri khoi tao san trong list Log thi khi undo ve nuoc di dau tien he thong se khong hieu la
        # can phai gan gia tri gi cho list goc' dan toi loi chuong trinh
        self.enpassantPossibleLog = [self.enpassantPossible]
        # castling
        self.currentCastlingRights = CastlingRights(True, True, True, True)
        # Khoi dau game ta co the nhap thanh tu 4 phia', neu sai dieu kien nhap thanh thi dat True thanh False
        self.castleRightsLog = [CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                               self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]

    # Thuc hien mot nuoc di dua tren thong tin cua class Move
    def makeMove(self, move, isBotPromote=False, pieceName=""):
        # Normal Move
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # Doi luot tu quan trang thang quan den

        # Neu quan vua di chuyen thi cap nhat lai vi tri
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            if isBotPromote:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
            else:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + pieceName

        # En passsant
        # Neu con tot di 2 nuoc thi luot tiep theo co the thuc hien en passant - luu vi tri duoc phep di vao list enpassant
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:  # Khi khong phai la nuoc doi cua con tot thi reset, nuoc doi cuac on tot ca game chi thuc hien dc 1 lan
            self.enpassantPossible = ()

        if move.isEnpassant:  # Bat con tot quan dich
            self.board[move.startRow][move.endCol] = "--"
        # Luu lai nuoc di enpassant
        self.enpassantPossibleLog.append(self.enpassantPossible)

        # Castling
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Nhap thanh canh vua
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][
                    move.endCol + 1]  # Copy con xe vao o ben trai vua
                self.board[move.endRow][move.endCol + 1] = "--"  # Xoa con xe cu~
            else:  # Nhap thanh canh hau
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                    move.endCol - 2]  # Copy con xe vao o ben phai vua
                self.board[move.endRow][move.endCol - 2] = "--"  # Xoa con xe cu~

        # luu lai quyen nhap thanh - chi ap dung doi voi con vua va con xe
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                                   self.currentCastlingRights.bks, self.currentCastlingRights.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # Cap nhat lai vi tri cua vua khi undo
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo sau khi thuc hien en passant
            if move.isEnpassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            # Sau khi undo thi day gia tri cuoi cung trong list ra ngoai (xoa no di)
            # sau khi day gia tri cuoi cu~ ra khoi list thi gan gia tri cuoi moi' cua list vao danh sach goc'
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # undo sau khi thuc hien castling
            self.castleRightsLog.pop()  # Loai bo gia tri cuoi trong ds Log nhap thanh
            castleRights = self.castleRightsLog[
                -1]  # Cap nhat lai gia tri currentCastlingRights = gia tri cuoi cua Log castle
            self.currentCastlingRights = CastlingRights(castleRights.wks, castleRights.wqs, castleRights.bks,
                                                        castleRights.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # Nhap thanh canh vua
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                        move.endCol - 1]  # Copy con xe vao o ben trai vua
                    self.board[move.endRow][move.endCol - 1] = "--"  # Xoa con xe cu~
                else:  # Nhap thanh canh hau
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][
                        move.endCol + 1]  # Copy con xe vao o ben phai vua
                    self.board[move.endRow][move.endCol + 1] = "--"  # Xoa con xe cu~

        self.checkMate = False
        self.staleMate = False

    # Cap nhat gia tri cac thuoc tinh cua class CastlingRights
    def updateCastleRights(self, move):
        # Dieu kien 1: Nhap thanh chi thuc hien duoc khi con vua va con xe chua tung di chuyen hoac con xe chua bi bat
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        # Quan xe di chuyen
        elif move.pieceMoved == "wR":
            if move.startRow == 7:  # Quan trang
                if move.startCol == 0:  # Quan xe ben trai
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:  # Quan xe ben phai
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:  # Quan den
                if move.startCol == 0:  # Quan xe ben trai
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:  # Quan xe ben phai
                    self.currentCastlingRights.bks = False
        # Neu quan xe bi bat'
        elif move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False

    # Di len hoac di qua trai thi tru`, di xuong hoac qua phai thi cong
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # Luot di cua quan mau trang
            if self.board[r - 1][c] == "--":  # Quan tot di mot o vuong
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # Quan tot di hai o vuong khi va chi khi no o vi tri ban dau
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # Bat quan dich ben trai
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassant=True))
            if c + 1 <= 7:  # Bat quan dich ben phai
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassant=True))

        else:  # Luot di cua quan mau den
            if self.board[r + 1][c] == "--":  # Quan tot di mot o vuong
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # Quan tot di hai o vuong khi va chi khi no o vi tri ban dau
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # Bat quan dich ben trai
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassant=True))
            if c + 1 <= 7:  # Bat quan dich ben phai
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassant=True))

    # Lay toan bo gia tri row va column cua ban co o moi huong di cua quan xe
    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Huong di cua con xe (r, c)
        #               len      trai    xuong    phai (lay quan trang lam chuan)
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:  # Lay het toan bo huong di tinh ra tung toa do co the co cua huong di va them vo list moves
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Kiem tra neu la o vuong trong thi duoc di
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Kiem tra neu la o vuong co quan co ke thu` thi duoc di
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Neu la o vuong co quan co cung phe thi khong tinh theo huong di hien tai nua
                        break
                else:  # Vuot qua pham vi ban co
                    break

    # Lay toan bo gia tri row va column o moi huong di cua quan ma~ va them vao moves
    def getKnightMoves(self, r, c, moves):
        knightDirections = [(-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2)]
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"
        for kd in knightDirections:
            endRow = r + kd[0]
            endCol = c + kd[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Cach dung break chi ap dung cho 2 vong lap for
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Lay toan bo gia tri row va column cua quan tuong va them vao list moves
    def getBishopMoves(self, r, c, moves):
        bishopDirections = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for bd in bishopDirections:
            for i in range(1, 8):
                endRow = r + bd[0] * i
                endCol = c + bd[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    # Lay toan bo gia tri row, column cua quan vua va them vao list moves
    def getKingMoves(self, r, c, moves):
        kingDirections = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"
        for i in range(8):
            endRow = r + kingDirections[i][0]
            endCol = c + kingDirections[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Cach dung break chi ap dung cho 2 vong lap for
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Lay toan bo nuoc di nhap thanh hop le va them vao list moves
    def getCastleMoves(self, r, c, moves):
        # Dieu kien thu 2: Vua khong bi chieu
        if self.inCheck():
            return  # Neu bi chieu thi khong tien hanh buoc ghi nuoc di hop le
        if (self.whiteToMove and self.currentCastlingRights.wks) or (
                not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMove(r, c, moves)  # Nhap thanh canh vua
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (
                not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMove(r, c, moves)  # Nhap thanh canh hau

    # Lay nuoc di nhap thanh hop le canh' vua va them vao list moves
    def getKingSideCastleMove(self, r, c, moves):
        # Dieu kien thu ba: Dam bao rang hai o ben canh vua la o trong'
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            # Dieu kien thu tu: Dam bao rang cac o ben canh vua khong nam trong su kiem soat cua bat ky quan dich nao
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    # Lay nuoc di nhap thanh hop le canh' hau va them vao list moves
    def getQueenSideCastleMove(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    # Lay toan bo gia tri row va column cau quan hau va theam vao list moves
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getAllPossibleMove(self):
        moves = []
        for r in range(len(self.board)):  # So luong hang
            for c in range(len(self.board[r])):  # So luong cot
                color = self.board[r][c][0]  # Lay ra chu cai dau tien cua phan tu thu r, c trong list
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]  # Lay chu cai thu hai cua phan tu thu r, c trong list
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    # Kiem tra xem vua co bi chieu hay khong, return true false neu bi chieu hoac khong bi chieu
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Kiem tra xem mot o vuong co nam duoi su tan cong cua quan dich khong, neu co tra ve True, khong tra ve False
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # Doi sang luot cua quan dich
        oppMoves = self.getAllPossibleMove()
        self.whiteToMove = not self.whiteToMove  # Doi lai luot cua minh
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # Neu toa do ma doi thu di chinh la toa do o vuong can xet thi tra ve True
                return True
        return False

    def getValidMove(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                          self.currentCastlingRights.bks, self.currentCastlingRights.bqs)

        # 1. Lay toan bo nuoc di co the cua phe minh
        moves = self.getAllPossibleMove()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # 2. Voi moi nuoc di trong buoc 1, thuc hien mot nuoc di co trong list tren ban co
        for i in range(len(moves) - 1, -1, -1):  # Duyet tu nuoc tu cuoi mang de khong bo sot phan tu nao
            self.makeMove(moves[i])
            # 3. Tao ra toan bo nuoc di co the cua doi thu
            # 4. Voi moi nuoc di cua doi thu, kiem tra xem co nuoc di nao tan cong vua cua minh khong
            self.whiteToMove = not self.whiteToMove  # Chuyen lai luot cua minh
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove  # Chuyen lai thanh luot cua doi thu
            self.undoMove()  # undoMove de nuoc di do quay ve vi tri ban dau

        if len(moves) == 0:  # Quan vua bi chieu hoan toan khong co duong thoat nen khong co duong di nao duoc tao ra
            if self.inCheck():  # Neu vua khong con duong thoat ,a the co` hien tai da chieu vua thi chieu tuong
                self.checkMate = True
            else:  # Neu vua khong con duong thoat ma the co hien tai chua chieu vua thi vao` the bi
                self.staleMate = True

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastleRights
        # 5. Tra ve danh sach cac nuoc di hop le
        return moves


# Kiem tra nhap thanh`
class CastlingRights():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks  # Nhap thanh canh vua trang' - White King Side
        self.wqs = wqs  # Nhap thanh canh hau trang' - White Queen Side
        self.bks = bks  # Nhap thanh canh vua den - Black King Sides
        self.bqs = bqs  # Nhap thanh canh hau den - Black Queen Side
