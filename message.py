import time, sys
import pygame as pg
from text_font import load_font


class MessageBox():
    '''
    Timed message box
    '''
    def __init__(self, scr: pg.Surface, font : str, size : int, w : int, h : int, bgColor : pg.Color):
        r = scr.get_rect()
        self.x = int((r.width - w) / 2)
        self.y = int((r.height - h) / 2)
        self.width = w
        self.height = h
        self.rect = pg.Rect(self.x,self.y, w, h)
        self.bgColor = bgColor
        self.font = load_font(font, size)

    def _drawText(self, msg: str, txtColor : pg.Color):
        msgs = msg.split('\n')
        images = []
        for m in msgs:
            images.append(self.font.render(m, 1, txtColor))
        return images

    def draw(self, scr: pg.Surface, msg: str, txtColor : pg.Color, pause : int = 0):
        '''
        timmed message. If pause > 0 auto-close box agter paue seconds
        :param scr:
        :param msg: multi-line message
        :param txtColor: message color (also border color
        :param pause:
        :return:
        '''
        pg.draw.rect(scr, self.bgColor, self.rect)
        pg.draw.rect(scr, txtColor, self.rect, 2)
        images = self._drawText(msg, txtColor)
        h1 = images[0].get_height()
        y = 20
        for img in images:
            x = self.x + int((self.width - img.get_width()) / 2)
            scr.blit(img, (x, self.y + y))
            y = y + h1 + 2

        pg.display.update()
        #if pause > 0:
        #    time.sleep(pause)
        #    return
        start = time.time()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return
            now = time.time()
            if pause > 0 and now - start > pause:
                return
