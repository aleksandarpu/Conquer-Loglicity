import pygame as pg
import time
from config import GRID_HEIGHT, GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_SIZE


class Player(pg.sprite.Sprite):
    def __init__(self, fName):
        super().__init__()
        colorKey = (255,255,255)
        self.image = pg.image.load(fName) #.convert_alpha()
        if self.image.get_alpha():
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
            self.image.set_colorkey(colorKey)
        self.rect = self.image.get_rect()
        self.xoffset = (BLOCK_SIZE - self.image.get_width()) / 2
        self.yoffset = (BLOCK_SIZE - self.image.get_height()) / 2
        self.init()

    def init(self):
        self.setPosition(0, 9)
        self.show = True
        self.steps = 0
        self.score = 0
        self.playTime = 0

    def startTime(self):
        self.runTime = int(time.time())

    def updateTime(self):
        now = int(time.time())
        #print('now={}'.format(now))
        self.playTime = self.playTime + (now - self.runTime)
        self.runTime = now

    def getTime(self):
        min = int(self.playTime / 60)
        sec = self.playTime - int(min * 60)
        if min > 60:
            h = int(min / 60)
            min = min - h * 60
            return '{}:{}:{}'.format(h, min, sec)
        else:
            #print('{}:{}'.format(min, sec))
            return '{}:{}'.format(min, sec)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = GRID_OFFSET_X + self.x * BLOCK_SIZE + self.xoffset
        self.rect.y = GRID_OFFSET_Y + self.y * BLOCK_SIZE + self.yoffset

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def draw(self, screen, x, y):
        r = self.image.get_rect()
        r.x = x
        r.y = y
        screen.blit(self.image, r)
