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
        self.current_frame = 0
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
        self.rect.centery += self.vel.y
        self.rect.centerx += self.vel.x
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

# Bullet as 0 velocity and grows once K is pressed, continues to grow until K released
class ChargeGun(DefaultGun):
    def __init__(self, spritesheet):
        super(ChargeGun, self).__init__()
        self.charging = False
        self.charge = 0
        self.cool_down = 0
        self.max_charge = 5
        self.unit_size = 20
        self.bullets = pygame.sprite.Group()
        self.charge_frames = spritesheet.get_images("static", self.unit_size)
        self.fly_frames = spritesheet.get_images("motion", self.unit_size)


    def update(self):
        if not self.charging:
            if self.cooldown > 0:
                self.cooldown -= 1

    #def release(self):
    #    self.charging = False
    #    self.cool_down = 4
    #    for bullet in self.bullets:


    def fire(self, direction, theta, x, y):
        self.charging = True
        self.cool_down = 1
        bullet = Bullet(direction, theta, x, y, vec(0,0), vec(0,0), 2, self.frames)
        self.bullets.add(bullet)
        return bullet

class FireGun(DefaultGun):
    def __init__(self, spritesheet):
        super(FireGun, self).__init__()
        self.firerate = 2
        self.cooldown = 0
        self.count = 1
        self.spritesheet = spritesheet
        self.bullet = None

    def fire(self, direction, theta, x, y):
        self.frames = self.spritesheet.get_images("static", min(self.count*10,100))
        self.cooldown = self.firerate
        self.count += 1
        self.count = self.count%20
        return Bullet(direction, theta, x, y, vec(20,0), vec(0,0), 100, self.frames)

class MultiGun(DefaultGun):
    def __init__(self):
        pass
