# main imports
from typing import Match
import pygame

# custom file imports
from floor import Floor
from bckg_obj import BackgroundObject
from player import Player
import level_reader

# testing area

# ========== INIT ==============
pygame.init()

# color definitions
BLACK = (0, 0, 0)
BLUE = (57, 177, 235)
BROWN = (194, 130, 52)
GREEN = (15, 227, 11)
RED = (189, 9, 42)


# constants
TITLE = "Genetic Level Checker"
GRAVITY = 0.5
HUMAN_CONTROL = True
TILE_SIZE = 30
LEVEL_NAME = 'level.csv'
level = level_reader.getLevel(LEVEL_NAME)
SCR_W = len(level[0]) * TILE_SIZE
SCR_H = len(level) * TILE_SIZE
SCR_DIMENSIONS = (SCR_W, SCR_H)
SCR = pygame.display.set_mode(SCR_DIMENSIONS)

level = level_reader.getLevel(LEVEL_NAME)

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

sprite_group = pygame.sprite.Group()
floor_tiles = pygame.sprite.Group()
characters = pygame.sprite.Group()
player = None

# load level
x = 0
y = 0
for row in level:
    x = 0
    for cell in row:
        if cell == 0:
            pass
        elif cell == 1:  # static floor tile
            tile = Floor(BROWN, TILE_SIZE, TILE_SIZE)
            tile.rect.x = x * TILE_SIZE
            tile.rect.y = y * TILE_SIZE
            sprite_group.add(tile)
            floor_tiles.add(tile)
        elif cell == 9:  # player
            player = Player(GREEN, TILE_SIZE, GRAVITY)
            player.rect.x = x * TILE_SIZE
            player.rect.y = y * TILE_SIZE
            sprite_group.add(player)
            characters.add(player)
        else:
            print("there's an error in the level data")

        x += 1
    y += 1

# MAIN LOOP
quit = False
while not quit and player is not None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    sprite_group.update()

    # check if player is colliding with floor
    if pygame.sprite.spritecollideany(player, floor_tiles):
        player.y_spd = 0
        player.is_jumping = False

    # Key events (ONLY ALLOWED WHEN A HUMAN IS PLAYING)
    if HUMAN_CONTROL:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

        if keys[pygame.K_a]:
            player.pressLeft()
        else:
            player.releaseLeft()

        if keys[pygame.K_d]:
            player.pressRight()
        else:
            player.releaseRight()

    # draw in screen
    SCR.fill(BLACK)
    # sprite_group.draw(SCR)
    floor_tiles.draw(SCR)
    characters.draw(SCR)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
