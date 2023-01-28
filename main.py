import pygame
import grid as board
import player as plr
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = (500, 500)
block_side = 20

block_count = size[0] // block_side
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")

game_running = True

clock = pygame.time.Clock()
grid = board.Grid()
grid.generate_grid(size[0], size[0])
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

    for x in range(block_count):
        for y in range(block_count):
            color = grid.nodes[x][y].perlin_val * 255
            pygame.draw.rect(screen, (color, 120, color),
                             pygame.Rect(x * block_side, y * block_side, block_side - 1, block_side - 1))
    player_x = player.position[0]
    player_y = player.position[1]
    pygame.draw.rect(screen, RED,
                     pygame.Rect((player_x + 0.25) * block_side, (player_y + 0.25) * block_side, block_side/2,
                                 block_side/2))
    pygame.display.flip()

pygame.quit()
