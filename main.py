from utils.actors.player import Player
from utils.world.platform import Platform
from utils.managers import GameManager, updateWorld
from utils.world.world import World, Physics
from utils.graphics.sheets import consume_xml_sheet, Spritesheet
import pygame

HEIGHT = 600
WIDTH = 500
FPS = 27
sheet_dir = "./assets/layouts/platformerGraphicsDeluxe_Updated/Tiles"
sheet_fname = "{}/tiles_spritesheet.xml".format(sheet_dir)
tile_fname = "{}/tiles_spritesheet.png".format(sheet_dir)
bkgr_fname = "./assets/layouts/kenney_backgroundElements/Samples/colored_talltrees.png"

# Game Manager creates the game window and does other basic setup.
gamemanager = GameManager(WIDTH, HEIGHT, "Optical Illusion")
spritesheet = Spritesheet(tile_fname, consume_xml_sheet(sheet_fname))

background_image = pygame.image.load(bkgr_fname).convert()
bheight = background_image.get_height()
bwidth = background_image.get_width()
scale = HEIGHT/bheight
background_image = pygame.transform.scale(background_image, (int(scale*bheight), int(scale*bwidth)))

# world holds the basic parameters of the world and references to sprites
world = World(gamemanager.win, Physics(1.0, -0.15), spritesheet, background_image)
player = Player(world)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for i in range(0, WIDTH, 50):
    world.platform_factory(i, HEIGHT, 50, "grassCenter.png")
for i in range(0, WIDTH, 50):
    world.platform_factory(i, HEIGHT-50, 50, "grassMid.png")

while gamemanager.state:
    gamemanager.clock.tick(FPS)
    gamemanager.parse(pygame.event.get())
    player.update()

    updateWorld(world, all_sprites)


pygame.quit()
