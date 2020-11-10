import pygame


class GameManager(object):
    def __init__(self):
        self.state = True

    def parse(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state = False
