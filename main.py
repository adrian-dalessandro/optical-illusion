from utils.actors.player import Player
from utils.world.platform import Platform
from utils.managers import GameManager, updateWorld
from utils.world.world import World, Physics, LevelBuilder
from utils.world.camera import Camera
from utils.graphics.sheets import Spritesheet, IconSheet
from utils.graphics.themes import Theme
from utils.weapons.guns import DefaultGun, FireGun
import pygame
import json

HEIGHT = 600
WIDTH = 500
FPS = 27

theme = Theme("./themes/Grass")

# Game Manager creates the game window and does other basic setup.
gamemanager = GameManager(WIDTH, HEIGHT, "Optical Illusion")
level_sheet = Spritesheet(theme.tilesheet.spritesheet, theme.tilesheet.dict)
player_sheet = Spritesheet(theme.actorsheet.spritesheet, theme.actorsheet.dict)
fire_bullet_sheet = IconSheet("./assets/bullets/fire.png", json.load(open("./assets/bullets/fire.json")))

fire_gun = FireGun(fire_bullet_sheet)

bkgr_fname = "./assets/layouts/kenney_backgroundElements/Samples/colored_talltrees.png"
background_image = pygame.image.load(bkgr_fname).convert()
bheight = background_image.get_height()
bwidth = background_image.get_width()
scale = HEIGHT/bheight
background_image = pygame.transform.scale(background_image, (int(scale*bheight), int(scale*bwidth)))

# world holds the basic parameters of the world and references to sprites
world = World(gamemanager.win, Physics(0.8, -0.15), {"player": player_sheet, "level": level_sheet}, background_image)
level = LevelBuilder("./worlds/sandbox.world", world)
lvl_height, lvl_width = level.shape()
camera = Camera(lvl_width, lvl_height, WIDTH, HEIGHT)
world.width = lvl_width
world.height = lvl_height

player = Player(world, fire_gun)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while gamemanager.state:
    gamemanager.clock.tick(FPS)
    gamemanager.parse(pygame.event.get())
    player.update()
    camera.update(player)

    updateWorld(world, all_sprites, camera)


pygame.quit()
