import pygame
from pygame.math import Vector2 as vec
from utils.world.platform import Platform

class Physics(object):
    def __init__(self, gravity, friction):
        self.gravity = gravity
        self.friction = friction

class World(object):
    def __init__(self, window, camera, physics, level):
        self.window = window
        self.camera = camera
        self.physics = physics
        self.level = level
        self.background = None
        self.width, self.height = self.level.shape()
        self.start = self.level.start
        self.groups = {"platforms": self.level.groups["platforms"],
                       "enemies": pygame.sprite.Group(),
                       "bullets": pygame.sprite.Group(),
                       "players": pygame.sprite.Group()}


    def add_to_group(self, sprite, name):
        self.groups[name].add(sprite)

    def get_group(self, name):
        return self.groups[name]

    def set_background(self, fname):
        bk_image = pygame.image.load(fname).convert()
        bk_h = bk_image.get_height()
        bk_w = bk_image.get_width()
        scale = self.window.get_height()/bk_h
        self.background = pygame.transform.scale(bk_image, (int(scale*bk_h), int(scale*bk_w)))


    def update(self):
        for group in self.groups.values():
            for sprite in group:
                sprite.update()
