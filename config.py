import pygame as pg

Title='Osvoji Logligrad'
WinnerMsg='Pobednik je '
question_files = ['data/questions-asoc.txt', 'data/questions-math.txt', 'data/questions-srpski.txt', 'data/questions-zvezda.txt']
mazeWallFile = 'data/walls.txt'
FieldsFile = 'data/fields.txt'
playerImages = ['images/smile-yellow.png', 'images/smile-blue1.png', 'images/smile-green2.png',
                'images/smile-blue2.png', 'images/smile-orange1.png','images/smile-pink1.png',
                'images/smile-violet.png']

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
GRID_HEIGHT = 10
GRID_WIDTH = 10
GRID_OFFSET_X = 10
GRID_OFFSET_Y = 40
BLOCK_SIZE = 44

errSound1 = ''
