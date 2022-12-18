import pygame as pg
import sys
from config import *
from Button import Button
import FormGamePlay as ChessMain

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font("guiPNG/font.ttf", size)


def drawKingdom():
    pg.init()
    screen = pg.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    backGround = pg.image.load("guiPNG/bgpxl.png")
    s = pg.Surface((700, 600))
    s.set_alpha(100)
    s.fill("#CCFF66")
    TEXT = get_font(30).render("CHOOSE YOUR KINGDOM!", True, "#669966")
    TEXT_RECT = TEXT.get_rect(center=((WIDTH + MOVE_LOG_PANEL_WIDTH)/2, 175))

    running = True
    while running:
        screen.blit(backGround, (0, 0))
        screen.blit(s, ((WIDTH + MOVE_LOG_PANEL_WIDTH) / 2 - s.get_width() / 2, HEIGHT / 2 - s.get_height() / 2))
        screen.blit(TEXT, TEXT_RECT)

        MOUSE_POS = pg.mouse.get_pos()

        PLAY_AS_WHITE = Button(image=pg.transform.scale(pg.image.load("guiPNG/Play Rect.png"), (250, 109)),
                               pos=((WIDTH + MOVE_LOG_PANEL_WIDTH)/2-150, 300), text_input="WHITE", font=get_font(22),
                               base_color="White", hovering_color="Gray")
        PLAY_AS_BLACK = Button(image=pg.transform.scale(pg.image.load("guiPNG/Play Rect.png"), (250, 109)),
                               pos=((WIDTH + MOVE_LOG_PANEL_WIDTH)/2 + 150, 300), text_input="BLACK", font=get_font(22),
                               base_color="White", hovering_color="Gray")
        BOT_PK = Button(image=pg.transform.scale(pg.image.load("guiPNG/Play Rect.png"), (550, 109)),
                        pos=((WIDTH + MOVE_LOG_PANEL_WIDTH)/2, 450), text_input="RELAX AND CHILL !!", font=get_font(22),
                        base_color="White", hovering_color="Gray")
        BACK_BUTTON = Button(image=pg.image.load("guiPNG/Quit Rect.png"), pos=((WIDTH + MOVE_LOG_PANEL_WIDTH)/2, 600),
                             text_input="BACK", font=get_font(22), base_color="White", hovering_color="Gray")

        for button in [PLAY_AS_WHITE, PLAY_AS_BLACK, BACK_BUTTON, BOT_PK]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

            # Bat su kien cac nut
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_AS_WHITE.checkForInput(MOUSE_POS):
                    return "white"
                if PLAY_AS_BLACK.checkForInput(MOUSE_POS):
                    return "black"

                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    running = False

                if BOT_PK.checkForInput(MOUSE_POS):
                    return "bot"

        pg.display.update()

# drawKingdom()
