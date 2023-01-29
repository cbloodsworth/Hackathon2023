import pygame
import pygame_gui
import worldgen
import grid as board
import player as plr

pygame.init()

# Board parameters


block_size = 25  # Size of side of the block

grid_height, grid_width = 100, 100
screen_size = min(grid_height * block_size, 1000), min(grid_width * block_size, 650)  # Screen size in pixels
screen_center = [screen_size[0] // 2, screen_size[1] // 2]

# Screen initialization
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Exploring The Unknown")

# Main menu screen GUI
main_background = pygame.Surface(screen_size)
main_background.fill(pygame.Color('#000000'))
main_gui = pygame_gui.UIManager(screen_size)
start_game_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen_center[0] - 100, screen_center[1] - 50), (200, 100)),
    text='Begin Your Journey',
    manager=main_gui)

# In game GUI
game_gui = pygame_gui.UIManager(screen_size, 'theme.json')
backpack_background = pygame.Surface(screen_size)
backpack_background.fill(pygame.Color('#000000'))
open_backpack_btn = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(screen_size[0] * 0.85, screen_size[1] * 0.825, 100, 75),
    text='Backpack',
    manager=game_gui)

game_running = True
game_begin = False
clock = pygame.time.Clock()
grid = board.Grid()
grid.generate_grid(grid_width, grid_height)
player = plr.Player([0, 0])

# In game bools
backpack_open = False

while game_running:
    # Frame rate
    time_delta = clock.tick(60) / 1000.0
    # Get player position
    plr_x = player.position[0]
    plr_y = player.position[1]
    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if game_begin:
            game_gui.process_events(event)
        else:
            main_gui.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_game_btn:
                game_begin = True
            if event.ui_element == open_backpack_btn:
                backpack_open = not backpack_open
    if game_begin:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move([0, 1])
        if keys[pygame.K_s]:
            player.move([0, -1])
        if keys[pygame.K_a]:
            player.move([1, 0])
        if keys[pygame.K_d]:
            player.move([-1, 0])

        # Set tile position and colors
        for x in range(grid_width):
            for y in range(grid_height):
                col = worldgen.colorMap[grid.nodes[x][y].terrain.biome]
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
        game_gui.update(time_delta)
        if backpack_open:
            pass
        game_gui.draw_ui(screen)
    else:
        main_gui.update(time_delta)
        screen.blit(main_background, (0, 0))
        main_gui.draw_ui(screen)

    # Draw screen
    pygame.display.update()

pygame.quit()
