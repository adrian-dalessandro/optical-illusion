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

class DirtyAnimation(object):
    def __init__(self, scale, spf, src_dir):
        self.counter = 0
        self.switch = 0
        self.spf = spf
        self.sprite_dict = {"standing": [], "jumping": []}
        for f in ["standing0.png", "standing1.png", "standing2.png", "standing3.png"]:
            image = pygame.image.load(src_dir + "/" + f).convert()
            image = pygame.transform.scale(image, (scale, scale))
            image.set_colorkey((0,0,0))
            self.sprite_dict["standing"].append(image)

        for f in ["jumping0.png"]:
            image = pygame.image.load(src_dir + "/" + f).convert()
            image = pygame.transform.scale(image, (scale, scale))
            image.set_colorkey((0,0,0))
            self.sprite_dict["jumping"].append(image)

    def next_frame(self, state, facing):
        sprite = self.sprite_dict[state]
        self.switch = (self.switch + 1) % self.spf
        if self.switch == 0:
            self.counter += 1
        self.counter = self.counter % len(sprite)
        image = sprite[self.counter]
        if facing == LEFT:
            image = pygame.transform.flip(image, True, False)
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, world, spritesheet, default_gun):
        super(Player, self).__init__()
        self.world = world
        self.states = {"running": False, "crouching": False,
                        "jumping": False, "doublejumping": False, "shooting": False, "trigger": False,
                        "isFacing": RIGHT, "imgFacing": RIGHT}
        self.attribs = {"jump": -15, "speed": 10}
        self.animation = DirtyAnimation(64, 4, "./assets/layouts/AdriansCustomGraphics/sprites/player1")
        self.image = self.animation.next_frame("standing", RIGHT)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = vec(world.start.x, world.start.y)
        self.vel = vec(0,0)
        self.active_gun = default_gun

    def jump(self):
        self.vel.y = self.attribs["jump"]
        self.states["jumping"] = True

    def double_jump(self):
        self.vel.y = self.attribs["jump"]
        self.states["doublejumping"] = True

    def aiming(self, keys):
        theta_matrix = [[0,  0], [90, 45]]
        theta = theta_matrix[keys[MV_UP] or keys[CROUCH]][keys[MV_LEFT] or keys[MV_RIGHT]]
        if keys[CROUCH]:
            theta = -theta
        x = cos(radians(theta))*self.image.get_width()//2
        y = sin(radians(theta))*self.image.get_height()
        if self.states["isFacing"] == LEFT:
            x = self.rect.centerx - x
        elif self.states["isFacing"] == RIGHT:
            x = self.rect.centerx + x
        y = self.rect.centery - y
        return theta, x, y

    def resolve_actions(self, keys):
        # Shooting Action
        if keys[SHOOT]:
            if not self.active_gun.check_cooldown():
                if not self.states["trigger"]:
                    self.states["trigger"] = True
                    self.active_gun.press_trigger(self.states["isFacing"], *self.aiming(keys))
                else:
                    self.active_gun.hold_trigger(self.states["isFacing"], *self.aiming(keys))
        else:
            if self.states["trigger"]:
                self.active_gun.release_trigger()
                self.states["trigger"] = False

    def resolve_collisions(self):
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.world.get_group("platforms"), False)
            if hits:
                for hit in hits:
                    if self.rect.centerx >= hit.rect.left and self.rect.centerx <= hit.rect.right:
                        if self.rect.bottom >= hit.rect.top and self.rect.centery <  hit.rect.top:
                            self.rect.bottom = hit.rect.top
                            self.vel.y = 0
                            self.states["doublejumping"] = False
                            self.states["jumping"] = False

    def resolve_motions(self, keys):
        """
        The method is for calculating the current player velocity in the
        x and y direction.
        """
        # Resolve x velocity (i.e. running)
        if not self.states["jumping"]:
            # Verify player is not jumping, and calculate movement
            direction = LEFT*keys[MV_LEFT] + RIGHT*keys[MV_RIGHT] # sets direction to either right or left

            if abs(direction) > 0:
                self.vel.x = self.attribs["speed"]*direction
                self.states["isFacing"] = direction
            else:
                self.vel.x = 0 # if no movement keys pressed, stop x motion
        # Resolve y velocity (i.e. jumping and failling)
        if keys[JUMP] and not self.states["jumping"]:
            self.jump()
        elif keys[JUMP] and not self.states["doublejumping"] and self.vel.y > 0:
            self.double_jump()
        self.vel += vec(0, self.world.physics.gravity)

    def animate(self):
        if self.states["jumping"] == True:
            new_image = self.animation.next_frame("jumping", self.states["isFacing"])
        else:
            new_image = self.animation.next_frame("standing", self.states["isFacing"])
        new_rect = new_image.get_rect()
        new_rect.centery = self.rect.centery
        new_rect.centerx = self.rect.centerx
        self.image = new_image
        self.rect = new_rect

    def update(self):
        keys = pygame.key.get_pressed()
        self.resolve_motions(keys)
        self.rect.center += self.vel
        self.resolve_collisions()
        self.active_gun.update()
        self.resolve_actions(keys)
        self.animate()
