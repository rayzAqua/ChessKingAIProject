'''
Mot class co vai tro cuc ky quan trong, class nay tao ra cac nuoc di dua tren thong tin toa do con tro chuot dang chon
'''

from config import *

class Move():
    # Chuyen cac vi tri trong List board thanh cac ky hieu tuong ung tren ban co vua
    # Vi tri phan tu hang tu 0 - 7 doi thanh 1 - 7
    # Vi tri phan tu cot, tu 0 - 7 doi thanh a - h

    # ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
    #                "5": 3, "6": 2, "7": 1, "8": 0}
    # rowsToRanks = {v: k for k, v in ranksToRows.items()}
    # filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
    #                "e": 4, "f": 5, "g": 6, "h": 7}
    # colsToFiles = {v: k for k, v in filesToCols.items()}
    ranksToRows = {"1": 0, "2": 1, "3": 2, "4": 3,
                   "5": 4, "6": 5, "7": 6, "8": 7}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 7, "b": 6, "c": 5, "d": 4,
                   "e": 3, "f": 2, "g": 1, "h": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassant=False, isCastleMove=False):
        # Create a move and MoveID for check move in getvalidMoves
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # Luu lai toa do ban dau cua quan co
        self.pieceCaptured = board[self.endRow][self.endCol]  # Luu lai toa do ban dau cua o vuong dc chon thu 2
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # Pawn Promote
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        # En passant
        self.isEnpassant = isEnpassant
        if self.isEnpassant:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
        # Castling
        self.isCastleMove = isCastleMove
        # Captured
        self.isCapture = self.pieceCaptured != "--"

    # Vi class Move khong hieu duoc hai gia tri class giong het nhau la bang nhau nen can ham nay de kiem tra xem class co bang nhau khong
    # moves = [Move((6, 4), (4, 4), self.board)]: Day la danh sach chua cac nuoc di hop le
    #  def __init__(self, startSq, endSq, board): con day la nuoc di cua nguoi choi tao thanh
    # vi du: trong list moves co nuoc di la 6,4 va 4,4
    # nguoi choi di nuoc 4,4
    # luc nay class Move co toi 2 gia tri giong het nhau
    # class khong hieu duoc hai gia tri nay bang nhau hay khac nhau nen phai thong qua ham __ed__ de kiem tra xem gia tri class
    # co bang nhau khong
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def getChessNotation(self):  # self, move
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def __str__(self):
        # castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == "p":
            if self.isPawnPromotion:
                return endSquare + "=+"
            elif self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        # Lay ky hieu cac quan co con lai
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
            return moveString + endSquare

        else:
            return moveString + endSquare



