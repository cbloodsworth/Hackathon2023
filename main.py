import pygame
import pygame_gui
import worldgen
import grid as board
import player as plr

pygame.init()

# Board parameters
screen_size = (500, 500)  # Screen size in pixels
block_size = 50  # Size of side of the block
grid_height, grid_width = 100, 100

# Screen initialization
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Exploring The Unknown")

# Main menu screen GUI
main_background = pygame.Surface(screen_size)
main_background.fill(pygame.Color('#000000'))
main_gui = pygame_gui.UIManager(screen_size)
start_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 200), (200, 100)),
                                          text='Begin Your Journey',
                                          manager=main_gui)

# In game GUI
game_gui = pygame_gui.UIManager(screen_size)


game_running = True
game_begin = False
clock = pygame.time.Clock()
grid = board.Grid()
grid.generate_grid(grid_width, grid_height)
player = plr.Player([2, 2])
while game_running:
    # Frame rate
    time_delta = clock.tick(60) / 1000.0

    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if game_begin:
            game_gui.process_events(event)
        else:
            main_gui.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_game:
                game_begin = True
    if game_begin:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move([0, -0.01])
        if keys[pygame.K_s]:
            player.move([0, 0.01])
        if keys[pygame.K_a]:
            player.move([-0.01, 0])
        if keys[pygame.K_d]:
            player.move([0.01, 0])

        # Set tile colors
        for x in range(grid_width):
            for y in range(grid_height):
                color = worldgen.biomeMap[grid.nodes[x][y].terrain.biome]
                pygame.draw.rect(screen, color,
                                 pygame.Rect(x * block_size, y * block_size, block_size, block_size))

        # Player draw
        player_x = player.position[0]
        player_y = player.position[1]
        pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                         pygame.Rect((player_x + 0.25) * block_size, (player_y + 0.25) * block_size, block_size / 2,
                                     block_size / 2))

    # GUI
    if game_begin:
        game_gui.update(time_delta)

    else:
        main_gui.update(time_delta)
        screen.blit(main_background, (0, 0))
        main_gui.draw_ui(screen)

    # Draw screen
    pygame.display.update()

pygame.quit()
