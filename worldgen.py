from enum import Enum
from math import floor

OCTAVE = 8
SEED = 823749


class Biome(Enum):
    # The difference between the first and next enum on this list determines how common the next will be.
    # Convoluted, I know. Maybe we could refactor this -C

    # BLANK = 100
    DEEP_OCEAN = 90
    OCEAN = 60
    BEACH = 55
    PLAINS = 40
    FOREST = 30
    MOUNTAIN = 10
    TALL_MOUNTAIN = 0


colorMap = {
    Biome.DEEP_OCEAN.value: (5, 12, 69),      # deep ocean
    Biome.OCEAN.value: (13, 30, 168),          # ocean
    Biome.BEACH.value: (222, 204, 155),           # beach
    Biome.PLAINS.value: (115, 168, 106),          # plains
    Biome.FOREST.value: (74, 110, 68),             # forest
    Biome.MOUNTAIN.value: (79, 117, 92),          # mountain
    Biome.TALL_MOUNTAIN.value: (200, 232, 211)    # tall mountain
}

class Terrain:
    def __init__(self, p: float):
        """

        :param p: Stands for perlin value: Range from 0-1.
        """
        self.perlin_val = p

        if p > 1.0:   p = 1.0
        elif p < 0.0: p = 0.0

        # Weird solution, might refactor later.
        # We want to multiply the perlin value by 100 and take the floor to get its integer equivalent.
        # The while loop checks if the "heat value" that corresponds with the perlin val exists, and
        # tries to find the next closest down if not.
        biomeKey = floor(p * 100)

        while biomeKey not in colorMap and biomeKey > 0:
            biomeKey -= 1

        self.biome = biomeKey
