import pygame
from pygame.math import Vector2 as vec
import random
from math import radians, cos, sin

LEFT = -1
RIGHT = 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, theta, x, y, velocity, frames):
        super(Bullet, self).__init__()
        self.vel = velocity
        self.direction = direction
        self.theta = theta
        self.count = 0
        self.frames = frames
        self.current_frame = 0
        self.image, self.rect = self.transform(frames[self.current_frame], x, y)
        self.image.set_colorkey((0,0,0))


    def update(self):
        self.rect.centery -= self.vel.y
        self.rect.centerx += self.vel.x
        self.count += 1
        if self.count%2 == 0:
            self.animate()

    def transform(self, image, x, y):
        height = image.get_height()
        width = image.get_width()
        if self.direction == LEFT:
            image =  pygame.transform.flip(image, True, False)
        image = pygame.transform.rotate(image, self.direction*self.theta)
        rect = image.get_rect()
        rect.centery = y - sin(radians(self.theta))*height//2
        rect.centerx = x + self.direction*cos(radians(self.theta))*width//2
        return image, rect

    def animate(self):
        self.current_frame = (self.current_frame + 1)%len(self.frames)
        new_frame = self.frames[self.current_frame]
        new_rect = new_frame.get_rect()
        if self.direction == LEFT:
            new_frame =  pygame.transform.flip(new_frame, True, False)
        new_rect.centery = self.rect.centery
        new_rect.centerx = self.rect.centerx
        self.image = new_frame
        self.rect = new_rect
        self.image.set_colorkey((0,0,0))

    def overwrite_velocity(self, magnitude):
        v_x = self.direction*cos(radians(self.theta))*magnitude
        v_y = sin(radians(self.theta))*magnitude
        self.vel = vec(v_x, v_y)

    def overwrite(self, direction, theta, x, y, velocity, frames):
        self.vel = velocity
        self.direction = direction
        self.theta = theta
        self.frames = frames
        self.image, self.rect = self.transform(frames[self.current_frame], x, y)
        self.image.set_colorkey((0,0,0))




class PrototypeGun(object):
    """------------+
    | PrototypeGun |--> This class is the basic prototype for a gun. All guns should be an extension of this class.
    +--------------+"""
    def __init__(self, spritesheet):
        # instantiate object
        self.spritesheet = spritesheet

    def check_cooldown(self) -> bool:
        # if cooldown is greater than 0, return True to indicate that the gun is in cooldown mode
        raise NotImplementedError('subclasses must override check_cooldown()!')

    def update(self, direction, theta, x, y): #
        pass

    def release(self):
        # when player releases weapon trigger, run this script
        pass # do nothing by default

    def shoot(self, direction, theta, x, y) -> Bullet:
        # if player clicks weapon trigger, run this script
        raise NotImplementedError('subclasses must override shoot()!')

"""-----------------+
| ALL CUSTOM GUNS   |
| DEFINED BELOW     |
+-------------------+
|    |    |    |    |
V    V    V    V    V
"""

class ChargeGun(PrototypeGun):
    """---------+
    | ChargeGun |--> this gun spawns a bullet when player clicks weapon trigger, and fires the bullet when
    +-----------+    the player releases the weapons trigger. The bullet grows in size and power the longer
                     the player holds down the weapon trigger; up to a maximum size."""
    def __init__(self, spritesheet):
        super(ChargeGun, self).__init__(spritesheet)
        self.is_charging = False
        self.charge = 1
        self.max_size = 100
        self.unit_size = 10
        self.cooldown = 0
        self.spritesheet = spritesheet
        self.charge_frames = spritesheet.get_images("static", self.unit_size)
        self.fly_frames = spritesheet.get_images("motion", self.unit_size)
        self.bullets = pygame.sprite.Group()

    def check_cooldown(self):
        # Set cooldown after bullet is released
        return self.cooldown > 0

    def release(self):
        # Update Bullet properties before releasing it to the world
        for bullet in self.bullets:
            bullet.overwrite_velocity(15)
            bullet.frames = self.spritesheet.get_images("motion", min(self.max_size, self.charge*self.unit_size))
        # remove reference in group, so that call to update no longer
        self.bullets.empty()
        self.is_charging = False
        self.charge = 1
        # set cooldown
        self.cooldown = 3

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def update_bullets(self, direction, theta, x, y):
        # If player moves while charging, update the charing bullet to reflex new coordinates
        self.charge += 1
        for bullet in self.bullets:
            bullet.overwrite(direction, theta, x, y, vec(0,0), self.spritesheet.get_images("static", min(self.max_size, self.charge*self.unit_size)))

    def shoot(self, direction, theta, x, y):
        # Spawn a new bullet
        self.is_charging = True
        bullet = Bullet(direction, theta, x, y, vec(0,0), self.spritesheet.get_images("static", self.charge*self.unit_size))
        self.bullets.add(bullet)
        return bullet
