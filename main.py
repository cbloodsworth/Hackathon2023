import pygame
import grid as board
import player as plr
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_size = (500, 500) # Screen size in pixels
block_size = 5  # Size of side of the block

grid_height, grid_width = 100, 100

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("My First Game")

game_running = True

clock = pygame.time.Clock()
grid = board.Grid()
grid.generate_grid(grid_width, grid_height)
player = plr.Player([2, 2])
while game_running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move([0, -0.001])
    if keys[pygame.K_s]:
        player.move([0, 0.001])
    if keys[pygame.K_a]:
        player.move([-0.001, 0])
    if keys[pygame.K_d]:
        player.move([0.001, 0])
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    for x in range(grid_width):
        for y in range(grid_height):
            color = grid.nodes[x][y].perlin_val * 255
            pygame.draw.rect(screen, (color, 120, color),
                             pygame.Rect(x * block_size, y * block_size, block_size - 1, block_size - 1))
    player_x = player.position[0]
    player_y = player.position[1]
    pygame.draw.rect(screen, RED,
                     pygame.Rect((player_x + 0.25) * block_size, (player_y + 0.25) * block_size, block_size / 2,
                                 block_size / 2))
    pygame.display.flip()

pygame.quit()
