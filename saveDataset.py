import Board
from datetime import datetime
import FormSignIn

def saveDataset(screen, gs, resultLog, depth):
    testMoveLog = str(Board.drawMoveLog(screen, gs))
    testMoveLog = testMoveLog.replace("'", "")
    testMoveLog = testMoveLog.replace("[", "")
    testMoveLog = testMoveLog.replace("]", "")
    testMoveLog = testMoveLog.replace(",", "")  
    depth = depth.replace("(", "")  
    depth = depth.replace(")", "")
    depth = depth.replace(",", "")
    depth = str(int(depth) - 1)
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    pgn_string = "\n[Event \"Chess Game\"]\n" + \
                "[Date \"" + time_string + "\"]\n"+ \
                "[Round \"" + depth + "\"]\n" + \
                "[Result \"" + resultLog + "\"]\n" + \
                testMoveLog + \
                "\n" + resultLog + "\n"
    with open('game.pgn', 'a') as f:
        f.write(pgn_string)