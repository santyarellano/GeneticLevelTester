# main imports
import pygame
pygame.init()

# custom file imports
import groups
import level_reader
import colors
import settings
from player import Player
from floor import Floor
from goal import Goal
from population import Population


# setup
level = level_reader.getLevel(settings.LEVEL_NAME)
settings.SCR_W = len(level[0]) * settings.TILE_SIZE
settings.SCR_H = len(level) * settings.TILE_SIZE
SCR_DIMENSIONS = (settings.SCR_W, settings.SCR_H)
SCR = pygame.display.set_mode(SCR_DIMENSIONS)
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

level = level_reader.getLevel(settings.LEVEL_NAME)

pygame.display.set_caption(settings.TITLE)

clock = pygame.time.Clock()

# load level
x = 0
y = 0
for row in level:
    x = 0
    for cell in row:
        if cell == 0:
            pass
        elif cell == 1:  # static floor tile
            tile = Floor(colors.BROWN, settings.TILE_SIZE, settings.TILE_SIZE)
            tile.rect.x = x * settings.TILE_SIZE
            tile.rect.y = y * settings.TILE_SIZE
            groups.floor_tiles.add(tile)
        elif cell == 8: # goal
            goal = Goal(colors.YELLOW, settings.TILE_SIZE, settings.TILE_SIZE)
            goal.rect.x = x * settings.TILE_SIZE
            goal.rect.y = y * settings.TILE_SIZE
            groups.top_layer.add(goal)
            settings.goal = goal
        elif cell == 9:  # player
            settings.PLAYER_SPAWN_X = x * settings.TILE_SIZE
            settings.PLAYER_SPAWN_Y = y * settings.TILE_SIZE

            if settings.HUMAN_CONTROL:
                player = Player(colors.GREEN, settings.TILE_SIZE, settings.GRAVITY, False)
                player.rect.x = settings.PLAYER_SPAWN_X
                player.rect.y = settings.PLAYER_SPAWN_Y
                groups.players_group.add(player)
            else:
                population = Population(settings.POPULATION_SIZE)
            
        else:
            print("there's an error in the level data")

        x += 1
    y += 1

# MAIN LOOP
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    groups.players_group.update()

    # Key events (ONLY ALLOWED WHEN A HUMAN IS PLAYING)
    if settings.HUMAN_CONTROL:
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
    elif population.generation < settings.GENERATIONS_WITHOUT_RENDER:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            settings.GENERATIONS_WITHOUT_RENDER = 0

    # draw in screen
    if settings.HUMAN_CONTROL or (population.generation > settings.GENERATIONS_WITHOUT_RENDER):
        SCR.fill(colors.BLACK)
        groups.floor_tiles.draw(SCR)
        groups.top_layer.draw(SCR)
        groups.players_group.draw(SCR)

        # show generation
        if not settings.HUMAN_CONTROL:
            txt = f'Generation: {population.generation}. Population: {len(population.players)}'
            text_renderer = font.render(txt, False, colors.WHITE)
            SCR.blit(text_renderer, (20,20))

        pygame.display.flip()

        clock.tick(settings.FPS)

    # genetic algorithm
    if not settings.HUMAN_CONTROL:
        if population.allFinished():
            population.calculateFitness()
            population.setBestPosition()
            population.naturalSelection()

pygame.quit()
