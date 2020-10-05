import os, sys, time
os.environ['PYGAME_FREETYPE'] = '1'
import pygame as pg

import text_font
from config import GRID_HEIGHT, GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_SIZE
from config import playerImages
from player import Player
from dice import Dice
from sound import soundHandler
from Fields import Fields
import colors, questions, maze, finish, config, message

class Board():

    def init(self):
        self.questions = questions.Questions()
        self.questions.loadQuestions(config.question_files)

        self.Fields = Fields()
        self.Fields.loadFieldsPositions(config.FieldsFile)
        self.finishPoint = self.Fields.finishPoint

        self.maze = maze.Maze(config.mazeWallFile)
        self.currentPlayer = -1
        self.player = None
        self.dice = Dice()

        self.playerColor = colors.playerColor
        self.scoreColor = colors.scoreColor

        headerFont = text_font.load_font('comicsanserf', 32)
        self.header = headerFont.render(config.Title, True, pg.Color('gold'))
        self.messageBoxWin =  message.MessageBox(pg.display.get_surface(), 'comicsansms', 26, 400, 300, colors.winMsgBgColor)
        self.messageBoxLose =  message.MessageBox(pg.display.get_surface(), 'comicsansms', 26, 400, 300, colors.loseMsgBgColor)

    def clear(self):
        self.currentPlayer = -1
        self.player = None
        for p in self.players:
            p.init()

    def getQuestion(self, x, y):
        x = self.Fields.getAt(x, y)
        if x is None:
            return None
        return self.questions.getQuestion(x)

    def setPlayers(self, count):
        self.players = []
        for i in range(count):
            self.players.append(Player(playerImages[i]))

        self.playersForScore = []
        for i in range(count):
            self.playersForScore.append(Player(playerImages[i]))
        self.clear()

    def drawScoreTable(self, scr):
        for i in range(len(self.players)):
            offsetX = GRID_OFFSET_X + BLOCK_SIZE * GRID_WIDTH + 60
            offsetY = GRID_OFFSET_Y + 10
            r = pg.Rect(offsetX, offsetY, scr.get_width() - offsetX - 10, len(self.players) * 50 + 20)
            pg.draw.rect(scr, pg.Color('darkolivegreen3'), r, 10)
            pg.draw.rect(scr, pg.Color('darkolivegreen2'), r, 7)
            pg.draw.rect(scr, pg.Color('darkolivegreen1'), r, 4)
            pg.draw.rect(scr, pg.Color('darkred'), r, 2)
            offsetX = offsetX + 15
            offsetY = offsetY + 15
            self.playersForScore[i].draw(scr, offsetX, offsetY + i * 50)
            msg = '{} poen{}. Vreme {}'.format(self.players[i].score, '' if self.players[i].score == 1 else 'a', self.players[i].getTime())
            rect = pg.Rect(offsetX + 50, offsetY + i * 50 + 5, 300, 100)
            r = text_font.drawText(scr, msg, self.scoreColor, rect, 'FreeSans.ttf', 32, True)

    def drawCurrentPlayer(self, scr):
        offsetY = GRID_OFFSET_Y + BLOCK_SIZE * GRID_HEIGHT + 30
        r = pg.Rect(10, offsetY, 500, scr.get_height() - offsetY - 10)
        pg.draw.rect(scr, colors.BLUE, r)
        pg.draw.rect(scr, pg.Color('darkolivegreen3'), r, 10)
        self.playersForScore[self.currentPlayer].draw(scr, 30, offsetY + 10)
        msg = '{} korak{}. {} poen{}. Vreme {}'.format(self.players[self.currentPlayer].steps,
                                                     '' if self.players[self.currentPlayer].steps == 1 else 'a',
                                                     self.players[self.currentPlayer].score,
                                                     '' if self.players[self.currentPlayer].score == 1 else 'a',
                                                     self.players[self.currentPlayer].getTime())
        rect = pg.Rect(70, offsetY + 15, 400, 100)
        r = text_font.drawText(scr, msg, self.playerColor, rect, 'freesans', 32, True)

    def drawBoard(self, scr):
        scr.fill(colors.BLUE)
        scr.blit(self.header, ((scr.get_width() - self.header.get_width())/ 2, 5))

        self.maze.draw(scr)
        self.Fields.drawSprites(scr)
        self.drawFinishPoint(scr)
        #print('before drawScoreTable')
        self.drawScoreTable(scr)
        #print('after drawScoreTable')
        self.drawCurrentPlayer(scr)
        #print('after drawCurrentPlayer')

    def drawFinishPoint(self, scr):
        rect = self.Fields.finishImage.get_rect()
        pic = pg.transform.scale(self.Fields.finishImage, (BLOCK_SIZE, BLOCK_SIZE))
        rect.x = GRID_OFFSET_X + self.finishPoint.X * BLOCK_SIZE
        rect.y = GRID_OFFSET_Y + self.finishPoint.Y * BLOCK_SIZE

        scr.blit(pic, rect)

    def selectPlayer(self, SCREEN):
        if self.currentPlayer == -1:
            self.currentPlayer = 0
            self.player = self.players[self.currentPlayer]
            self.player.blit(SCREEN)
            self.drawCurrentPlayer(SCREEN)
            self.player.steps = self.dice.rollDice(SCREEN, self.player)
            self.player.startTime()

        self.player = self.players[self.currentPlayer]
        self.player.updateTime()

        if self.player.steps == 0:
            soundHandler.playSound('next_player')
            pg.display.update()
            while pg.mixer.get_busy():
                pass
            pg.display.update()

            self.currentPlayer = self.currentPlayer + 1
            if self.currentPlayer >= len(self.players):
                self.currentPlayer = 0

            self.player = self.players[self.currentPlayer]
            self.player.startTime()
            if self.player.steps == 0:
                self.player.blit(SCREEN)
                self.drawCurrentPlayer(SCREEN)
                self.player.steps = self.dice.rollDice(SCREEN, self.player)

            pg.event.clear()


    def run(self, SCREEN):
        isFinished = False

        #print('before main loop board.run()')
        while not isFinished:
            #print('before drawBoard()')
            self.drawBoard(SCREEN)
            #print('after drawBoard()')
            for p in self.players:
                if p.show:
                    p.blit(SCREEN)

            self.selectPlayer(SCREEN)

            #print('before player blit()')
            self.player.blit(SCREEN)

            playerX = self.player.x
            playerY = self.player.y

            for event in pg.event.get():
                self.selectPlayer(SCREEN)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        if self.player.y > 0 and not self.maze.checkWallCollision(self.player, 0, -1):
                            self.player.setPosition(self.player.x,  self.player.y - 1)
                        else:
                            soundHandler.playSound('error-beep')
                    elif event.key == pg.K_DOWN:
                        if self.player.y < (GRID_HEIGHT - 1) and not self.maze.checkWallCollision(self.player, 0, 1):
                            self.player.setPosition(self.player.x,  self.player.y + 1)
                        else:
                            soundHandler.playSound('error-beep')
                    elif event.key == pg.K_LEFT:
                        if self.player.x > 0 and not self.maze.checkWallCollision(self.player, -1, 0):
                            self.player.setPosition(self.player.x - 1,  self.player.y)
                        else:
                            soundHandler.playSound('error-beep')
                    elif event.key == pg.K_RIGHT:
                        if self.player.x < GRID_WIDTH and not self.maze.checkWallCollision(self.player, 1, 0):
                            self.player.setPosition(self.player.x + 1, self.player.y)
                        else:
                            soundHandler.playSound('error-beep')
                # if moved
                if playerX != self.player.x or playerY != self.player.y:
                    soundHandler.playSound('footstep')
                    self.player.blit(SCREEN)
                    pg.display.update()
                    while pg.mixer.get_busy():
                        pass
                    pg.display.update()

                    if self.player.steps > 0:
                        self.player.steps = self.player.steps - 1
                        self.player.score = self.player.score + 1

                    if self.player.x == self.finishPoint.X and self.player.y == self.finishPoint.Y:
                        self.player.updateTime()
                        isFinished = True
                        finishScreen = finish.Finish()
                        finishScreen.run(SCREEN,self. player)

                    # if question below player
                    question = self.getQuestion(self.player.x, self.player.y)
                    if question:
                        ret = question.draw(SCREEN)
                        # if answer is correct player.steps += 2
                        if ret == True:
                            # play success sound
                            soundHandler.playSound('collect')
                            self.player.steps = self.player.steps + 2
                            self.player.score = self.player.score + 3
                            self.messageBoxWin.draw(SCREEN, 'TAČNO!\nDobijaš 2 poena i\n2 dodatna koraka', (200, 0, 0), 20)

                        else:
                            soundHandler.playSound('wrong')
                            self.messageBoxWin.draw(SCREEN, 'NETAČNO!\nGubiš korake i\nnastavlja sledeći igrač', (200, 0, 0), 20)
                            #time.sleep(0.5)
                            self.player.steps = 0
                            pg.event.clear()

            #print('before display update in board.run()')
            pg.display.update()
