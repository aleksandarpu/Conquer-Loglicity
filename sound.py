import pygame as pg

class SoundHandler:
    def __init__(self):
        self.sndFiles = { 'quit' : 'sounds/quit.wav',
                     'roll' : 'sounds/roll.wav',
                     'error-beep' : 'sounds/error-beep.wav',
                     'footstep' : 'sounds/footstep.wav',
                     'collect' : 'sounds/collect.wav',
                     'wrong' : 'sounds/wrongAnswer.wav',
                     'next_player' : 'sounds/changePlayer.wav',
                     'wall_hit' : 'sounds/wall_beep.wav',
                     'win' : 'sounds/winning.wav'}
        self.sndLoaded = dict()

    def loadSound(self, type : str) -> pg.mixer.Sound:
        if type in self.sndLoaded:
            return self.sndLoaded[type]

        if type in self.sndFiles:
            fname = self.sndFiles[type]
            snd = pg.mixer.Sound(fname)
            self.sndLoaded[type] = snd
            return snd
        return None

    def playSound(self, type: str):
        snd = self.loadSound(type)
        if snd is not None:
            snd.play()

    def playSoundAndHold(self, type: str):
        snd = self.loadSound(type)
        if snd is not None:
            snd.play()
            while pg.mixer.get_busy():
                pass



soundHandler = SoundHandler()
