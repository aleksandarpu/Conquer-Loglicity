import pygame as pg
from config import GRID_HEIGHT, GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_SIZE
import Point

class QuestionSprite(pg.sprite.Sprite):

    def __init__(self, width, height, fName):
        super().__init__()

        colorKey = (255,255,255)
        self.image = pg.image.load(fName)
        if self.image.get_alpha():
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
            self.image.set_colorkey(colorKey)

        self.rect = self.image.get_rect()

class Fields:
    def __init__(self):
        self.questionSprites = pg.sprite.Group()
        self.questionFields = []

    def initImages(self):
        for q in self.questionFields:
            x = GRID_OFFSET_X + int(q[1]) * BLOCK_SIZE
            y = GRID_OFFSET_Y + int(q[2]) * BLOCK_SIZE
            if q[0] == 'math':
                s = QuestionSprite(30, 30, 'images/5.png')
            elif q[0] == 'lang':
                s = QuestionSprite(30, 30, 'images/l.png')
            elif q[0] == 'star':
                s = QuestionSprite(30, 30, 'images/star.png')
            elif q[0] == 'assoc':
                s = QuestionSprite(30, 30, 'images/a.png')

            s.rect.x = x + (BLOCK_SIZE - s.image.get_width()) / 2
            s.rect.y = y + (BLOCK_SIZE - s.image.get_height()) / 2
            self.questionSprites.add(s)

    def loadFieldsPositions(self, fName):
        # one item prer line: type, x, y type is M,L,A,S,N
        with open(fName, 'r') as f:
            line = f.readline(100)
            while line:
                s = line.split(',')
                if s[0] == '5':
                    self.questionFields.append(('math', int(s[1]), int(s[2])))
                elif s[0] == 'L':
                    self.questionFields.append(('lang', int(s[1]), int(s[2])))
                elif s[0] == 'Z':
                    self.questionFields.append(('star', int(s[1]), int(s[2])))
                elif s[0] == 'A':
                    self.questionFields.append(('assoc', int(s[1]), int(s[2])))
                elif s[0] == 'W':
                    # Load finish point too
                    self.finishPoint = Point.Point(int(s[1]), int(s[2]))
                    self.finishImage = pg.image.load('images/crown1.png') #.convert_alpha()
                    if self.finishImage.get_alpha():
                        self.finishImage = self.finishImage.convert_alpha()
                    else:
                        colorKey = (255, 255, 255)
                        self.finishImage = self.finishImage.convert()
                        self.finishImage.set_colorkey(colorKey)

                line = f.readline(100)

        self.initImages()

    def getAt(self, x : int, y : int) -> str:
        for v in self.questionFields:
            if v[1] == x and v[2]== y:
                return v[0]
        return None

    def drawSprites(self, scr):
        self.questionSprites.draw(scr)
