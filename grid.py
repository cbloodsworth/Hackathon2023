import node
from math import pow, pi, sin
from worldgen import ELEV_OCTAVE, MOIST_OCTAVE, SEED, ELEV_POWER, MOIST_POWER, POLE, EQUATOR
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
        e_noise1 = PerlinNoise(octaves=ELEV_OCTAVE * 1, seed=SEED[0])
        e_noise2 = PerlinNoise(octaves=ELEV_OCTAVE * 2, seed=SEED[1])
        e_noise3 = PerlinNoise(octaves=ELEV_OCTAVE * 4, seed=SEED[2])

        m_noise1 = PerlinNoise(octaves=MOIST_OCTAVE * 1, seed=SEED[3])
        m_noise2 = PerlinNoise(octaves=MOIST_OCTAVE * 2, seed=SEED[4])
        m_noise3 = PerlinNoise(octaves=MOIST_OCTAVE * 4, seed=SEED[5])

        elevation_array = [[0.0 for i in range(width)] for j in range(height)]  # Initializing
        moisture_array = [[0.0 for i in range(width)] for j in range(height)]  # Initializing

        for x in range(width):
            column = {}
            for y in range(height):
                elevation = 1.00 * e_noise1([x / width, y / height]) + \
                            0.50 * e_noise2([x / width, y / height]) + \
                            0.25 * e_noise3([x / width, y / height]) + 0.5

                moisture = 1.00 * m_noise1([x / width, y / height]) + \
                           0.50 * m_noise2([x / width, y / height]) + \
                           0.25 * m_noise3([x / width, y / height]) + 0.5

                elevation = pow(elevation, ELEV_POWER) if elevation > 0 else 0
                moisture = pow(moisture, MOIST_POWER) if moisture > 0 else 0

                # We want lower temperatures as we go further from the equator and towards the poles
                equiv_elevation = elevation + POLE*0.5 + (EQUATOR - POLE) * sin(pi * (y / height))
                elevation_array[x][y] = equiv_elevation
                moisture_array[x][y] = moisture

                column[y] = node.Node(equiv_elevation, moisture)

            self.nodes[x] = column

