from utils.world.world import World, Physics
from utils.world.levels import Level
from utils.world.camera import Camera
from utils.actors.player import Player
from utils.managers import GameManager
from utils.graphics.sheets import Spritesheet, HierarchySpritesheet
from utils.graphics.themes import Theme
from utils.weapons.guns2 import ChargeGun
import pygame
import json

win_width = 500
win_height = 600
FPS = 27
game_name = "Optical Illusion"
level_file = "./worlds/sandbox.world"
bkgr_fname = "./assets/layouts/kenney_backgroundElements/Samples/colored_talltrees.png"

gamemanager = GameManager(win_width, win_height, game_name)

# graphics
theme = Theme("./themes/Grass")
player_sheet = Spritesheet(theme.actorsheet.spritesheet, theme.actorsheet.dict)
level_sheet = Spritesheet(theme.tilesheet.spritesheet, theme.tilesheet.dict)
#fire_bullet_sheet = IconSheet("./assets/bullets/fire.png", json.load(open("./assets/bullets/fire.json")))
charge_bullet_sheet = HierarchySpritesheet("./assets/bullets/charge.png", json.load(open("./assets/bullets/charge.json")))

# Game Setup
level = Level(level_file, level_sheet)
l_width, l_height = level.shape()
camera = Camera(l_width, l_height, win_width, win_height)
physics = Physics(0.8, -0.15)
world = World(gamemanager.get_window(), camera, physics, level)

fire_gun = ChargeGun(charge_bullet_sheet)
player = Player(world, player_sheet)
player.set_gun(fire_gun)
world.add_to_group(player, "players")
world.set_background(bkgr_fname)

while gamemanager.state:
    gamemanager.clock.tick(FPS)
    gamemanager.parse(pygame.event.get())
    world.update()
    camera.update(player)
    gamemanager.game_loop(world, camera)

pygame.quit()
