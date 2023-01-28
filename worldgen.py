from enum import Enum


class Biome(Enum):
    DEEP_OCEAN = 9
    OCEAN = 8
    BEACH = 7
    PLAINS = 6
    FOREST = 2
    MOUNTAIN = 1
    TALL_MOUNTAIN = 0


biomeMap = {
    Biome.DEEP_OCEAN: (5, 12, 69),      # deep ocean
    Biome.OCEAN: (13, 30, 168),          # ocean
    Biome.BEACH: (222, 204, 155),           # beach
    Biome.PLAINS: (115, 168, 106),          # plains
    Biome.FOREST: (37, 74, 31),             # forest
    Biome.MOUNTAIN: (97, 115, 72),          # mountain
    Biome.TALL_MOUNTAIN: (200, 232, 211)    # tall mountain
}

class Terrain:
    def __init__(self, p: float):
        """

        :param p: Stands for perlin value: Range from 0-1.
        """
        self.perlin_val = p

        print(p)

        if   p >= 0.6: self.biome = Biome.DEEP_OCEAN
        elif p >= 0.55: self.biome = Biome.OCEAN
        elif p >= 0.5: self.biome = Biome.BEACH
        elif p >= 0.4: self.biome = Biome.PLAINS
        elif p >= 0.3: self.biome = Biome.FOREST
        elif p >= 0.2: self.biome = Biome.MOUNTAIN
        elif p >= 0.1: self.biome = Biome.TALL_MOUNTAIN

