import math, sys
from perlin_noise import PerlinNoise
import pygame

pygame.init()
width, height = 800, 600

screen_display = pygame.display
screen_display.set_caption("World Generation")

surface = screen_display.set_mode((width, height))

size = 10
numSquares = 50
board = pygame.Surface((size * numSquares, size * numSquares))
board.fill((255, 255, 255))

noise = PerlinNoise(octaves=10, seed=69)

pic = [[noise([i/numSquares, j/numSquares]) for j in range(numSquares)] for i in range(numSquares)]

for x in range(0, numSquares, 2):
    for y in range(0, numSquares, 2):
        c = 255 * (pic[x][y] * 0.5 + 0.5)
        pygame.draw.rect(board, (c,c,c), (x*size, y*size, size, size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    surface.blit(board, board.get_rect())
    screen_display.update()