import pygame
from pygame.math import Vector2 as vec


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, hscale, world, style):
        super(Platform, self).__init__()
        self.world = world
        self.image = self.world.spritesheet.get_image(style, hscale)
        self.image.set_colorkey((0,255,0))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = vec(x,y)
