import pygame as pg
from config import GRID_HEIGHT, GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_SIZE
import colors
from player import Player

class Maze:
    def __init__(self, fName : str):
        self.vList = []
        self.hList = []
        self.hWalls = []
        self.vWalls = []
        for i in range(GRID_HEIGHT):
            self.vWalls.append([])
        for i in range(GRID_WIDTH):
            self.hWalls.append([])

        self.loadMaze(fName)

    def getLine(self, f):
        line = f.readline(100)
        if len(line) == 0:
            return ''
        while line == '':
            line = f.readline(100)
        while line[0] == '#' or line[0] == '\n':
            line = f.readline(100)
            if len(line) == 0 or line == '':
                return ''
        return line

    def _loadMazeFile(self, fName : str):
        with open(fName, 'r') as f:
            line = self.getLine(f)
            while line:
                l = line.split(',')
                for item in l:
                    item = item.strip()
                    if item[0] == 'V':
                        self.vList.append(item)
                    elif item[0] == 'H':
                        self.hList.append(item)
                line = self.getLine(f)

    def loadMaze(self, fName : str):
        # load data from file into list
        # call generateMaze to create maze from this list
        #self.vList = ['V 3 5', 'V 4 5', 'V 5 5', 'V 9 1']
        #self.hList = ['H 0 2', 'H 2 3', 'H 3 3', 'H 7 6', 'H 8 6', 'H 9 6']
        self._loadMazeFile(fName)

        for h in self.hList:
            lh = h.split(' ')
            row = int(lh[1])
            pos = int(lh[2])
            self.hWalls[row].append(pos)
        for v in self.vList:
            lv = v.split(' ')
            col = int(lv[1])
            pos = int(lv[2])
            self.vWalls[col].append(pos)

    def drawGrid(self, scr : pg.Surface):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pg.Rect(GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE,
                                   BLOCK_SIZE, BLOCK_SIZE)
                pg.draw.rect(scr, colors.WHITE, rect, 1)

    def drawWalls(self, scr: pg.Surface):
        for i in range(GRID_WIDTH):
            h = self.hWalls[i]
            for pos in h:
                pg.draw.line(scr, colors.RED,
                    (GRID_OFFSET_X + i * BLOCK_SIZE,       GRID_OFFSET_Y + (pos + 1) * BLOCK_SIZE - 2),
                    (GRID_OFFSET_X + (i + 1) * BLOCK_SIZE, GRID_OFFSET_Y + (pos + 1) * BLOCK_SIZE - 2), 4)

        for i in range(GRID_HEIGHT):
            v = self.vWalls[i]
            for pos in v:
                pg.draw.line(scr, colors.RED,
                    (GRID_OFFSET_X + (pos + 1) * BLOCK_SIZE - 2, GRID_OFFSET_Y + i * BLOCK_SIZE),
                    (GRID_OFFSET_X + (pos + 1) * BLOCK_SIZE - 2, GRID_OFFSET_Y + (i + 1) * BLOCK_SIZE), 4)


    def checkWallCollision(self, player: Player, x: int, y : int) -> bool:
        """
        Test player vs wall collision
        :param player: current player - x,y are player old position
        :param x: increment in x direction (-1 for left, +1 for right)
        :param y: increment in y direction (-1 for up, +1 for down)
        :return: True if player collide with wall, else return False
        """
        if y != 0:
            h = self.hWalls[player.x]

            l = min(player.y, player.y + y)
            r = max(player.y, player.y + y)
            for pos in h:
                if l == pos:
                    return True
        else:
            v = self.vWalls[player.y]
            l = min(player.x + x, player.x)
            r = max(player.x + x, player.x)
            for pos in v:
                if l == pos and r == pos + 1:
                    return True

        return False

    def draw(self, scr: pg.Surface):
        self.drawGrid(scr)
        self.drawWalls(scr)