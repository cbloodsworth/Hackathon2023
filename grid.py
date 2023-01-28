import node
from perlin_noise import PerlinNoise


class Grid:
    def __init__(self):
        self.nodes = {}

    def generate_grid(self, width, height):
        """

        :param width: Grid width in blocks
        :param height: Grid height in blocks
        :return:
        """
        noise = PerlinNoise(octaves=10, seed=3)
        pic = [[noise([i / height, j / width]) for j in range(width)] for i in range(height)]
        for x in range(width):
            column = {}
            for y in range(height):
                column[y] = node.Node()
                column[y].perlin_val = pic[x][y] * 0.5 + 0.5
            self.nodes[x] = column
