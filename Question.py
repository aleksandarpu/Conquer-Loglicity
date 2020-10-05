import pygame as pg
import sys, time, random
from colors import questionColor, answerColor,answerArrowColor, WHITE, GREEN
from text_font import load_font, drawText
from config import errSound1
from common import getLine

class Question():
    def __init__(self):

        OFFSET_INNER_VIEW = -4
        MAIN_VIEW_OFFSET_X = -100
        MAIN_VIEW_OFFSET_Y = -30
        VERICAL_IMAGE_QUESTION_SPACE = 350
        HORIZONTAL_IMAGE_QUESTION_SPACE = 200

        self.type = None
        self.text = '???'
        self.imageFile = None
        self.image = None
        # dummy 4 answers
        self.answers = ['1', '2', '3', '4']
        self.valid = 1
        self.answer = 0
        self.bgColor = pg.Color('darkgreen')
        self.questionColor = questionColor
        self.answerColor = answerColor
        self.arrowColor = answerArrowColor
        self.drawArrow()
        self.borderColor = (200, 0, 0)

        scrRect = pg.display.get_surface().get_rect()

        # question window
        self.viewRect = scrRect.inflate(MAIN_VIEW_OFFSET_X, MAIN_VIEW_OFFSET_Y)
        self.viewInnerRect = self.viewRect.inflate(OFFSET_INNER_VIEW, OFFSET_INNER_VIEW)

        # positions and dimensions for vertical image width < height
        self.imageRectV = self.viewInnerRect.copy()
        self.imageRectV.width = self.imageRectV.width - VERICAL_IMAGE_QUESTION_SPACE

        self.questionTextRectV = self.viewInnerRect.copy()
        self.questionTextRectV.x = self.questionTextRectV.x + self.imageRectV.width
        self.questionTextRectV.width = VERICAL_IMAGE_QUESTION_SPACE
        self.answerRectV = self.questionTextRectV.copy()

        # positions and dimensions for horizontal image width > height
        self.questionTextRectH = self.viewInnerRect.copy()
        self.questionTextRectH.height = 200

        self.imageRectH = self.viewInnerRect.copy()
        self.imageRectH.width = self.imageRectH.width - HORIZONTAL_IMAGE_QUESTION_SPACE

        self.answerRectH = self.viewInnerRect.copy()
        self.answerRectH.x = self.answerRectH.x + self.imageRectH.width
        self.answerRectH.width = HORIZONTAL_IMAGE_QUESTION_SPACE

        self.timerFnt = load_font('freesans', 24)
        self.timerImg = self.timerFnt.render('00:00', 1, (100,100,100))
        self.timerRect = self.timerImg.get_rect()
        self.timerRect.inflate_ip(5, 5)
        self.timerRect.move(-2, -2)
        self.countdown = 30
        self.timerStart = time.time()

    def readQuestion(self, line : str, f ):
        """
        read question data from file
        line is first line already loaded in form Qx:a:fname
        x is question group, a is correct answer, fname is optional image path
        :param line: string
        :param f: file
        :return: nothing
        """
        qitems = line.split(':')

        self.type = qitems[0][1]
        self.answer = int(qitems[1]) - 1
        # read optional image path
        if len(qitems) > 2:
            x = qitems[2].strip().strip("'")
            self.imageFile = x
            #self.image = pg.image.load(x).convert_alpha()
        else:
            self.image = None
        # read question text
        l1 = []
        line = f.readline(100)
        while not line.startswith('A1:'):
            l1.append(line)
            line = getLine(f)
        qText = ''.join(l1)
        self.text = qText.strip()

        # read answers - can be one line only
        self.answers[0] = line[3:].strip()
        line = getLine(f)
        while not line.startswith('A2:'):
            line = getLine(f)
        self.answers[1] = line[3:].strip()
        line = getLine(f)
        while not line.startswith('A3:'):
            line = getLine(f)
        self.answers[2] = line[3:].strip()
        line = getLine(f)
        while not line.startswith('A4:'):
            line = getLine(f)
        self.answers[3] = line[3:].strip()

        self.valid = True
        self.text = qText

    def drawQuestionText(self, scr : pg.Surface, r : pg.Rect):

        #with open('test.txt', 'r', encoding="utf8") as f:
        #    msg = f.readline(100)
        #msg = 'Ide macka oko tebe\npazi da te ne ogrebe.\nCuvaj misu rep nemoj biti slep'
        msg = self.text
        #msg = u'Zaključi koliko iznosi ringišpil?'

        return drawText(scr, msg, self.questionColor, r, 'arial', 32, True)

    def drawArrow(self):
        self.arrowImage = pg.Surface([30, 30])
        self.arrowImage.fill(self.bgColor)
        pg.draw.polygon(self.arrowImage, self.arrowColor,
                        ((0, 10), (0, 20), (20, 20), (20, 30), (30, 15), (20, 0), (20, 10)))

    def shuffleAnswers(self):
        self.rndAnswers = self.answers.copy()
        self.rndAnswer = 0
        random.shuffle(self.rndAnswers)
        for i  in range(len(self.rndAnswers)):
            if self.answers[self.answer] == self.rndAnswers[i]:
                self.rndAnswer = i
                return

    def drawAnswers(self, scr : pg.Surface, r : pg.Rect, ans : int):
        offsetX = r.x + 40
        offsetY = r.y + 15
        rowHeigth = 40
        pg.draw.rect(scr, self.bgColor, r)
        for i in range(4):
            msg = "{})  {}".format(chr(ord('A') + i), self.rndAnswers[i])
            rect1 = pg.Rect(offsetX, i * rowHeigth + offsetY, scr.get_width() - offsetX, scr.get_height())
            drawText(scr, msg, self.answerColor, rect1, 'freesans', 26, True)
            if i == ans:
                scr.blit(self.arrowImage, (r.x + 5, r.y + 8 + i * rowHeigth))

    def drawImage(self, scr : pg.Surface, r : pg.Rect):
        w = r.width
        h = r.height
        sc1 = self.image.get_width() / w
        sc2 = self.image.get_height() / h
        offsetX = 0
        if sc1 > sc2:
            imgW = w
            imgH = int(self.image.get_height() / sc1)
        else:
            imgW = int(self.image.get_width() / sc2)
            imgH = h
        pic = pg.transform.scale(self.image, (imgW, imgH))
        x1 = int((w - pic.get_width()) / 2)
        y1 = int((h - pic.get_height()) / 2)
        offsetX = r.x + x1
        offsetY = r.y + y1
        scr.blit(pic, (offsetX, offsetY))

    def _drawV(self, scr: pg.Surface):
        pg.draw.rect(scr, (200, 0, 0), self.viewRect, 2)

        self.drawImage(scr, self.imageRectV)

        h1 = self.drawQuestionText(scr, self.questionTextRectV)
        r = self.answerRectV.copy()
        r.y = r.y + h1
        r.height = r.height - h1

        ans = 0
        self.shuffleAnswers()
        self.drawAnswers(scr, r, ans)

        pg.display.update()

        return self.run(scr, r, ans)

    def _drawH(self, scr: pg.Surface):
        pg.draw.rect(scr, (200,0,0), self.viewRect, 2)

        h1 = self.drawQuestionText(scr, self.questionTextRectH)
        r = self.imageRectH.copy()
        r.y = r.y + h1
        r.height = r.height - h1
        self.drawImage(scr, r)

        ans = 0
        self.shuffleAnswers()
        self.drawAnswers(scr, self.answerRectH, ans)

        pg.display.update()

        return self.run(scr, self.answerRectH, ans)

        pg.display.update()
        time.sleep(100)

    def drawNoImage(self, scr: pg.Surface):
        qrect = self.viewInnerRect.copy()
        qrect.x = qrect.x + 10
        qrect.y = qrect.y + 5
        qrect.width = qrect.width - 20
        qrect.height = qrect.height - 20

        h = self.drawQuestionText(scr, qrect)
        arect = qrect.copy()
        arect.y = arect.y + h + 5
        arect.height = arect.height - h - 5
        ans = 0
        self.shuffleAnswers()
        self.drawAnswers(scr, arect, ans)

        pg.display.update()

        return self.run(scr, arect, ans)

    def drawTimer(self, scr: pg.Surface):
        r = self.timerRect
        r.x = self.viewRect.x + self.viewRect.width - self.timerRect.width - 2
        r.y = self.viewRect.y + self.viewRect.height - self.timerRect.height - 2
        bg = scr.subsurface(r.x,r.y,r.width,r.height)
        delta = self.countdown - (time.time() - self.timerStart)
        min = int(delta // 60)
        sec = int(delta) - min * 60
        timestr = '{:02d}:{:02d}'.format(min, sec)
        if delta > 10:
            clr = (0,0,0)
        else:
            clr=(200, 0,0)
        img = self.timerFnt.render(timestr, 1, clr)
        pg.draw.rect(scr, self.bgColor, r)
        #pg.draw.rect(scr, (200, 10, 10), r)
        scr.blit(img, self.timerRect)


    def draw(self, scr: pg.Surface):
        if self.imageFile:
            # lazy load
            if self.image is None:
                self.image = pg.image.load(self.imageFile).convert_alpha()
        pg.draw.rect(scr, self.borderColor, self.viewRect, 2)
        pg.draw.rect(scr, self.bgColor, self.viewInnerRect)
        self.shuffleAnswers()
        if self.image is None:
            return self.drawNoImage(scr)
        if self.image.get_width() < self.image.get_height():
            return self._drawV(scr)
        else:
            return self._drawH(scr)


    def run(self, scr : pg.Surface, aRect : pg.Rect, ans : int):
        doReturn = False;
        pg.event.clear()
        self.countdown = 30
        self.timerStart = time.time()
        while True:
            if doReturn:
                self.drawAnswers(scr, aRect, ans)
                pg.display.update()
                time.sleep(0.2)
                pg.event.clear()
                return ans == self.rndAnswer

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        return ans == self.rndAnswer

                    if event.key == pg.K_DOWN:
                        if ans < 3:
                            ans = ans + 1
                        else:
                            errSound1.play()

                    if event.key == pg.K_UP:
                        if ans > 0:
                            ans = ans - 1
                        else:
                            errSound1.play()

                    if event.key == pg.K_a:
                        ans = 0
                        doReturn = True
                    elif event.key == pg.K_b:
                        ans = 1
                        doReturn = True
                    elif event.key == pg.K_c:
                        ans = 2
                        doReturn = True
                    elif event.key == pg.K_d:
                        ans = 3
                        doReturn = True

            self.drawAnswers(scr, aRect, ans)
            self.drawTimer(scr)
            if time.time() - self.timerStart > self.countdown:
                pg.display.update()
                return False

            pg.display.update()


if __name__ == '__main__':

    q = Question()
    f = open('questions-asoc.txt', 'r', encoding="utf8")
    line = getLine(f)
    q.readQuestion(line, f)
    if q.type is not None:
        SCREEN = pg.display.set_mode((1000, 600))
        pg.display.set_caption('Question test')
        a = q.draw(SCREEN)
        time.sleep(10)
