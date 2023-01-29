from enum import Enum
from math import floor
from random import randint
from pygame import Color

#### CONSTANTS: CHANGE IF YOU WANT TO MODIFY WORLDGEN

ELEV_OCTAVE = 4  # How large / detailed you want the world. POSITIVE INTEGER, DEFAULT=4
ELEV_POWER = 2.0  # Higher values give higher peaks, lower valleys. POSITIVE FLOAT, DEFAULT=2.0

MOIST_OCTAVE = 4  # Same as above but for moisture.
MOIST_POWER = 2.0

#SEED = [randint(0, 999999) for i in range(6)]  # Randomly generated seeds array. Size 6.
SEED = [0,1,2,3,4,5]

## END CONSTANTS
def biome(elevation: float, moisture: float):
    elevation *= 100
    moisture *= 100

    if elevation < 10: return Biome.DEEP_OCEAN
    if elevation < 16: return Biome.OCEAN
    if elevation < 20: return Biome.BEACH

    if elevation > 80:
        if moisture < 10: return Biome.ASHEN
        if moisture < 20: return Biome.DRY_DESERT
        if moisture < 50: return Biome.TUNDRA
        return Biome.SNOW

    if elevation > 60:
        if moisture < 33: return Biome.TEMPERATE_DESERT
        if moisture < 66: return Biome.OUTBACK
        return Biome.TAIGA

    if elevation > 40:
        if moisture < 16: return Biome.TEMPERATE_DESERT
        if moisture < 66: return Biome.PLAINS
        if moisture < 85: return Biome.WOODLAND
        return Biome.JUNGLE

    if elevation > 20:
        if moisture < 16: return Biome.DESERT
        if moisture < 33: return Biome.PLAINS
        return Biome.TROPICAL


class Biome(Enum):
    # Hex-codes correspond to each biome and are used in the code for maps etc
    DEEP_OCEAN = 0x100
    OCEAN = 0x200
    BEACH = 0x300

    ASHEN = 0x003
    DRY_DESERT = 0x013
    TUNDRA = 0x023
    SNOW = 0x033

    TEMPERATE_DESERT = 0x012
    OUTBACK = 0x022
    TAIGA = 0x032

    PLAINS = 0x011
    WOODLAND = 0x021
    JUNGLE = 0x031

    DESERT = 0x010
    TROPICAL = 0x020


colorMap = {
    Biome.DEEP_OCEAN: 0x50C45,
    Biome.OCEAN: 0x0D1EA8,
    Biome.BEACH: 0xDECC9b,


    Biome.ASHEN: 0x898580,
    Biome.DRY_DESERT: 0xA29F78,
    Biome.TUNDRA: 0xB9D79F,
    Biome.SNOW: 0xBCD7C4,

    Biome.TEMPERATE_DESERT: 0x9EA959,
    Biome.OUTBACK: 0x89A45A,
    Biome.TAIGA: 0x69843A,

    Biome.PLAINS: 0x73A86A,
    Biome.WOODLAND: 0x4A6E44,
    Biome.JUNGLE: 0x006226,

    Biome.DESERT: 0xCEC079,
    Biome.TROPICAL: 0xADC767
}


class Terrain:
    def __init__(self, e: float, m: float):
        """
        e is perlin elevation
        m is perlin moisture
        """

        if e > 1.0:   e = 1.0
        elif e < 0.0: e = 0.0

        # Weird solution, might refactor later.
        # We want to multiply the perlin value by 100 and take the floor to get its integer equivalent.
        # The while loop checks if the "heat value" that corresponds with the perlin val exists, and
        # tries to find the next closest down if not.
        biomeKey = floor(e * 100)

        self.biome = biome(biomeKey)
