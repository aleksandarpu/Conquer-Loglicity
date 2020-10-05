import pygame as pg
import random
from Question import Question
from common import getLine

class Questions():
    """
    Load question collections into dict
    """
    def __init__(self):
        # map the char from question txt file (question header line) into the dictionary key
        self.type2key = {'5' : 'math', 'L' : 'lang', 'A' : 'assoc', 'Z' : 'star'}
        self.qDict = {'math' : [], 'lang' : [],'star' : [], 'assoc' : []}

    def getQuestion(self, type : str) -> Question:
        """
        Get random question from selected questions list
        :param type: question group (dictionary key)
        :return: Question object or None on error
        """
        q1 = self.qDict[type]
        if len(q1) > 1:
            rn = random.randrange(len(q1))
            while rn == self.lastQuestions[type]:
                rn = random.randrange(len(q1))
        else:
            rn = 0

        ####rn = 0
        #   show question
        if rn < len(q1):
            question = q1[rn]
            self.lastQuestions[type] = rn
            return question
        else:
            return None

    def loadQuestions(self, fNames : list):
        for fn in fNames:
            self._loadQuestions(fn)

        self.lastQuestions = dict()
        for k,v in self.qDict.items():
            self.lastQuestions[k] = -1
            print('{} has {} questions'.format(k, len(v)))

    def _loadQuestions(self, fName : str):
        """
         format in file:
         T is type: 5-math, L-language, Z - star, A - associations
         QT:valid_answer:image_path
         question text line 1
         question text line 2
         ...
         question text line n
         A1:answer text 1
         A2:answer text 1
         A3:answer text 1
         A4:answer text 1
        """
        with open(fName, 'r', encoding="utf8") as f:
            line = getLine(f)
            while line:
                if len(line) == 0:
                    continue
                # find question header line
                while line[0] != 'Q':
                    line = getLine(f)
                # read question header
                while line[0] != 'Q':
                    line = getLine(f)

                newQuestion = Question()
                newQuestion.readQuestion(line, f)
                if newQuestion.valid and newQuestion.type is not None:
                    self.appendQuestion(newQuestion.type, newQuestion)

                line = getLine(f)

    def appendQuestion(self, type: str, question : Question):
        if type in self.type2key.keys():
            self.qDict[self.type2key[type]].append(question)
        else:
            print("Unknown type '{}'".format(type))
