import node


class Grid:
    def __init__(self):
        self.nodes = {}

    def generate_grid(self, length, height):
        for x in range(length):
            column = {}
            for y in range(height):
                column[y] = node.Node()
            self.nodes[x] = column
