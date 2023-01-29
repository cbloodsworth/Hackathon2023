import pygame
import better_gui as ui
import worldgen
import grid as board
import player as plr
from worldgen import WALKABLE
from math import floor
from grid import *

pygame.init()
# Font
game_font = pygame.font.SysFont("monospace", 20)

game_font_smaller = pygame.font.SysFont("monospace", 16)

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
notification.pos = [screen_size[0] * 0.85, screen_size[1] * 0.3]
notification.size = [200, 150]
notification.color = pygame.Color(255, 255, 255, 180)
game_screen_ui.objects["Notification"] = notification

# Backpack UI
backpack_ui = ui.UI()

inventory_box = ui.Box()
inventory_box.size = [screen_size[0] * 0.75, screen_size[1] * 0.75]
inventory_box.pos = [screen_center[0], screen_center[1] * 0.85]
inventory_box.color = pygame.Color(0, 0, 0, 150)
backpack_ui.objects["Inventory Box"] = inventory_box

NUM_ITEMS = 36

for i in range(NUM_ITEMS):
    inventory_cell = ui.Textbox(game_font)
    cell_x = inventory_box.pos[0] + inventory_box.size[0] // 9 * (i % 9) - screen_size[0] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[0] * .19 / 18)
    cell_y = inventory_box.pos[1] + inventory_box.size[1] // 4 * (i // 9) - screen_size[1] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[1] * .06)
    inventory_cell.size = [inventory_box.size[0] * 0.09, inventory_box.size[0] * 0.09]
    inventory_cell.pos = [cell_x, cell_y]
    inventory_cell.color = pygame.Color(255, 255, 255, 100)
    backpack_ui.objects["Inventory Cell " + str(i)] = inventory_cell

# List of UIs
ui_list = [main_screen_ui, game_screen_ui, backpack_ui]
# Screen initialization
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Exploring The Unknown")

# Grid, player, and clock initialization
clock = pygame.time.Clock()
world_grid = board.Grid()
world_grid.generate_grid(grid_width, grid_height)

visited = set()
pair_found = False

start_pos = [0, 0]

player = plr.Player(start_pos)

world_grid.nodes[50][50].items = {1: "Wood"}
world_grid.nodes[49][50].items = {1: "Stone"}
world_grid.nodes[51][50].items = {1: "Gold"}
# Pre game bools
game_running = True
game_begin = False

# In game bools
backpack_open = False

while game_running:
    # Frame rate
    time_delta = clock.tick(60) / 1000.0
    # Get player position
    plr_x = player.position[0]
    plr_y = player.position[1]

    gridwise_pos = [(plr_x + screen_size[0] // 2) // block_size, (plr_y + screen_size[1] // 2) // block_size]

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
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

    if game_begin:
        # Player movement
        keys = pygame.key.get_pressed()

        sprint = 2  # Sprint factor. Not sprinting = 1, sprinting = 2

        if keys[pygame.K_LSHIFT]: sprint = 2

        # DEBUG
        if keys[pygame.K_SPACE]: print(gridwise_pos)

        if world_grid.nodes[gridwise_pos[0]][gridwise_pos[1]].elevation < WALKABLE:
            sprint = 0.5

        if keys[pygame.K_w]: player.move([0, -2 * sprint])
        if keys[pygame.K_s]: player.move([0, 2 * sprint])
        if keys[pygame.K_a]: player.move([-2 * sprint, 0])
        if keys[pygame.K_d]: player.move([2 * sprint, 0])

        # Set tile position and colors
        for x in range(grid_width):
            for y in range(grid_height):
                col = worldgen.colorMap[world_grid.nodes[x][y].biome]
                center_x, center_y = x * block_size, y * block_size
                pygame.draw.rect(screen, col,
                                 pygame.Rect(center_x - plr_x, + center_y - plr_y, block_size, block_size))

        # Player draw
        pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                         pygame.Rect(screen_center[0] - block_size / 4, screen_center[1] - block_size / 4,
                                     block_size / 2, block_size / 2))


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
