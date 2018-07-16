from common import *
import pygame
from math import ceil, sqrt


class Rect:
    """Class to represent rectangle objects to be drawn"""
    def __init__(self, color, height, width, center):
        self.color = color
        self.center = center
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Circle:
    """Class representing a pygame circle, to be used for frequency rating"""
    def __init__(self, color, pos, radius):
        self.regular_color = color
        self.color = color
        # pygame draw will complain if either part of pos is a float
        self.pos = (int(pos[0]), ceil(pos[1]))
        self.radius = radius
        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = pos


    def draw(self, screen):
        if self.color is not None:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)


# CONSTANTS FOR TEXT CLASS
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


class Text:
    """Class representing a pygame text object (surface)"""
    def __init__(self, font, text, color, x, y):
        self.font = font
        self.text = text
        self.color = color
        self.surface = font.render(text, True, color)
        # center the text on x, y
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)
        # setup collision rects
        self.collision_rects = []
        if len(text) == 1:
            main_collision_rect = pygame.Rect(0, 0, self.rect.width*6.9, self.rect.height*3)
        else:
            main_collision_rect = pygame.Rect(0, 0, self.rect.width*3.5, self.rect.height*3)
        main_collision_rect.center = self.rect.center
        self.collision_rects.append(main_collision_rect)

        self.circles = assign_circles_by_frequency(self.rect.center,
                                                   self.rect.bottom - self.rect.top,
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
        screen.blit(self.surface, self.rect)
        for circle in self.circles:
            circle.draw(screen)
