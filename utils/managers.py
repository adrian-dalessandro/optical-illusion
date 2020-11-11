import pygame

def updateWorld(world, group):
    world.window.blit(world.background, [0, 0])
    group.draw(world.window)
    world.all_platforms.draw(world.window)
    pygame.display.update()

class GameManager(object):
    def __init__(self, width, height, name):
        self.state = True
        pygame.init()
        self.win = pygame.display.set_mode((width,height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

    def parse(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state = False
