import pygame
from pygame.math import Vector2 as vec

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, x, y):
        super(Bullet, self).__init__()
        self.vel = vec(direction*20,0)
        self.direction = direction
        self.radius = 10
        self.pos = vec(x, y)
        self.count = 0

    def update(self):
        self.pos += self.vel
        self.count += 1
        if self.count > 20:
            self.kill()

    def draw(self, win):
        pygame.draw.circle(win, (244,50,0), (self.pos.x,self.pos.y), self.radius)
        pygame.draw.circle(win, (100,0,100), (self.pos.x + self.direction*1.2, self.pos.y), int(self.radius - self.radius/4))

class Gun(object):
    def __init__(self):
        self.firerate = 4 #per second
        self.cooldown = 0

    def check_cooldown(self):
        return self.cooldown > 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def fire(self, direction, x, y):
        self.cooldown = self.firerate
        return Bullet(direction, x, y)
