import pygame
import sys

from config import *
from Button import Button
import FormGamePlay as ChessMain
import FormSwapColor as kingdom


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("guiPNG/font.ttf", size)

def onePlayer():
    pygame.display.set_caption("Chess King")
    pygame.display.set_icon(pygame.image.load("guiPNG/chessIcon.png"))

    kingdomColor = kingdom.drawKingdom()
    if kingdomColor == "white":
        ChessMain.main(True, False)
    elif kingdomColor == "black":
        ChessMain.main(False, True)
    elif kingdomColor == "bot":
        ChessMain.main(False, False)


def twoPlayer():
    pygame.display.set_caption("Chess King")
    pygame.display.set_icon(pygame.image.load("guiPNG/chessIcon.png"))

    ChessMain.main(True, True)
    # main.mainloop()

def main_menu():
    pygame.init()
    WIDTH_MENU = WIDTH + MOVE_LOG_PANEL_WIDTH
    BG = pygame.image.load("guiPNG/bgpxl.png")
    pygame.display.set_caption("Chess King")
    pygame.display.set_icon(pygame.image.load("guiPNG/chessIcon.png"))
    SCREEN = pygame.display.set_mode((WIDTH_MENU, HEIGHT))
    while True:
        # Set BG
        SCREEN.blit(BG, (0, 0))
        # Draw Main Menu text
        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH_MENU / 2, 150))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Draw Button
        PLAY_BUTTON = Button(image=pygame.image.load("guiPNG/Play Rect.png"), pos=(WIDTH_MENU / 2, 300),
                             text_input="1 PLAYER", font=get_font(30), base_color="White",
                             hovering_color="Gray")
        OPTIONS_BUTTON = Button(image=pygame.image.load("guiPNG/Play Rect.png"), pos=(WIDTH_MENU / 2, 450),
                                text_input="2 PLAYER", font=get_font(30), base_color="White",
                                hovering_color="Gray")
        QUIT_BUTTON = Button(image=pygame.image.load("guiPNG/Quit Rect.png"), pos=(WIDTH_MENU / 2, 600),
                             text_input="QUIT", font=get_font(30), base_color="White", hovering_color="Gray")

        # Draw credit text
        credits_text = get_font(12).render("Create by group 2", True, "#b77f42")
        credits_rect = credits_text.get_rect(center=(WIDTH_MENU / 2, 730))
        SCREEN.blit(credits_text, credits_rect)

        # Ve lai mau sac cac nut len man hinh
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Bat su kien cac nut
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    onePlayer()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    twoPlayer()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
