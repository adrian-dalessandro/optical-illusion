import pygame
from pygame.math import Vector2 as vec

class Physics(object):
    def __init__(self, gravity, friction):
        self.gravity = gravity
        self.friction = friction

class World(object):
    def __init__(self, window, physics):
        self.window = window
        self.width = window.get_width()
        self.height = window.get_height()
        self.physics = physics
        self.start = vec(0, self.height)
