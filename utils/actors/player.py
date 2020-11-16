import pygame
from pygame.math import Vector2 as vec
from math import cos, sin, radians

LEFT = -1
RIGHT = 1
UP = 2
JUMP = pygame.K_z
MV_LEFT = pygame.K_LEFT
MV_RIGHT = pygame.K_RIGHT
MV_UP = pygame.K_UP
CROUCH = pygame.K_DOWN
SHOOT = pygame.K_SPACE

class Player(pygame.sprite.Sprite):
    def __init__(self, world, spritesheet):
        super(Player, self).__init__()
        self.world = world
        self.image = spritesheet.get_image("p1_stand", 50)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(world.start.x, world.start.y)
        self.isJumping = 0
        self.isFacing = RIGHT
        self.imgFacing = RIGHT
        self.isAiming = RIGHT
        self.trigger_pressed = False
        self.isUP = 1
        self.active_gun = None # todo

        self.rect.topleft = self.pos
        self.base_acc = 1
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def set_gun(self, gun):
        self.active_gun = gun

    def jump(self):
        self.vel.y = -15
        self.isJumping = 1

    def move(self, direction):
        self.acc.x = self.base_acc*direction//abs(direction)
        self.isFacing = direction//abs(direction)
        self.isUP = abs(direction)

    def animate(self):
        pass

    def release(self):
        self.active_gun.release()

    def shoot(self):
        keys = pygame.key.get_pressed()
        theta_matrix = [[0,  0], [90, 45]]
        if not self.active_gun.check_cooldown():
            theta = theta_matrix[keys[MV_UP] or keys[CROUCH]][keys[MV_LEFT] or keys[MV_RIGHT]]
            if keys[CROUCH]:
                theta = -theta
            x = cos(radians(theta))*self.image.get_width()//2
            y = sin(radians(theta))*self.image.get_height()

            if self.isFacing == LEFT:
                x = self.rect.centerx - x
            elif self.isFacing == RIGHT:
                x = self.rect.centerx + x
            y = self.rect.centery - y
            if self.trigger_pressed:
                self.active_gun.update_bullets(self.isFacing, theta, x, y)
            else:
                self.world.add_to_group(self.active_gun.shoot(self.isFacing, theta, x, y ), "bullets")

    def update(self):
        # For each round, calculate applied forces and simulate acceleration
        self.acc = vec(0, self.world.physics.gravity)
        keys = pygame.key.get_pressed()
        self.active_gun.update()



        if keys[JUMP] and self.isJumping == 0:
            self.jump()
        elif self.isJumping == 0:
            mvment = 0
            if keys[MV_LEFT]:
                mvment += LEFT
            if keys[MV_RIGHT]:
                mvment += RIGHT
            if keys[MV_UP]:
                mvment *= UP
            if mvment != 0:
                self.move(mvment)
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
            hits = pygame.sprite.spritecollide(self, self.world.get_group("platforms"), False)
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
        if keys[SHOOT]:
            self.shoot()
            self.trigger_pressed = True
        elif self.trigger_pressed and not keys[SHOOT]:
            self.trigger_pressed = False
            self.release()
