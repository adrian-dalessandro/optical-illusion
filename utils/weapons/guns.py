import pygame
from pygame.math import Vector2 as vec
import random
from math import radians, cos, sin

LEFT = -1
RIGHT = 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, theta, x, y, velocity, angle, distance, frames):
        super(Bullet, self).__init__()
        self.vel = velocity
        self.direction = direction
        self.angle = angle
        self.distance = distance
        self.pos = vec(x, y)
        self.count = 0
        self.frames = frames
        self.current_frame = random.randint(0, len(frames)-2)
        self.image = frames[self.current_frame]
        self.image.set_colorkey((0,0,0))
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        if direction == LEFT:
            self.image =  pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.rotate(self.image, direction*theta)
        self.rect = self.image.get_rect()
        self.rect.centery = y - sin(radians(theta))*self.height//2
        self.rect.centerx = x + direction*cos(radians(theta))*self.width//2


    def update(self):
        self.pos += self.vel
        self.count += 1


        if self.count > self.distance:
            self.kill()

    def animate(self):
        pass

"""
Gun logic:
    - If fire has already been hit,
"""

class DefaultGun(object):
    def __init__(self):
        #self.statistics = {
        #        "firerate": 4,
        #        "velocity": Vec(0,0),
        #        "spread" : 1,
        #        "angle" : Vec(0,0)}
        self.firerate = 4 #per second
        self.cooldown = 0

    def check_cooldown(self):
        return self.cooldown > 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def animate(self):
        pass

    def fire(self, direction, theta, x, y):
        self.cooldown = self.firerate
        return Bullet(direction, theta, x, y)

# TODO
# Gun needs to store references to

class FireGun(DefaultGun):
    def __init__(self, spritesheet):
        super(FireGun, self).__init__()
        self.firerate = 2
        self.cooldown = 0
        self.frames = spritesheet.get_images(100)
        self.bullet = None

    def fire(self, direction, theta, x, y):
        self.cooldown = self.firerate
        return Bullet(direction, theta, x, y, vec(0,0), vec(0,0), 2, self.frames)

class MultiGun(DefaultGun):
    def __init__(self):
        pass
