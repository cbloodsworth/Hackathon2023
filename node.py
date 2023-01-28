class Node:
    def __init__(self):
        self.perlin_val: float  # A value from 0-1 representing the perlin generated value at this node.
        self.biome = "Plains"
        self.enemies = {}
        self.items = {}
