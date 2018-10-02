# classes for a variety of "dialog" boxes in which the user
# has to select a resource, or some number of resources,
# which is required for some step of the game
import pygame

import common
from shapes import Rect
from text import SelectableText, get_font_width

pygame.init()
pygame.font.init()


class TextRect(Rect):
    """A colored rectangle with centered text in it. That's it."""

    color = common.LIGHT_BLUE
    text_color = common.BLACK

    def __init__(self, x, y, width, height, text, font):
        # setup rect
        super().__init__(TextRect.color, height, width, (x, y))

        # setup text
        self.text = SelectableText(font, text, TextRect.text_color, x, y)
        self.text.rect.center = self.rect.center

    def draw(self, screen):
        super().draw(screen)
        self.text.draw(screen)


class TBox(Rect):
    """Base class for all interactive, boxed prompts which require
    the user to select resource or some number of resources, including
    their own resources and those of other players"""

    color = common.BROWN
    width = 400
    height = 300

    font_type = 'graph-35.ttf'
    font_size = 18

    prompt_box_height = 40
    prompt_box_offset = height / 10

    response_box_height = 40
    response_box_width = 90
    response_box_y_offset = height * 9/10

    ok_box_x_offset = width / 3
    lone_ok_box_x_offset = width / 2
    cancel_box_x_offset = width * 2/3

    def __init__(self, x, y, prompt, allow_cancel):
        super().__init__(TBox.color, TBox.height, TBox.width, (x, y))

        font = pygame.font.Font(TBox.font_type, TBox.font_size)

        # setup prompt
        prompt_width = get_font_width(font) * len(prompt)
        self.prompt = TextRect(x, self.rect.y + TBox.prompt_box_offset, prompt_width,
                               TBox.prompt_box_height, prompt, font)

        # setup response buttons
        if allow_cancel:
            self.ok = TextRect(self.rect.left + TBox.ok_box_x_offset,
                               self.rect.top + TBox.response_box_y_offset,
                               TBox.response_box_width, TBox.response_box_height,
                               'OK', font)
            self.cancel = TextRect(self.rect.left + TBox.cancel_box_x_offset,
                                   self.rect.top + TBox.response_box_y_offset,
                                   TBox.response_box_width, TBox.response_box_height,
                                   'CANCEL', font)
        else:
            self.ok = TextRect(self.rect.left + TBox.lone_ok_box_x_offset,
                               self.rect.top + TBox.response_box_y_offset,
                               TBox.response_box_width, TBox.response_box_height,
                               'OK', font)
            self.cancel = None

    def check_for_mouse(self, mouse_pos):
        if self.ok.text.check_for_mouse(mouse_pos):
            self.ok.text.select()
        if self.cancel:
            if self.cancel.text.check_for_mouse(mouse_pos):
                self.cancel.text.select()

    def draw(self, screen):
        super().draw(screen)
        self.prompt.draw(screen)
        self.ok.draw(screen)
        if self.cancel:
            self.cancel.draw(screen)