import pygame
from common import *
from shapes import Circle


class Text:
    """Base class for text-like objects"""
    def __init__(self, font, text, color):
        self.font = font
        self.text = text
        self.color = color
        self.surface = font.render(text, True, color)
        # center the text on x, y
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class SelectableText(Text):
    """Class for text objects that will light up when moused over (when in certain game states)"""
    def __init__(self, font, text, color, x, y):
        super(SelectableText, self).__init__(font, text, color)
        self.rect.x = x
        self.rect.y = y

    # user had the mouse over this text, but no longer
    def deselect(self):
        self.surface = self.font.render(self.text, True, self.color)

    # see if this text needs to be highlighted (e.g. if the user's mouse is over it)
    def check_for_mouse(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            # mouse is over this text
            self.surface = self.font.render(self.text, True, WHITE)
        else:
            self.deselect()


class HexText(Text):
    """Class for text objects on the Hex tiles (with the frequency rating dots)"""
    def __init__(self, font, text, color, x, y):
        super(HexText, self).__init__(font, text, color)
        self.rect.center = (x, y)
        # setup collision rects
        self.collision_rects = []
        if len(text) == 1:
            main_collision_rect = pygame.Rect(0, 0, self.rect.width * 6.9, self.rect.height * 3)
        else:
            main_collision_rect = pygame.Rect(0, 0, self.rect.width * 3.5, self.rect.height * 3)
        main_collision_rect.center = self.rect.center
        self.collision_rects.append(main_collision_rect)

        self.circles = assign_circles_by_frequency(self.rect.center, self.rect.bottom - self.rect.top,
                                                   int(text))

    def deselect(self):
        self.surface = self.font.render(self.text, True, self.color)
        # change circles back
        for circle in self.circles:
            circle.color = circle.regular_color

    # returns self to be drawn at end if the mouse is selecting self
    def check_for_mouse(self, mouse_pos):
        for collision_rect in self.collision_rects:
            if collision_rect.collidepoint(mouse_pos):
                # the rect is upon us, re-render
                self.surface = self.font.render(self.text, True, WHITE)
                # gotta change little circles below text as well
                for circle in self.circles:
                    circle.color = WHITE
                return self
            else:
                self.deselect()
                return None

    def draw(self, screen):
        super(HexText, self).draw(screen)
        for circle in self.circles:
            circle.draw(screen)


# constants for the HexText class
CIRCLES_PER_FREQUENCY = {2: 1, 12: 1,
                         3: 2, 11: 2,
                         4: 3, 10: 3,
                         5: 4, 9: 4,
                         6: 5, 8: 5}

FREQUENCY_CIRCLE_RADIUS = 2


# determines how many circles a number should have based on its
# frequency and where these circles should be placed
# relative to the center of the text.
# returns a list of Circles
# note: this function is ugly but works, so don't pay it any attention
def assign_circles_by_frequency(center, box_height, frequency):
    # first assign how many circles there should be
    num_circles = CIRCLES_PER_FREQUENCY[frequency]
    circles = []
    circle_y = center[1] + int(box_height*0.75)  # every circle is on the same axis
    distance_between = FREQUENCY_CIRCLE_RADIUS # distance between each circle
    if num_circles == 1:
        circles.append(Circle(BLACK, (center[0], circle_y), FREQUENCY_CIRCLE_RADIUS))
    elif num_circles == 2:
        effective_distance = int(distance_between / 2 + FREQUENCY_CIRCLE_RADIUS)
        circles.append(Circle(BLACK, (int(center[0] - effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (int(center[0] + effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
    elif num_circles == 3:
        effective_distance = int(distance_between + FREQUENCY_CIRCLE_RADIUS*2)
        circles.append(Circle(BLACK, (center[0], circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (center[0] + effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (center[0] - effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
    elif num_circles == 4:
        effective_distance = int(distance_between / 2 + FREQUENCY_CIRCLE_RADIUS)
        circles.append(Circle(BLACK, (int(center[0] - effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (int(center[0] + effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        effective_distance = int(distance_between * 1.5) + int(FREQUENCY_CIRCLE_RADIUS*3)
        circles.append(Circle(BLACK, (int(center[0] - effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (int(center[0] + effective_distance),
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
    elif num_circles == 5:
        effective_distance = int(distance_between + FREQUENCY_CIRCLE_RADIUS*2)
        circles.append(Circle(BLACK, (center[0], circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (center[0] + effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (center[0] - effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        effective_distance = effective_distance * 2
        circles.append(Circle(BLACK, (center[0] + effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
        circles.append(Circle(BLACK, (center[0] - effective_distance,
                                      circle_y), FREQUENCY_CIRCLE_RADIUS))
    return circles