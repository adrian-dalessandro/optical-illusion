import pygame
from pygame.math import Vector2 as vec

LEFT = -1
RIGHT = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, world, default_gun):
        super(Player, self).__init__()
        self.world = world
        self.image = self.world.spritesheets["player"].get_image("p1_stand", 50)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(world.start.x, world.start.y)
        self.isJumping = 0
        self.isFacing = RIGHT
        self.imgFacing = RIGHT
        self.active_gun = default_gun # todo

        self.rect.topleft = self.pos
        self.base_acc = 1
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        self.vel.y = -15
        self.isJumping = 1

    def move(self, direction):
        self.acc.x = direction*self.base_acc
        self.isFacing = direction

    def shoot(self):
        if self.isFacing == LEFT:
            self.world.bullet_factory(self.active_gun, self.isFacing, self.rect.left, self.rect.centery)
        elif self.isFacing == RIGHT:
            self.world.bullet_factory(self.active_gun, self.isFacing, self.rect.right, self.rect.centery)

    def update(self):
        # For each round, calculate applied forces and simulate acceleration
        self.acc = vec(0, self.world.physics.gravity)
        keys = pygame.key.get_pressed()

        self.active_gun.update()


        if keys[pygame.K_UP] and self.isJumping == 0:
            self.jump()
        elif self.isJumping == 0:
            if keys[pygame.K_LEFT]:
                self.move(LEFT)
            if keys[pygame.K_RIGHT]:
                self.move(RIGHT)
            # apply coefficient of friction
            self.acc.x += self.vel.x * self.world.physics.friction
        #print(self.vel, end=",")
        self.vel += self.acc
        #print(self.vel, end=",")
        self.pos += self.vel + 0.5*self.acc
        if self.pos.x > self.world.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.world.width

        self.rect.bottomleft = self.pos
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.world.all_platforms, False)
            #print(hits, end=",")
            if hits:
                if self.pos.y <= hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top
                    self.vel.y = 0
                    self.isJumping = 0
        #print(self.vel)
        self.rect.bottomleft = self.pos
        if self.isFacing != self.imgFacing:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgFacing = self.isFacing
        if keys[pygame.K_SPACE]:
            self.shoot()
