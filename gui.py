import settings

import pygame

pygame.font.init()
FONT_BIG = pygame.font.SysFont("Arial", 16)

class ActionButton:
    """A regular rectangular button."""

    font = FONT_BIG

    def __init__(self, pos, size, text):
        self.text = text
        x, y = pos
        width, height = size
        self.rect = pygame.Rect(x, y, width, height)

    def clicked(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
                return True
        return False

    def render(self, surface):
        pygame.draw.rect(surface, settings.C_PRIMARY, self.rect)
        text = self.font.render(self.text, False, settings.C_LIGHTEST)
        surface.blit(text, (self.rect.x, self.rect.y))

class Counter:
    """A counter which can be incremented or decremented. Cpunter.value is used to
    get the current value.
    """
    font = FONT_BIG

    def __init__(self, pos, height, text, minimum, maximum, start=None):
        """If start is None it will be set to minimum."""
        self.pos = pos
        self.text = text
        self.minimum = minimum
        self.maximum = maximum
        self.height = height
        self.text = self.font.render(text, False, settings.C_LIGHTEST)
        self.dec = ActionButton((self.text.get_width() + pos[0], pos[1]),
                                (height, height), '-')
        self.inc = ActionButton((self.text.get_width() + pos[0] + height * 2, pos[1]),
                                (height, height), '+')
        self.value = start
        if self.value is None:
            self.value = minimum

    def update(self, events):
        if self.dec.clicked(events):
            self.value -= 1
            if self.value < self.minimum:
                self.value = self.maximum
        elif self.inc.clicked(events):
            self.value += 1
            if self.value > self.maximum:
                self.value = self.minimum

    def render(self, surface):
        self.dec.render(surface)
        self.inc.render(surface)
        text = self.font.render((str(self.value)), False, settings.C_LIGHTEST)
        surface.blit(text, (self.text.get_width() +
                            self.pos[0] + self.height, self.pos[1]))
        surface.blit(self.text, self.pos)

class RadioButtons:
    """A set of radio buttons, can get the active index by RadioButtons.selected."""

    font = FONT_BIG

    def __init__(self, pos, size, columns, rows, strings=[], spacing=0):
        if len(strings):
            assert len(strings) == columns * rows
        self.strings = strings
        x, y = pos
        width, height = size
        self.arearect = pygame.Rect(x, y,
                                    (width + spacing) * columns,
                                    (height + spacing) * rows)
        self.rects = []
        self.selected = 0
        for r in range(rows):
            for c in range(columns):
                self.rects.append(pygame.Rect(x + c * (width + spacing),
                                              y + r * (height + spacing),
                                              width,
                                              height))

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and self.arearect.collidepoint(e.pos):
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(e.pos):
                        self.selected = i
                        return self.selected
        return None

    def render(self, surface):
        for i, rect in enumerate(self.rects):
            font_color = settings.C_LIGHTEST
            button_color = settings.C_PRIMARY
            if i == self.selected:
                font_color = settings.C_LIGHTEST
                button_color = settings.C_DARKER
            pygame.draw.rect(surface, button_color, rect)
            try:
                text = self.font.render(self.strings[i], False, font_color)
                surface.blit(text, (rect.x, rect.y))
            except:
                pass

class Slider:
    """A rectangle which is turned into a slider. Slider.get_data() returns the
    percentage filled. The slider will be horizontal or vertical depending on the
    size of the rectangle.
    """
    def __init__(self, rect):
        self.rect = rect
        self.active = False
        self._pixels = 0.0

    def update(self, events, finetune=False):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                self.active = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(e.pos)
                pygame.mouse.get_rel()
        if self.active:
            relx, rely = pygame.mouse.get_rel()
            if finetune:
                rely *= 0.2
            self._pixels -= rely
            if self._pixels < 0:
                self._pixels = 0.0
            elif self._pixels > self.rect.height:
                self._pixels = float(self.rect.height)
            return self.get_data()
        return None

    def render(self, surface):
        pygame.draw.rect(surface, settings.C_PRIMARY, self.rect)
        status = pygame.Rect(self.rect.left,
                             self.rect.bottom - self._pixels,
                             self.rect.width,
                             self._pixels)
        pygame.draw.rect(surface, settings.C_DARKER, status)

    def get_data(self):
        """Return the percentage filled."""
        return self._pixels / self.rect.height

    def set_value(self, value, maximum, minimum=0.0):
        if value > maximum:
            value = maximum
        self._pixels = (float(value - minimum) / (maximum - minimum)) * self.rect.height
