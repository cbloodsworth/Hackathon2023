class Player:
    def __init__(self, position):
        self.backpack = {}
        self.stats = {"health_points": 10, "move_speed": 1}
        self.position = position

    def move(self, position):
        self.position[0] += position[0] * self.stats["move_speed"]
        self.position[1] += position[1] * self.stats["move_speed"]