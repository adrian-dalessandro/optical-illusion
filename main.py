from utils.actors.player import Player
from utils.managers import GameManager
from utils.world.world import World, Physics
import pygame

def updateGameWindow(world, group):
    world.window.fill((0,0,0))
    group.draw(world.window)
    pygame.display.update()

pygame.init()
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("Optical Illusion")
clock = pygame.time.Clock()

world = World(win, Physics(0.8, -0.15))

gamemanager = GameManager()
player = Player(world)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while gamemanager.state:
    clock.tick(27)
    gamemanager.parse(pygame.event.get())
    player.update()

    updateGameWindow(world, all_sprites)


pygame.quit()
