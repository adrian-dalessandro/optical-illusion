import pygame
from pygame.math import Vector2 as vec

LEFT = -1
RIGHT = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, world):
        super(Player, self).__init__()
        self.world = world
        self.image = pygame.Surface((50,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(world.start.x, world.start.y - 50)
        self.isJumping = 0

        self.rect.bottomleft = self.pos
        self.base_acc = 1
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        self.vel.y = -15
        self.isJumping = 1

    def move(self, direction):
        self.acc.x = direction*self.base_acc

    def update(self):
        # For each round, calculate applied forces and simulate acceleration
        self.acc = vec(0, self.world.physics.gravity)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.isJumping == 0:
            self.jump()
        elif self.isJumping == 0:
            if keys[pygame.K_LEFT]:
                self.move(LEFT)
            if keys[pygame.K_RIGHT]:
                self.move(RIGHT)
            # apply coefficient of friction
            self.acc.x += self.vel.x * self.world.physics.friction

        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        if self.pos.x > self.world.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.world.width

        self.rect.bottomleft = self.pos

        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.world.all_platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
                self.isJumping = 0
