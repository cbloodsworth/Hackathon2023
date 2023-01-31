import pygame
import better_gui as ui
import worldgen
import grid as board
import player as plr
from worldgen import *
import random
from math import floor
from grid import *
random.seed()
pygame.init()
# Font
game_font = pygame.font.SysFont("monospace", 20)

game_font_smaller = pygame.font.SysFont("monospace", 16)
# GUI

# Main screen UI
main_screen_ui = ui.UI()  # Initialize UI for main screen

# Start game button
start_btn = ui.Textbox(game_font)
start_btn.pos = screen_center
start_btn.size = [300, 100]
start_btn.text = "Begin Your Journey"
start_btn.color = pygame.Color(0, 255, 0, 255)
main_screen_ui.buttons["Start Button"] = start_btn

# In game screen UI
game_screen_ui = ui.UI()

# Backpack button
open_backpack_btn = ui.Textbox(game_font)
open_backpack_btn.pos = [screen_size[0] * 0.85, screen_size[1] * 0.9]
open_backpack_btn.size = [200, 90]
open_backpack_btn.text = "Open Backpack"
open_backpack_btn.color = pygame.Color(0, 255, 0, 255)
game_screen_ui.buttons["Open Backpack"] = open_backpack_btn

# Notification text box
notification = ui.Textbox(game_font_smaller)
notification.justify = "top"
notification.pos = [screen_size[0] * 0.85, screen_size[1] * 0.15]
notification.size = [200, 90]
notification.color = pygame.Color(255, 255, 255, 180)
game_screen_ui.objects["Notification"] = notification

# Craft boat button
craft_button = ui.Textbox(game_font_smaller)
craft_button.justify = "top"
craft_button.pos = [screen_size[0] * 0.85, screen_size[1] * 0.45]
craft_button.size = [200, 90]
craft_button.color = pygame.Color(255, 255, 255, 180)
craft_button.text = "5 ??? to craft a boat"
game_screen_ui.buttons["Craft"] = craft_button
# Backpack UI
backpack_ui = ui.UI()

inventory_box = ui.Box()
inventory_box.size = [screen_size[0] * 0.75, screen_size[1] * 0.75]
inventory_box.pos = [screen_center[0], screen_center[1] * 0.85]
inventory_box.color = pygame.Color(0, 0, 0, 150)
backpack_ui.objects["Inventory Box"] = inventory_box

NUM_ITEMS = 36

for i in range(NUM_ITEMS):
    inventory_cell = ui.Textbox(game_font_smaller)
    cell_x = inventory_box.pos[0] + inventory_box.size[0] // 9 * (i % 9) - screen_size[0] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[0] * .19 / 18)
    cell_y = inventory_box.pos[1] + inventory_box.size[1] // 4 * (i // 9) - screen_size[1] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[1] * .06)
    inventory_cell.size = [inventory_box.size[0] * 0.09, inventory_box.size[0] * 0.09]
    inventory_cell.pos = [cell_x, cell_y]
    inventory_cell.color = pygame.Color(255, 255, 255, 100)
    backpack_ui.objects["Inventory Cell " + str(i+1)] = inventory_cell

# List of UIs
ui_list = [main_screen_ui, game_screen_ui, backpack_ui]
# Screen initialization
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Swamp Investigator")

# Grid, player, and clock initialization
clock = pygame.time.Clock()
world_grid = board.Grid()
world_grid.generate_grid(grid_width, grid_height)
rand_x = random.randint(0, grid_width-1)
rand_y = random.randint(0, grid_height-1)
while world_grid.nodes[rand_x][rand_y].biome != Biome.DEEP_OCEAN:
    rand_x = random.randint(0, grid_width-1)
    rand_y = random.randint(0, grid_height-1)
world_grid.nodes[rand_x][rand_y].items.append("Gator")

for x in world_grid.nodes:
    for y in world_grid.nodes[x]:
        if world_grid.nodes[x][y].biome == Biome.WOODLAND:
            if x % 5 == 0 or y % 4 == 0:
                world_grid.nodes[x][y].items.append("Wood")

pair_found = False

start_pos = [grid_width * block_size // 2, grid_width * block_size // 2]

player = plr.Player(start_pos)

# Pre game bools
game_running = True
game_begin = False

# In game bools
backpack_open = False
has_boat = False
while game_running:
    # Screen black
    screen.fill((0, 0, 255))
    # Frame rate
    time_delta = clock.tick(60) / 1000.0
    # Get player position
    plr_x = player.position[0]
    plr_y = player.position[1]

    gridwise_pos = [(plr_x + screen_size[0] // 2) // block_size, (plr_y + screen_size[1] // 2) // block_size]
    grid_items = world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].items
    if len(grid_items) > 0:
        if grid_items[0] in player.backpack:
            game_screen_ui.objects["Notification"].text = f"{grid_items[0]} found! Press x to pick up."
            if not has_boat:
                game_screen_ui.buttons["Craft"].text = "5 wood to craft a boat"
        elif grid_items[0] == "Wood" or has_boat:
            game_screen_ui.objects["Notification"].text = f"??? found? Press x to pick up."

    else:
        game_screen_ui.objects["Notification"].text = ""
    # Events
    pack_count = 0
    for item in player.backpack:
        pack_count += 1
        backpack_ui.objects[f"Inventory Cell {pack_count}"].text = item

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if len(grid_items) > 0 and pack_count < 36:
                    for item in grid_items:
                        player.backpack.append(item)
                        grid_items.remove(item)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for u in ui_list:
                for key in u.buttons.keys():
                    if u.buttons[key].get_bounds().collidepoint(mouse_pos):
                        if key == "Start Button":
                            game_begin = True
                        if key == "Open Backpack":
                            backpack_open = not backpack_open
                            if backpack_open:
                                u.buttons[key].text = "Close Backpack"
                                u.buttons[key].color = pygame.Color(255, 0, 0)
                            else:
                                u.buttons[key].text = "Open Backpack"
                                u.buttons[key].color = pygame.Color(0, 255, 0)
                        if key == "Craft" and not has_boat:
                            wood_count = 0
                            for item in player.backpack:
                                if item == "Wood":
                                    wood_count += 1
                            if wood_count >= 5:
                                last_count = wood_count
                                while wood_count > last_count - 5:
                                    backpack_ui.objects[f"Inventory Cell {wood_count}"].text = ""
                                    wood_count -= 1
                                    player.backpack.remove("Wood")
                                    has_boat = True
                                    game_screen_ui.buttons["Craft"].text = "Boat crafted!"

    if game_begin:
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
        if not has_boat:
            player_color = 0x880022 if currentBiome == Biome.DEEP_OCEAN else 0xFF0000
        else:
            player_color = 0x964B00 if currentBiome == Biome.DEEP_OCEAN else 0xFF0000

        # Actual player
        pygame.draw.rect(screen, player_color,
                         pygame.Rect(screen_center[0] - block_size / 4, screen_center[1] - block_size / 4,
                                     block_size / 2, block_size / 2))

        # Minimap player
        pygame.draw.rect(screen, player_color,
                         pygame.Rect((VISIBLE_BLOCKS_VERT // 2) * MM_ZOOM + MM_OFFSET_X,
                                     (VISIBLE_BLOCKS_VERT // 2) * MM_ZOOM + MM_OFFSET_Y, 2, 2))

        # Minimap Border
        # pygame.draw.rect(screen, 0xAAAAAA,
        #                  pygame.Rect()

    # GUI
    if game_begin:
        game_screen_ui.draw_all(screen)
    else:
        main_screen_ui.draw_all(screen)
    if backpack_open:
        backpack_ui.draw_all(screen)
    # Draw screen
    pygame.display.update()

pygame.quit()
