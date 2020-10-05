import pygame as pg
import sys
import text_font
from player import Player
from config import WINDOW_HEIGHT, WINDOW_WIDTH, WinnerMsg
import colors
from sound import soundHandler

class Finish():
    def __init__(self):
        pass

    def run(self, scr : pg.Surface, player : Player):
        crownImage = pg.image.load('images/crown1.png')  # .convert_alpha()
        winnerFont = text_font.load_font('comicsansms', 46)
        winner = winnerFont.render(WinnerMsg, True, pg.Color('gold'))

        soundHandler.playSound('win')
        r = scr.get_rect()
        view = scr.subsurface(100, 100, r.width - 200, r.height - 200)
        view.fill(pg.Color('chocolate4'))
        pg.draw.rect(view, pg.Color('darkolivegreen3'), view.get_rect(), 10)
        pg.draw.rect(view, pg.Color('darkolivegreen2'), view.get_rect(), 7)
        pg.draw.rect(view, pg.Color('darkolivegreen1'), view.get_rect(), 4)
        pg.draw.rect(view, pg.Color('darkred'), view.get_rect(), 2)

        winnerX = (view.get_width() - winner.get_width() - player.image.get_width()) / 2 - 10
        view.blit(winner, (winnerX, 25))
        player.draw(view, winnerX + 10 + winner.get_width(), 45)

        #player.draw(view, 100, 100)

        txtRect = pg.Rect(145, 30, 500, 200)
        #msg = 'Pobednik je'
        #text_font.drawText(view, msg, colors.questionColor, txtRect, 'freesans', 48, True)

        txtRect.y = 60
        msg = '{} poen{}, vreme {}'.format(player.score, '' if player.score == 1 else 'a', player.getTime())
        #msgFont = text_font.load_font('comicsansms', 32)
        msgFont = text_font.load_font('comicsanserf', 32)
        msgSurface = msgFont.render(msg, True, pg.Color('gold'))
        msgX = (view.get_width() - msgSurface.get_width()) / 2
        msgY = 25 + winner.get_height() + 10
        view.blit(msgSurface, (msgX, msgY))
        crownY = msgY + 10 + msgSurface.get_height()
        crownH = view.get_height() - crownY
        percent = crownH / crownImage.get_height()
        crownW = int(percent * crownImage.get_width())
        pic = pg.transform.scale(crownImage, (crownW, crownH))
        crownX = (view.get_width() - pic.get_width()) / 2

        view.blit(pic, (crownX, crownY))

        msg = 'Logligradsko kraljevstvo je tvoje!'
        msgSurface = msgFont.render(msg, True, pg.Color('gold'))
        msgX = (view.get_width() - msgSurface.get_width()) / 2
        msgY = view.get_height() - 30
        view.blit(msgSurface, (msgX, msgY))

        #text_font.drawText(view, msg, colors.questionColor, txtRect, 'freesans', 48, True)

        while True:
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    return
                if event.type == pg.MOUSEBUTTONDOWN:
                    return
