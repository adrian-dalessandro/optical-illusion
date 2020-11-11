import pygame
from pygame.math import Vector2 as vec
from utils.world.platform import Platform


class Physics(object):
    def __init__(self, gravity, friction):
        self.gravity = gravity
        self.friction = friction

class World(object):
    def __init__(self, window, physics, spritesheet, background):
        self.window = window
        self.background = background
        self.width = window.get_width()
        self.height = window.get_height()
        self.spritesheet = spritesheet
        self.physics = physics
        self.start = vec(0, self.height-50)
        self.all_platforms = pygame.sprite.Group()

    def platform_factory(self, x, y, hscale, style):
        plat = Platform(x, y, hscale, self, style)
        self.all_platforms.add(plat)
