import pygame

def get_color(r ,g ,b ,a)
    return pygame.Color(r, g, b, a)
class UI:
    def __init__(self):
        self.objects = {}

    def draw_all(self, screen):
        for key in self.objects:
            self.objects[key].draw(screen)
        for key in self.buttons:
            self.buttons[key].draw(screen)


class Object:
    def __init__(self):
        self.pos = [0, 0]
        self.color = pygame.Color(255, 255, 255, 255)


class Box(Object):
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.layer = pygame.Surface((100, 100))

    def draw(self, screen):
        pass


class Textbox(Box):
    def __init__(self, font):
        super().__init__()
        self.text = ""
        self.text_color = (0, 0, 0)
        self.font = font

    def draw(self, screen):
        pass
