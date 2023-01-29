from worldgen import biome


class Node:
    def __init__(self, e: float, m: float):
        self.elevation = e  # A value from 0-1 representing the perlin generated value at this node.
        self.moisture = m   # A value from 0-1 representing the perlin generated value at this node.
        self.biome = biome(e, m)
        self.enemies = {}
        self.items = []
        self.visited: bool = False
