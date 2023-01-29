import node
from math import pow
from worldgen import OCTAVE, SEED, ELEV_POWER
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
        noise1 = PerlinNoise(octaves=OCTAVE * 1, seed=SEED[0])
        noise2 = PerlinNoise(octaves=OCTAVE * 2, seed=SEED[1])
        noise3 = PerlinNoise(octaves=OCTAVE * 4, seed=SEED[2])

        pic = [[0.0 for i in range(width)] for j in range(height)]  # Initializing

        # These variables are good if you want to make sure the elevation range is valid (0-1).
        # TEST_min = 255
        # TEST_max = 0

        for x in range(width):
            column = {}
            for y in range(height):
                elevation = 1.00 * noise1([x / width, y / height]) + \
                            0.50 * noise2([x / width, y / height]) + \
                            0.25 * noise3([x / width, y / height]) + 0.5

                elevation = pow(elevation, ELEV_POWER) if elevation > 0 else 0
                # TEST_max = max(elevation, TEST_max)
                # TEST_min = min(elevation, TEST_min)

                pic[x][y] = elevation
                column[y] = node.Node(elevation)

            self.nodes[x] = column

