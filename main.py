import pygame
import better_gui as ui
import worldgen
import grid as board
import player as plr

pygame.init()
# Font
game_font = pygame.font.SysFont("monospace", 20)

# Board parameters
block_size = 25  # Size of side of the block
grid_height, grid_width = 100, 100
screen_size = min(grid_height * block_size, 1000), min(grid_width * block_size, 650)  # Screen size in pixels
screen_center = [screen_size[0] // 2, screen_size[1] // 2]

# GUI

# Main screen UI
main_screen_ui = ui.UI()  # Initialize UI for main screen

# Start game button
start_btn = ui.Textbox(game_font)
start_btn.pos = screen_center
start_btn.size = [300, 100]
start_btn.text = "Begin Your Journey"
start_btn.color = pygame.Color(0, 255, 0, 0)
main_screen_ui.buttons["Start Button"] = start_btn

# In game screen UI
game_screen_ui = ui.UI()

# Backpack button
open_backpack_btn = ui.Textbox(game_font)
open_backpack_btn.pos = [screen_size[0] * 0.85, screen_size[1] * 0.9]
open_backpack_btn.size = [200, 90]
open_backpack_btn.text = "Open Backpack"
open_backpack_btn.color = pygame.Color(0, 255, 0, 0)
game_screen_ui.buttons["Open Backpack"] = open_backpack_btn

# Backpack UI

backpack_ui = ui.UI()

inventory_box = ui.Box()
inventory_box.size = [screen_size[0] * 0.75, screen_size[1] * 0.75]
inventory_box.pos = [screen_center[0], screen_center[1] * 0.85]
inventory_box.color = pygame.Color(0, 0, 0, 150)
backpack_ui.objects["Inventory Box"] = inventory_box

NUM_ITEMS = 36

for i in range(NUM_ITEMS):
    inventory_cell = ui.Box()
    cell_x = inventory_box.pos[0] + inventory_box.size[0] // 9 * (i % 9) - screen_size[0] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[0] * .19 / 18)
    cell_y = inventory_box.pos[1] + inventory_box.size[1] // 4 * (i // 9) - screen_size[1] * 0.75 // 2 + inventory_box.size[0] * 0.045 + (inventory_box.size[1] * .08)
    inventory_cell.size = [inventory_box.size[0] * 0.09, inventory_box.size[0] * 0.09]
    inventory_cell.pos = [cell_x, cell_y]
    inventory_cell.color = pygame.Color(0, 0, 255, 100)
    backpack_ui.objects["Inventory Cell " + str(i)] = inventory_cell

# List of UIs
ui_list = [main_screen_ui, game_screen_ui, backpack_ui]
# Screen initialization
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Exploring The Unknown")

# Grid, player, and clock initialization
clock = pygame.time.Clock()
grid = board.Grid()
grid.generate_grid(grid_width, grid_height)
player = plr.Player([0, 0])

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

        sprint = 1  # Sprint factor. Not sprinting = 1, sprinting = 2

        if keys[pygame.K_LSHIFT]: sprint = 2

        if keys[pygame.K_w]: player.move([0, 2 * sprint])
        if keys[pygame.K_s]: player.move([0, -2 * sprint])
        if keys[pygame.K_a]: player.move([2 * sprint, 0])
        if keys[pygame.K_d]: player.move([-2 * sprint, 0])

        # Set tile position and colors
        for x in range(grid_width):
            for y in range(grid_height):
                col = worldgen.colorMap[grid.nodes[x][y].biome]
                center_x = (x - grid_width // 2) * block_size + screen_center[0]
                center_y = (y - grid_height // 2) * block_size + screen_center[1]
                pygame.draw.rect(screen, col,
                                 pygame.Rect(center_x + plr_x, + center_y + plr_y, block_size, block_size))

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
