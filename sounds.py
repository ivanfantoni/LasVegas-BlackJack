import pygame
from pygame import mixer

class Mixer:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def load(self, file):
        pygame.mixer.Sound(file).play()

class BlackJack_Sounds:

    def __init__(self):
        self.m = Mixer()

    def s_blackjack(self):
        self.m.load('snds/blackjack.wav')

    def s_win(self):
        self.m.load('snds/win.wav')

    def s_loose(self):
        self.m.load('snds/loose.wav')

    def s_option(self):
        self.m.load('snds/option.wav')

    def s_ins_split(self):
        self.m.load('snds/ins_split.wav')

    def s_chips(self):
        self.m.load('snds/chips.wav')

    def s_card(self):
        self.m.load('snds/card.wav')

    def s_welcome(self):
        self.m.load('snds/welcome.wav')

    def s_alert(self):
        self.m.load('snds/alert.wav')

    def s_tie(self):
        self.m.load('snds/tie.wav')
