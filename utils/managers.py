import pygame

def updateWorld(world, group, camera):
    world.window.blit(world.background, [0, 0])
    #world.all_platforms.draw(world.window)
    for platform in world.all_platforms:
        world.window.blit(platform.image, camera.apply(platform))
        #platform.draw(world.window)

    for sprite in group:
        world.window.blit(sprite.image, camera.apply(sprite))
    world.all_bullets.update()
    for bullet in world.all_bullets:
        world.window.blit(bullet.image, camera.apply(bullet))


    pygame.display.update()

class GameManager(object):
    def __init__(self, width, height, name):
        self.state = True
        pygame.init()
        self.win = pygame.display.set_mode((width,height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

    def get_window(self):
        return self.win

    def parse(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state = False

    def game_loop(self, world, camera):
        world.window.blit(world.background, [0, 0])
        for group in world.groups.values():
            for sprite in group:
                world.window.blit(sprite.image, camera.apply(sprite))
        pygame.display.update()
