import random
import FormSignIn

"""
Nguyen lieu diem so cua tung quan co, nguyen lieu nay dung de tinh toan ra bang diem vi tri
"""
try:
    temp, level = FormSignIn.showInformation()
except:
    level = 2

# Diem so cua tung quan co - Nguyen lieu
pieceScores = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 2, 4, 4, 2, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 2, 4, 4, 2, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

chessPossitonsDict = {"wp": whitePawnScores, "bp": blackPawnScores}

# Neu chieu tuong thi diem vi tri la cao nhat
CHECKMATE = 1000
# Chieu bi la khi di duong nao` cung bi doi thu de doa, cho nen chieu bi se = 0, = 0 tot hon la thuc hien nuoc di
# voi rui ro la bi an mat nuoc do
STALEMATE = 0
# DEPTH = level
DEPTH = 3
# print(DEPTH)
# Tao ra mot so nguyen i ngau nhien va truyen no vao list validMoves, sau do tra ve validMove[i]
def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# Giai thuat tham lam: La giai thuat tim ra giai phap toi uu nhat sao cho gia tri ma no dat duoc la lon nhat (dung tham lam), co the
# hieu la "lam` thi it ma muon dat duoc luong cao".
# Thuat toan tham lam duoc ap dung o day la de tim ra nuoc di tot nhat sao cho score co gia tri la cao nhat' cho ban than
# va thap nhap cho doi thu
# Tai day neu ap dung thuat toan tham lam nay vao thi de dat duoc gia tri score cao nhat no se chi dam dau vao viec
# an cac quan co cua doi thu ma khong them quan tam lam the nao de chieu tuong
# -> Thuat toan nay qua ngu cho nen nang cap no thanh minimax.
def findBestMoveMinMaxNoRecursively(gs, validMoves):
    turnValue = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE  # Diem so lon nhat cua doi thu
    bestPlayerMove = None
    random.shuffle(validMoves)  # Lam xao' tron danh sach mot cach ngau nhien
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMove()
        if gs.checkMate:
            opponentMaxScore = -CHECKMATE
        elif gs.staleMate:
            opponentMaxScore = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:  # Tra ve gia tri lon nhat cua no
                gs.makeMove(opponentMove)
                # Ly do cho su xuat hien cua no la vi can phai kiem tra lai the co xem co checkmate hay kh
                gs.getValidMove()
                if gs.checkMate:  # Neu quan trang ma chieu tuong duoc quan den
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:  # Tinh toan diem so nuoc di
                    # Chuyen gia tri max cua nguoi choi thanh gia tri am
                    # Ly do: gia tri max cua nguoi choi la gia tri co loi nhat cho nguoi choi
                    # va cai chung ta can tim o day la gia tri diem so sao cho bot co loi. nhat
                    # Nhu vay, gia tri diem so cua nguoi choi cang lon thi con bot no cang bat loi
                    # chinh vi li do do', ta co mot ly thuyet rang: gia tri nho nhat cua nguoi choi se la gia tri lon
                    # nhat cua con Bot (Mini-Max)m va de thuc hien dc ly thuyet nay ta can chuyen gia tri max cua ng
                    # choi thanh gia tri am. VD: 10 > 1 ---> -10 < -1
                    score = -turnValue * scoreMaterial(gs.board)
                if score > opponentMaxScore:  # Tim ra gia tri nho nhat cua nguoi choi
                    opponentMaxScore = score
                gs.undoMove()
        # Voi viec kiem tra tung nuoc di co the, AI se tim ra duoc gia tri diem so nuoc di lon nhat cua nguoi choi
        # sau do tim ra gia tri nho nhat trong so cac gia tri lon nhat do de thuc hien nuoc di cua minh.
        # Vi du: con tot cua nguoi choi co the an duoc con tot cua no neu no thuc hien nuoc di voi hang ben canh
        # luc nay no tinh toan ra gia tri cua nguoi choi se la 1
        # sau do no se so sanh voi gia tri mac dinh la 1000 va dat lai gia tri mac dinh la 1
        # tiep tuc thuc hien cac nuoc di khac va sau do lai thuc hien nuoc di cua nguoi choi, neu luc ket thuc
        # qua trinh tim kiem diem so ma no tim duoc gia tri nho hon 1 thi gia tri do chinh la gia tri nho nhat cua nguoi
        # choi va gia tri nho nhat do chinh la best move cua AI
        # Quy luat tham lam: tim kiem gia tri sao cho gia tri cua ban than la lon nhat con gia tri cua nguoi choi la nho
        # nhat
        # Co the hieu rang: Diem so thap nhat cua nguoi choi la diem so cao nhat cua AI
        if opponentMaxScore < opponentMinMaxScore:  # Tim gia tri min trong so cac gia tri max cua nguoi choi
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

# Ham ho tro goi de quy MinMax
def findBestMove(gs, validMoves, returnQueue):
    global botBestMove, counter
    counter = 0
    botBestMove = None
    # Lam xao tron danh sach validMove
    random.shuffle(validMoves)
    # findMoveMinMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, gs.whiteToMove)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    # print("So lan de quy: " + str(counter))
    returnQueue.put(botBestMove)

# Giai thuat MinMax: Giai thuat luon tim cach lam max diem so nuoc di cua minh sao cho no la lon nhat
# va lam cho diem so cua doi thu la nho nhat
# - Doi voi quan trang Score se la so duong: so duong cang lon thi cang co loi.
# - Doi voi quan mau den Scoẻ se la so am: so am cang lon thi cang co loi.
# Chi vi the nen giai thuat minMax se tim ra gia tri MAX cua doi thu sau do lam am no di
# Dieu nay se khien cho gia tri lon nhat cua doi thu (gia tri lam cho ban than bi bat loi) tro thanh gia tri so am nho
# nhat cua ban than -> Bien bat loi thanh co loi.
# No se lam cho gia tri nho nhat cua doi thu tro thanh lon nhat cho ban than - Gia tri doi thu cang nho thi khi doi dau
# no se tro thanh gia tri am lon nhat cua ban than.
# VD: - Quan trang thuc hien quan hau an quan hau cua quan den va co duoc so diem la 10
# - Quan trang thuc hien quan tot va khien cho ban than mat hau va diem dat duoc la -10
# Nhu vay AI se tinh toan dc la 30 la diem so bat loi cho ban than, no se bien 10 thanh -10, va
# bien diem so bat loi cua doi thu la -10 thanh 10 va ghi lai do la MAX cua ban than.
def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global botBestMove, counter

    if depth == 0:
        return scoreMaterial(gs.board)

    counter += 1

    if whiteToMove:
        # Quan trang co gang lam max gia tri duong cua ban than nen khoi dau bang gia tri thap nhat
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            opponentMoves = gs.getValidMove()
            score = findMoveMinMaxAlphaBeta(gs, opponentMoves, depth - 1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    botBestMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

    else:
        # Quan den co gang lam min di gia tri cua quan trang nen khoi dau bang gia tri cao nhat
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            opponentMoves = gs.getValidMove()
            score = findMoveMinMaxAlphaBeta(gs, opponentMoves, depth - 1, beta, alpha, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    botBestMove = move
            gs.undoMove()
            if beta > minScore:
                beta = minScore
            if alpha >= beta:
                break
        return minScore

# Bien the cua MinMax - NegaMax
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnValue):
    global botBestMove, counter
    if depth == 0:
        return turnValue * scoreBoard(gs)

    counter += 1

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        opponentMoves = gs.getValidMove()
        score = -findMoveNegaMaxAlphaBeta(gs, opponentMoves, depth - 1, -beta, -alpha, -turnValue)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                botBestMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# Tinh toan cac diem so vi tri tren ban co:
# + Neu la so duong thi do la gia tri thang cho quan trang
# + Neu la so am thi do la gia tri thang cho quan den
# Ham phu trach tinh diem so dua tren nguyen lieu
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":  # Quan trang thi gia tri duong
                score += pieceScores[square[1]]
            elif square[0] == "b":  # Quan den thi gia tri am
                score -= pieceScores[square[1]]
    return score

# Quan trang diem so co loi. la so duong, quan den diem so co loi. la so am
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:  # Quan den thang' thi tra ve -CHECKMATE sau do luc goi de quy thi no se chuyen thanh 1000
            return -CHECKMATE
        else:  # Quan trang thang' sau do luc goi de quy thi no se chuyen thanh 1000
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square == "wp":
                    piecePositionScore = chessPossitonsDict["wp"][row][col]
                elif square == "bp":
                    piecePositionScore = chessPossitonsDict["bp"][row][col]

                if square[0] == "w":  # Quan trang thi gia tri duong
                    score += pieceScores[square[1]] + piecePositionScore
                elif square[0] == "b":  # Quan den thi gia tri am
                    score -= pieceScores[square[1]] + piecePositionScore

    return score
