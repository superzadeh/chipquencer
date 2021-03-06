import screen
import gui

from modeline import Modeline

import pygame

class ChoiceList(screen.Screen):
    SCROLL_WIDTH = 25
    ITEM_HEIGHT = 25
    font = gui.FONT_BIG

    def __init__(self, choices, modelinetext=''):
        self.scrolling = False
        self.choices = choices
        self.returnkey = modelinetext.lower().replace(' ', '_')
        self.modeline = Modeline()
        self.modeline.strings = [modelinetext]
        self.rects = []
        self.listsurface = pygame.Surface((gui.SCREEN_WIDTH - self.SCROLL_WIDTH,
                                       self.ITEM_HEIGHT * len(choices)))
        self.listsurface.fill(gui.C_LIGHTER)
        self.scrolled = 0 # pixels scrolled
        for i, choice in enumerate(choices):
            rect = pygame.Rect((0, i * self.ITEM_HEIGHT),
                               (gui.SCREEN_WIDTH - self.SCROLL_WIDTH,
                                self.ITEM_HEIGHT))
            self.rects.append(rect)
            pygame.draw.rect(self.listsurface, gui.C_PRIMARY, rect, 1)
            if type(choice) is list:
                text = self.font.render(choice[0], False, gui.C_DARKER)
            else:
                text = self.font.render(choice, False, gui.C_DARKER)
            # FIX: Pseudo centering
            self.listsurface.blit(text, (4, i * self.ITEM_HEIGHT + 7))

    def _update(self, events):
        self.has_changed = True
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                pygame.mouse.get_rel()
                if x < gui.SCREEN_WIDTH - self.SCROLL_WIDTH:
                    index_clicked = (y + self.scrolled) // self.ITEM_HEIGHT
                    if index_clicked >= len(self.choices):
                        return
                    value = None
                    if type(self.choices[index_clicked]) is list:
                        screen.stack.pop(**{self.returnkey: self.choices[index_clicked][1]})
                    else:
                        screen.stack.pop(**{self.returnkey: self.choices[index_clicked]})
                else:
                    self.scrolling = True
            elif e.type == pygame.MOUSEBUTTONUP:
                self.scrolling = False
            if self.scrolling:
                self.has_changed = True
                relx, rely = pygame.mouse.get_rel()
                self.scrolled -= rely * 3
                listheight = len(self.choices) * self.ITEM_HEIGHT - gui.SCREEN_HEIGHT + self.modeline.HEIGHT
                if self.scrolled > 0:
                    self.scrolled = 0
                elif abs(self.scrolled) > listheight:
                    self.scrolled = -listheight

    def _render(self, surface):
        surface.blit(self.listsurface, (0, self.scrolled))
        self.modeline.render(surface)
        return surface
