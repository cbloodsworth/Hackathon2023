import pygame


class UI:
    def __init__(self):
        self.objects = {}
        self.buttons = {}

    def draw_all(self, screen):
        for key in self.objects:
            self.objects[key].draw(screen)
        for key in self.buttons:
            self.buttons[key].draw(screen)


class Object:
    def __init__(self):
        self.pos = [0, 0]
        self.color = (255, 255, 255, 100)
        self.enabled = True


class Box(Object):
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.layer = pygame.Surface((100, 100))
        self.centered = True
        self.bounds = pygame.Rect(self.pos, self.size)

    def draw(self, screen):
        if self.enabled:
            if self.centered:
                rect_pos = [self.pos[0] - self.size[0] // 2, self.pos[1] - self.size[1] // 2]
            else:
                rect_pos = self.pos
            pygame.draw.rect(screen, pygame.Color(self.color), pygame.Rect(rect_pos, self.size))
            self.bounds = pygame.Rect(rect_pos, self.size)


class Textbox(Box):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont("monospace", 20)
        self.text_centered = True

    def draw(self, screen):
        if self.enabled:
            if self.centered:
                rect_pos = [self.pos[0] - self.size[0] // 2, self.pos[1] - self.size[1] // 2]
            else:
                rect_pos = self.pos
            pygame.draw.rect(screen, pygame.Color(self.color), pygame.Rect(rect_pos, self.size))
            draw_text(screen, self.text, self.text_color, pygame.Rect(rect_pos, self.size), self.font)
            self.bounds = pygame.Rect(rect_pos, self.size)
        else:
            self.bounds = pygame.Rect((0, 0), (0, 0))


# Code adapted from Pygame.org

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        center_adjust_x = rect.left + (rect.width - image.get_width()) // 2
        center_adjust_y = y + (rect.height - font_height) // 2
        surface.blit(image, (center_adjust_x, center_adjust_y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text
