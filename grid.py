import node
from worldgen import OCTAVE, SEED
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
        noise1 = PerlinNoise(octaves=OCTAVE * 1, seed=SEED)
        noise2 = PerlinNoise(octaves=OCTAVE * 2, seed=SEED)
        noise3 = PerlinNoise(octaves=OCTAVE * 4, seed=SEED)

        pic = [[0 for i in range(width)] for j in range(height)]

        for x in range(width):
            column = {}
            for y in range(height):
                pic[x][y] = 1.00 * noise1([x / width, y / height]) + \
                            0.50 * noise2([x / width, y / height]) + \
                            0.25 * noise3([x / width, y / height])
                column[y] = node.Node(pic[x][y] + 0.5)

            self.nodes[x] = column
