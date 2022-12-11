import pygame, sys
from Button import Button
import ChessMain
from config import WIDTH, HEIGHT

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess King")

BG = pygame.image.load("guiPNG/bgpxl.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("guiPNG/font.ttf", size)


def onePlayer():
    # while True:
    #     PLAY_MOUSE_POS = pygame.mouse.get_pos()
    #
    #     SCREEN.fill("black")
    #
    #     PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
    #     PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
    #     SCREEN.blit(PLAY_TEXT, PLAY_RECT)
    #
    #     PLAY_BACK = Button(image=None, pos=(640, 460),
    #                        text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
    #
    #     PLAY_BACK.changeColor(PLAY_MOUSE_POS)
    #     PLAY_BACK.update(SCREEN)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
    #                 main_menu()
    #
    #     pygame.display.update()
    main = ChessMain.Main(True, False)
    main.mainloop()


def twoPlayer():
    # # while True:
    #     OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    #
    #     # SCREEN.fill("white")
    #     #
    #     # OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
    #     # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
    #     # SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
    #
    #     OPTIONS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
    #
    #     OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    #     OPTIONS_BACK.update(SCREEN)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
    #                 main_menu()
    #
    #     pygame.display.update()

    main = ChessMain.Main(True, True)
    main.mainloop()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 150))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(image=pygame.image.load("guiPNG/Play Rect.png"), pos=(WIDTH/2, 300),
                             text_input="1 PLAYER", font=get_font(40), base_color="White", hovering_color="Gray")
        OPTIONS_BUTTON = Button(image=pygame.image.load("guiPNG/Play Rect.png"), pos=(WIDTH/2, 450),
                                text_input="2 PLAYER", font=get_font(40), base_color="White", hovering_color="Gray")
        QUIT_BUTTON = Button(image=pygame.image.load("guiPNG/Quit Rect.png"), pos=(WIDTH/2, 600),
                             text_input="QUIT", font=get_font(40), base_color="White", hovering_color="Gray")

        credits_text = get_font(12).render("Create by group 2", True, "#b77f42")
        credits_rect = credits_text.get_rect(center=(WIDTH/2, 730))
        SCREEN.blit(credits_text, credits_rect)

        # Ve cac nut len man hinh
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


main_menu()