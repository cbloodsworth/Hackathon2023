from grid import *
from math import floor


def pos_to_grid(pos: tuple[float, float]) -> tuple[int, int]:
    x = (pos[0] - screen_center[0]) // block_size + (grid_width // 2) - 0.5
    y = (pos[1] - screen_center[1]) // block_size + (grid_height // 2) - 0.5
    return floor(x), floor(y)


class Player:
    def __init__(self, position):
        self.backpack = {}
        self.stats = {"health_points": 10, "move_speed": 1}
        self.position = position
        self.grid_pos = pos_to_grid(position)

    def move(self, position):
        self.position[0] += position[0] * self.stats["move_speed"]
        self.position[1] += position[1] * self.stats["move_speed"]
