import node
from perlin_noise import PerlinNoise


class Grid:
    def __init__(self):
        self.nodes = {}

    def generate_grid(self, length, height):
        noise = PerlinNoise(octaves=10, seed=3)
        pic = [[noise([i / height, j / length]) for j in range(length)] for i in range(height)]
        for x in range(length):
            column = {}
            for y in range(height):
                column[y] = node.Node()
                column[y].perlin_val = pic[x][y] * 0.5 + 0.5
            self.nodes[x] = column
