import pygame
import gui as ui
import worldgen
import grid as board
import player as plr
from worldgen import *
import random
from math import floor
from grid import *

# Game needs to start otherwise Font cannot load
pygame.init()
from gui import gui_manager

random.seed()

# Screen initialization
window = pygame.display.set_mode(screen_size)
screen = pygame.Surface(screen_size, pygame.SRCALPHA)

pygame.display.set_caption("Swamp Investigator")

# Grid, player, and clock initialization
clock = pygame.time.Clock()
world_grid = board.Grid()
world_grid.generate_grid(grid_width, grid_height)
rand_x = random.randint(0, grid_width - 1)
rand_y = random.randint(0, grid_height - 1)

while world_grid.nodes[rand_x][rand_y].biome != Biome.DEEP_OCEAN:
    rand_x = random.randint(0, grid_width - 1)
    rand_y = random.randint(0, grid_height - 1)
world_grid.nodes[rand_x][rand_y].items.append("Gator")

for x in world_grid.nodes:
    for y in world_grid.nodes[x]:
        if world_grid.nodes[x][y].biome == Biome.WOODLAND:
            if x % 5 == 0 or y % 4 == 0:
                world_grid.nodes[x][y].items.append("Wood")

start_pos = [grid_width * block_size // 2, grid_width * block_size // 2]

player = plr.Player(start_pos)

game_running = True
has_boat = True
game_begin = False

while game_running:
    # Screen black
    screen.fill((0, 0, 0, 0))
    window.fill((0, 0, 255))

    # Frame rate
    time_delta = clock.tick(60) / 1000.0
    # Get player position
    plr_x = player.position[0]
    plr_y = player.position[1]

    gridwise_pos = [(plr_x + screen_size[0] // 2) // block_size, (plr_y + screen_size[1] // 2) // block_size]
    grid_items = world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].items
    # Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for key in gui_manager.buttons:
                btn = gui_manager.buttons[key]
                if btn.bounds.collidepoint(mouse_pos):
                    if key == "start_game_btn":
                        game_begin = True
                        btn.enabled = False
                    if key == "backpack_btn":
                        inv = gui_manager.objects["backpack_inventory"]
                        inv.enabled = not inv.enabled

    if game_begin:
        gui_manager.buttons["backpack_btn"].enabled = True
        gui_manager.objects["alert_box"].enabled = True

        if len(world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].items) > 0:
            its = world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].items
            gui_manager.objects["alert_box"].text = f"Press x to pick up {its[0]}"
        else:
            gui_manager.objects["alert_box"].text = ""
        # Player movement
        keys = pygame.key.get_pressed()

        sprint = 1  # Sprint factor. Not sprinting = 1, sprinting = 2

        if keys[pygame.K_LSHIFT]: sprint = 2

        # DEBUG
        if keys[pygame.K_SPACE]: print(gridwise_pos)

        currentBiome = biome(world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].elevation,
                             world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].moisture)

        if currentBiome == Biome.DEEP_OCEAN:
            if has_boat:
                sprint = 2.5
            else:
                sprint = 0.5
        elif currentBiome == Biome.OCEAN:
            sprint = 0.8
        elif currentBiome.value & 0x003 == 0x003:
            sprint = 1

        if gridwise_pos[1] > 0:
            if keys[pygame.K_w]: player.move([0, -3 * sprint])

        if gridwise_pos[1] < grid_height - 1:
            if keys[pygame.K_s]: player.move([0, 3 * sprint])

        if gridwise_pos[0] > 0:
            if keys[pygame.K_a]: player.move([-3 * sprint, 0])

        if gridwise_pos[0] < grid_width - 1:
            if keys[pygame.K_d]: player.move([3 * sprint, 0])

        # In pixels
        MM_OFFSET_X = 30
        MM_OFFSET_Y = 30
        MM_BORDER_THICK = 5

        MM_SIZE_HORZ = VISIBLE_BLOCKS_HORZ // 2 + 0  # Change second value. WARNING: WILL AFFECT PERFORMANCE
        MM_SIZE_VERT = VISIBLE_BLOCKS_HORZ // 2 + 0
        # The astute eye may notice that VISIBLE_BLOCKS_HORZ is used, rather than its vertical equivalent.
        # This is intentional and allows the minimap to be square.

        MM_ZOOM = 2

        # Set tile position and colors
        for i in range(-MM_SIZE_HORZ, MM_SIZE_HORZ):
            for j in range(-MM_SIZE_VERT, MM_SIZE_VERT):
                x = max(0, min(i + gridwise_pos[0], grid_width - 1))
                y = max(0, min(j + gridwise_pos[1], grid_height - 1))

                # Color is initially set to the biome color value
                col = worldgen.colorMap[world_grid.nodes[x][y].biome]

                if abs(x - gridwise_pos[0]) < FOG_OF_WAR and abs(y - gridwise_pos[1]) < FOG_OF_WAR:
                    world_grid.nodes[x][y].visited = True
                    col += 0x212121

                center_x, center_y = x * block_size, y * block_size

                # Only draw tiles if visible
                if -VISIBLE_BLOCKS_HORZ // 2 < i < VISIBLE_BLOCKS_HORZ // 2 and\
                   -VISIBLE_BLOCKS_VERT // 2 < j < VISIBLE_BLOCKS_VERT // 2:
                    pygame.draw.rect(screen, col if world_grid.nodes[x][y].visited else 0x666666,
                                     pygame.Rect(center_x - plr_x, center_y - plr_y, block_size, block_size))

        for i in range(-MM_SIZE_HORZ, MM_SIZE_HORZ):
            for j in range(-MM_SIZE_VERT, MM_SIZE_VERT):
                x = max(0, min(i + gridwise_pos[0], grid_width - 1))
                y = max(0, min(j + gridwise_pos[1], grid_height - 1))

                col = worldgen.colorMap[world_grid.nodes[x][y].biome]

                # Draw Minimap, which has double the view distance as the regular viewport
                pygame.draw.rect(screen, col,
                                 pygame.Rect((x + MM_OFFSET_X - plr_x // block_size) * MM_ZOOM,
                                             (y + MM_OFFSET_Y - plr_y // block_size) * MM_ZOOM, MM_ZOOM,
                                             MM_ZOOM))

        # Player color change if in water
                pygame.draw.rect(window, col,
                                 pygame.Rect(center_x - plr_x, + center_y - plr_y, block_size, block_size))

        for x in range(grid_width):
            for y in range(grid_height):
                curr = world_grid.nodes[x][y]
                col = worldgen.colorMap[curr.biome]
                if curr.items:
                    if curr.items[0] == "Wood":
                        col = 0x00F0F0
                    else:
                        col = 0xAB9213
                if not curr.visited:
                    col = 0x888888
                pygame.draw.rect(window, col, pygame.Rect(x * 2 + 10, y * 2 + 10, 2, 2))

        # Player draw
        if not has_boat:
            player_color = 0x880022 if currentBiome == Biome.DEEP_OCEAN else 0xFF0000
        else:
            player_color = 0x964B00 if currentBiome == Biome.DEEP_OCEAN else 0xFF0000

        # Actual player
        pygame.draw.rect(window, player_color,
                         pygame.Rect(screen_center[0] - block_size / 4, screen_center[1] - block_size / 4,
                                     block_size / 2, block_size / 2))

        # Minimap player
        pygame.draw.rect(window, player_color,
                         pygame.Rect((VISIBLE_BLOCKS_VERT // 2) * MM_ZOOM + MM_OFFSET_X,
                                     (VISIBLE_BLOCKS_VERT // 2) * MM_ZOOM + MM_OFFSET_Y, 2, 2))

        # Minimap Border
        # pygame.draw.rect(screen, 0xAAAAAA,
        #                  pygame.Rect()

    # Draw GUI
    gui_manager.draw_all(screen)
    window.blit(screen, (0, 0))


    # Update
    pygame.display.update()

pygame.quit()
