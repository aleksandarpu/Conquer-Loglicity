import pygame as pg
from sound import soundHandler
from player import Player
import sys, random, time
import text_font
import colors

class Dice():
    def __init__(self):
        scr = pg.display.get_surface()
        offsetX = 200
        self.diceFrameRect = pg.Rect(scr.get_width() - 70 - offsetX, scr.get_height() - 70, 60, 60)
        self.diceTxtRect = pg.Rect(scr.get_width() - 120 - offsetX, scr.get_height() - 120, 200, 60)
        self.dicePlayerX = scr.get_width() - 110 - offsetX
        self.dicePlayerY = scr.get_height() - 55

        self.diceX = scr.get_width() - 65 - offsetX
        self.diceY = scr.get_height() - 65

        self.diceImages = []
        for i in range(4):
            img = pg.image.load('images/dice/{}.png'.format(i+1))
            img = pg.transform.scale(img, (50, 50))
            self.diceImages.append(img)  # .convert_alpha()


    def draw(self, SCREEN, i):
        SCREEN.blit(self.diceImages[i], (self.diceX, self.diceY))

    def animateRoll(self, scr):
        ret = 0
        soundHandler.playSound('roll')
        time.sleep(0.1)
        for i in range(10):
            ret = random.randrange(len(self.diceImages))
            self.draw(scr, ret)
            pg.display.update()
            time.sleep(0.2)

        while pg.mixer.get_busy():
            pass
        #time.sleep(0.2)
        return ret + 1

    def rollDice(self, scr, player : Player):
        msg = '   Klikni ili stisni\n' \
              'razmaklicu za broj koraka'
        text_font.drawText(scr, msg, colors.questionColor, self.diceTxtRect, 'freesans', 24, True)
        pg.draw.rect(scr, pg.Color('darkolivegreen3'), self.diceFrameRect, 10)
        pg.draw.rect(scr, pg.Color('darkolivegreen2'), self.diceFrameRect, 7)
        pg.draw.rect(scr, pg.Color('darkolivegreen1'), self.diceFrameRect, 4)
        pg.draw.rect(scr, pg.Color('darkred'), self.diceFrameRect, 2)
        self.draw(scr, -1)

        #self.player.blit(scr)
        #self.drawCurrentPlayer(scr)
        scr.blit(player.image, (self.dicePlayerX, self.dicePlayerY))
        pg.display.update()

        isFinished = False

        while not isFinished:
            pos = pg.mouse.get_pos()
            pressed1, pressed2, pressed3 = pg.mouse.get_pressed()
            # Check if the rect collided with the mouse pos
            # and if the left mouse button was pressed.
            if self.diceFrameRect.collidepoint(pos) and pressed1:
                return self.animateRoll(scr)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return self.animateRoll(scr)
            pg.display.update()

        # time.sleep(10)
        return -1
