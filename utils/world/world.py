import pygame
from pygame.math import Vector2 as vec
from utils.world.platform import Platform

class LevelBuilder(object):
    def __init__(self, wfname, world):
        world = world
        with open(wfname, "r") as f:
            file = f.read()
        lines = file.split("\n")
        header = self._parse_header(lines)
        theme = self._parse_theme(lines)
        level = self._parse_level(lines)
        self.build(header, theme, level, world)
        height = len(level)*header["unit"]
        width = len(level[0])*header["unit"]
        self.height = height
        self.width = width

    def shape(self):
        return self.height, self.width

    def build(self, header, theme, level, world):
        unit = header["unit"]
        for i, row in enumerate(level):
            for j, block in enumerate(row):
                if block == '.':
                    continue
                elif block in '#_':
                    world.platform_factory(j*50, i*50, unit, theme[block])
                elif block in '[-]':
                    world.platform_factory(j*50, i*50, unit, theme[block])
                elif block == 'x':
                    world.start = vec(j*50, i*50)

    def _parse_level(self, lines):
        level = []
        start = False
        for line in lines:
            if start:
                row = list(line)
                if len(row) > 0:
                    level.append(row)
            if line == "t>":
                start = True
        return level

    def _parse_header(self, lines):
        header = {}
        for line in lines[0:5]:
            key = line.split(":")[0].strip(" ").lower()
            val = line.split(":")[1].strip(" ")
            if val.isnumeric():
                val = int(val)
            header[key] = val
        return header

    def _parse_theme(self, lines):
        theme = {}
        start = False
        for line in lines:
            if line == "t>":
                break
            if start:
                key = line.split("=")[0].strip(" ")
                val = line.split("=")[1].strip(" ")
                theme[key] = val
            if line == "<t":
                start = True
        return theme

class Physics(object):
    def __init__(self, gravity, friction):
        self.gravity = gravity
        self.friction = friction


class World(object):
    def __init__(self, window, physics, spritesheets, background):
        self.window = window
        self.background = background
        self.width = window.get_width()
        self.height = window.get_height()
        self.spritesheets = spritesheets
        self.physics = physics
        self.start = vec(0, 0)
        self.groups = {"platforms": pygame.sprite.Group(),
                       "enemies": pygame.sprite.Group(),
                       "bullets": pygame.sprite.Group()}
        self.all_platforms = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()

    def add_to_group(self, sprite, name):
        self.groups[name].add(sprite)

    def get_group_list(self):
        return list(self.groups.values())

    def platform_factory(self, x, y, hscale, style):
        plat = Platform(x, y, hscale, self, style)
        self.all_platforms.add(plat)

    def bullet_factory(self, gun, direction, x, y):
        if gun.check_cooldown():
            pass
        else:
            self.all_bullets.add(gun.fire(direction, x, y))
