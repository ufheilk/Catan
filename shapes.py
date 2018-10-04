from common import *
import pygame
from math import ceil, sqrt
import pygame.gfxdraw

class Rect:
    """Class to represent rectangle objects to be drawn"""
    def __init__(self, color, height, width, center):
        self.color = color
        self.center = center
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class NonCenteredRect:
    """Class to represent rectangle objects to be drawn WITHOUT CENTERING"""
    def __init__(self, color, height, width, x, y):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Circle:
    """Class representing a pygame circle, to be used for frequency rating"""
    def __init__(self, color, pos, radius):
        self.color = color
        # pygame draw will complain if either part of pos is a float
        self.pos = (int(pos[0]), ceil(pos[1]))
        self.radius = radius
        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = pos

    def draw(self, screen):
        if self.color is not None:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)


class Triangle:
    """~t r i a n g l e ( s p e c i f i c a l l y , e q u i l a t e r a l )~"""

    # radius, as in the distance from the center to one of the vertices
    def __init__(self, x, y, radius, color, pointed_up=True):
        if pointed_up:
            self.points = [(x, y - radius), (x - int(radius * sqrt(3)/2), y + int(radius / 2)),
                           (x + int(radius * sqrt(3)/2), y + int(radius / 2))]
        else:
            self.points = [(x - int(radius * sqrt(3)/2), y - int(radius / 2)),
                           (x + int(radius * sqrt(3)/2), y - int(radius / 2)), (x, y + radius)]

        self.color = color

    def draw(self, screen):
        pygame.gfxdraw.aapolygon(screen, self.points, self.color)
        pygame.gfxdraw.filled_polygon(screen, self.points, self.color)




