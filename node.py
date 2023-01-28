from worldgen import Terrain
class Node:
    def __init__(self, p: float):
        self.perlin_val = p  # A value from 0-1 representing the perlin generated value at this node.
        self.terrain = Terrain(p)
        self.enemies = {}
        self.items = {}
