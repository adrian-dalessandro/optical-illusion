import pygame
from pygame.math import Vector2 as vec
import random

LEFT = -1
RIGHT = 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, x, y, velocity, angle, distance, frames):
        super(Bullet, self).__init__()
        self.vel = velocity
        self.direction = direction
        self.angle = angle
        self.distance = distance
        self.pos = vec(x, y)
        self.count = 0
        self.frames = frames
        self.current_frame = random.randint(0, len(frames)-1)
        self.image = frames[self.current_frame]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        if direction == LEFT:
            self.rect.midright = self.pos
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.pos

    def update(self):
        self.pos += self.vel
        self.count += 1

        if self.count > self.distance:
            self.kill()




class DefaultGun(object):
    def __init__(self):
        self.firerate = 4 #per second
        self.cooldown = 0

    def check_cooldown(self):
        return self.cooldown > 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def animate(self):
        pass

    def fire(self, direction, x, y):
        self.cooldown = self.firerate
        return Bullet(direction, x, y)

# TODO
# Gun needs to store references to 

class FireGun(DefaultGun):
    def __init__(self, spritesheet):
        super(FireGun, self).__init__()
        self.firerate = 2
        self.cooldown = 0
        self.frames = spritesheet.get_images(100)
        self.bullet = None

    def fire(self, direction, x, y):
        self.cooldown = self.firerate
        return Bullet(direction, x, y, vec(0,0), vec(0,0), 2, self.frames)

class MultiGun(DefaultGun):
    def __init__(self):
        pass
