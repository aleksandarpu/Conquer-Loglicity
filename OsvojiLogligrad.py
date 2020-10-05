import os, random
os.environ['PYGAME_FREETYPE'] = '1'
import pygame as pg
import start_gui
import colors, config
import board
import text_font
#import finish, player
from sound import SoundHandler, soundHandler
from config import GRID_HEIGHT, GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_SIZE
from config import WINDOW_HEIGHT, WINDOW_WIDTH
from config import Title
"""
The Simple maze game 
A Maze with walls and question fields
Walls are loaded from the file walls.txt 
Question fields position are loaded from the file fields.txt
The Questions are loaded from the files (see config.question_files) 
Player movement is with cursor keys
Dice roll with space key or mouse click at the dice
Goal is to reach crown at te top right position (can be changed in fields.txt) 
"""

SCREEN = 0
CLOCK = 0

class StartPos(pg.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(colors.BLACK)

        pg.draw.polygon(self.image, (200, 200, 0),
                            ((0, 10), (0, 20), (20, 20), (20, 30), (30, 15), (20, 0), (20, 10)))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = GRID_OFFSET_X
        self.rect.y = GRID_OFFSET_Y + GRID_HEIGHT * BLOCK_SIZE + 5


def testQuestion():
    q = gameboard.questions.qDict['lang'][0]
    a = q.draw(SCREEN)
    if a == True:
        print('Correct!')
    else:
        print('Wrong!')

def init():
    global SCREEN, CLOCK
    pg.init()
    pg.mixer.init()
    pg.font.init()

    SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(Title)
    CLOCK = pg.time.Clock()
    SCREEN.fill(colors.BLUE)
    random.seed()

if __name__ == '__main__':

    clock = pg.time.Clock()
    init()

    headerFont = text_font.load_font('comicsansms', 26)
    header = headerFont.render(Title, True, pg.Color('gold'))

    SCREEN.fill(colors.BLUE)
    SCREEN.blit(header, (int((SCREEN.get_width() - header.get_width()) / 2), 5))

    #fin = finish.Finish()
    #fin.run(SCREEN, player.Player(board.playerImages[0]))

    #testQuestion()

    gameboard = board.Board()
    gameboard.init()

    is_running = True

    while True:
        playersCount = start_gui.get_players_number(SCREEN, clock)
        #print('after start_gui.get_players_number()')
        if playersCount == -1:
            soundHandler.playSound('quit')
            #quitSound.play()
            while pg.mixer.get_busy():
                pass
            quit(0)

        #print('before setPlayers')
        gameboard.setPlayers(playersCount)
        #print('after setPlayers')
        gameboard.run(SCREEN)
