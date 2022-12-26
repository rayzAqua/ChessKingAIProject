import time

import pygame as pg
import sys

from config import *
from Button import Button
import FormGamePlay as ChessMain
import FormSwapColor as kingdom
import FormSignIn

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font("guiPNG/font.ttf", size)


def onePlayer(level, isPlayerMode):
    pg.display.set_caption("Chess King")
    pg.display.set_icon(pg.image.load("guiPNG/chessIcon.png"))

    kingdomColor = kingdom.drawKingdom()
    if kingdomColor == "white":
        ChessMain.main(True, False, level, isPlayerMode)
    elif kingdomColor == "black":
        ChessMain.main(False, True, level, isPlayerMode)
    elif kingdomColor == "bot":
        ChessMain.main(False, False, level, isPlayerMode)


def twoPlayer(isPlayerMode):
    pg.display.set_caption("Chess King")
    pg.display.set_icon(pg.image.load("guiPNG/chessIcon.png"))

    ChessMain.main(True, True, 0, isPlayerMode)
    # main.mainloop()


def main_menu():
    pg.init()
    WIDTH_MENU = WIDTH + MOVE_LOG_PANEL_WIDTH
    BG = pg.image.load("guiPNG/bgpxl.png")
    pg.display.set_caption("Chess King")
    BG_MUSIC = pg.mixer.Sound("music/bg_music.mp3")
    BG_MUSIC.set_volume(0.3)
    BG_MUSIC.play(-1)
    MENU_BUTTON_SFX = pg.mixer.Sound("music/button_effect.mp3")
    SCREEN = pg.display.set_mode((WIDTH_MENU, HEIGHT))
    while True:
        # Set BG
        SCREEN.blit(BG, (0, 0))
        # Draw Main Menu text
        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH_MENU / 2, 150))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        # Draw Button
        PLAY_BUTTON = Button(image=pg.image.load("guiPNG/Play Rect.png"), pos=(WIDTH_MENU / 2, 300),
                             text_input="1 PLAYER", font=get_font(30), base_color="White",
                             hovering_color="Gray")
        OPTIONS_BUTTON = Button(image=pg.image.load("guiPNG/Play Rect.png"), pos=(WIDTH_MENU / 2, 450),
                                text_input="2 PLAYER", font=get_font(30), base_color="White",
                                hovering_color="Gray")
        QUIT_BUTTON = Button(image=pg.image.load("guiPNG/Quit Rect.png"), pos=(WIDTH_MENU / 2, 600),
                             text_input="QUIT", font=get_font(30), base_color="White", hovering_color="Gray")

        # Draw credit text
        credits_text = get_font(12).render("Created by group 2", True, "#b77f42")
        credits_rect = credits_text.get_rect(center=(WIDTH_MENU / 2, 730))
        SCREEN.blit(credits_text, credits_rect)

        # Ve lai mau sac cac nut len man hinh
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Bat su kien cac nut
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                MENU_BUTTON_SFX.play()
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    time.sleep(0.3)
                    # onePlayer()
                    # pg.quit()
                    FormSignIn.formSignin()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    time.sleep(0.3)
                    isPlayerMode = True
                    twoPlayer(isPlayerMode)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    time.sleep(0.3)
                    pg.quit()
                    sys.exit()

        pg.display.flip()

# def CheckPlayer(player):
#     if player:
#         is_Two_Mode = True
#         return is_Two_Mode
#     else:
#         is_Two_Mode = False
#     return is_Two_Mode


if __name__ == "__main__":
    main_menu()
