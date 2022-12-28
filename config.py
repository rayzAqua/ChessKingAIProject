'''
File này chứa các kích thước của trò chơi
'''

import socket

'''
GAME SCREEN
'''
# Chiều rộng bàn cờ
WIDTH = 800
# Chiều cao bàn cờ
HEIGHT = 800
# Bàn cờ có 8 hàng, 8 cột
DIMENSION = 8
# Kích thước một ô vuông trên bàn cờ bằng 8 lần chiều dài hoặc chiều cao
SQ_SIZE = HEIGHT // DIMENSION

MOVE_LOG_PANEL_WIDTH = 400
MOVE_LOG_PANEL_HEIGHT = 600
WIDTH_BUTTON = MOVE_LOG_PANEL_WIDTH/3
HEIGHT_BUTTON = 100

'''
Other
'''
PIECE_NAME = []
# Tối đa số lần lặp trong một giây (FPS)
MAX_FPS = 15
# Một thư viện ảnh dùng lưu trữ ảnh của từng quân cờ
IMAGES = {}
# CONNECT DATABASE
USER_NAME = socket.gethostname()
IP = socket.gethostbyname(USER_NAME)
MSSQL_LOGIN = 'sa'
MSSQL_PASSWORD = '123'
DB_NAME = 'ChessAIProject'