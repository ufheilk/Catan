from enum import Enum
import math
import pygame

from common import *
from shapes import Rect
from text import Text, get_font_width, get_font_height

pygame.init()
pygame.font.init()

class Resource(Enum):
    FOREST = DARK_GREEN
    SHEEP = LIGHT_GREEN
    WHEAT = GOLDENROD
    MOUNTAIN = SLATE_GRAY
    REDDISH_ORANGE = ORANGE_RED
    NO_RESOURCE = BLACK


# class representing the rectangle which shows what
# resources the port can trade for
class PortRect:
    width = 42
    height = 27
    color = (255, 255, 255)
    font_type = 'graph-35.ttf'
    font_size = 15

    def __init__(self, x, y, resource):
        self.rect = Rect(PortRect.color, PortRect.height, PortRect.width, (x, y))
        self.resource = resource
        font = pygame.font.Font(PortRect.font_type, PortRect.font_size)
        font_width = get_font_width(font)
        font_height = get_font_height(font)
        if resource == Resource.NO_RESOURCE:
            self.exchange = Text(font, '3', BLACK)
        else:
            self.exchange = Text(font, '2', resource.value)
        self.exchange.rect.x = x - PortRect.width / 2 + 3
        self.exchange.rect.y = y - font_height / 2 + 2

        self.base_text = Text(font, ':1', BLACK)
        self.base_text.rect.x = x - font_width / 2 + 3
        self.base_text.rect.y = y - font_height / 2 + 2

    def draw(self, screen):
        self.rect.draw(screen)
        self.exchange.draw(screen)
        self.base_text.draw(screen)

# class representing a port in Catan
# with two docks coming out of the two nodes it is associated with
# and a boat displaying what can be traded
class Port:
    length = 80
    thickness = 2
    dock_color = (140, 140, 15)

    def __init__(self, point1, point2, theta1, theta2):
        self.dock1_end1 = point1
        self.dock1_end2 = (point1[0] + math.cos(theta1) * Port.length,
                           point1[1] + math.sin(theta1) * Port.length)
        self.dock2_end1 = point2
        self.dock2_end2 = (point2[0] + math.cos(theta2) * Port.length,
                           point2[1] + math.sin(theta2) * Port.length)

    def draw(self, screen):
        pygame.draw.line(screen, port.dock_color, self.dock1_end1, self.dock1_end2,
                         Port.thickness)
        pygame.draw.line(screen, port.dock_color, self.dock2_end1, self.dock2_end2,
                         Port.thickness)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

screen.fill((100, 100, 250))
port = Port((100, 100), (250, 100), math.radians(45), math.radians(180))

p_rect = PortRect(300, 300, Resource.NO_RESOURCE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(1)
    pygame.display.flip()
    port.draw(screen)
    p_rect.draw(screen)
