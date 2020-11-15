from utils.world.platform import Platform
import pygame
from pygame.math import Vector2 as vec

class Level(object):
    def __init__(self, wfname, spritesheet):
        with open(wfname, "r") as f:
            file = f.read()
        lines = file.split("\n")
        header = self._parse_header(lines)
        theme = self._parse_theme(lines)
        level = self._parse_level(lines)
        height = len(level)*header["unit"]
        width = len(level[0])*header["unit"]
        self.spritesheet = spritesheet
        self.height = height
        self.width = width
        self.start = None
        self.groups = {"platforms": pygame.sprite.Group()}
        self.build(header, theme, level)

    def build(self, header, theme, level):
        unit = header["unit"]
        for i, row in enumerate(level):
            for j, block in enumerate(row):
                if block == '.':
                    continue
                elif block in '#_[-]':
                    self.groups["platforms"].add(Platform(j*50, i*50, unit, self.spritesheet, theme[block]))
                elif block == 'x':
                    self.start = vec(j*50, i*50)

    def get_start(self):
        return self.start

    def get_groups(self, name):
        return self.groups[name]

    def shape(self):
        return self.width, self.height

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
