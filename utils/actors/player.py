import pygame
from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    def __init__(self, world):
        super(Player, self).__init__()
        self.world = world
        self.image = pygame.Surface((50,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.world.start
        self.pos = self.world.start
        self.base_acc = 1
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def update(self):
        self.acc = vec(0, 0)#self.world.physics.gravity)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -self.base_acc
        if keys[pygame.K_RIGHT]:
            self.acc.x = self.base_acc

        self.acc.x += self.vel.x * self.world.physics.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        if self.pos.x > self.world.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.world.width

        self.rect.midbottom = self.pos
