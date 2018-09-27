from enum import Enum
import math
import pygame

from common import *
from shapes import Rect
from text import Text, get_font_width, get_font_height

pygame.init()
pygame.font.init()


class Resource(Enum):
    """The types of resources that can be traded at a port"""
    FOREST = DARK_GREEN
    SHEEP = LIGHT_GREEN
    WHEAT = GOLDENROD
    MOUNTAIN = SLATE_GRAY
    REDDISH_ORANGE = ORANGE_RED
    ANY_RESOURCE = BLACK


class PortRect(Rect):
    """Represents the rectangle graphic with text to identify port resources"""
    color = (255, 255, 255)
    font_type = 'graph-35.ttf'
    font_size = 15
    num_chars = 3 # number of chars in rect

    def __init__(self, x, y, resource):
        # font setup
        font = pygame.font.Font(PortRect.font_type, PortRect.font_size)
        font_width = get_font_width(font)
        font_height = get_font_height(font)

        margin_multiplier = 0.15
        margin_x = int(font_width * margin_multiplier)
        margin_y = int(font_height * margin_multiplier)
        rect_x = PortRect.num_chars * font_width + 2 * margin_x
        rect_y = font_height + 2 * margin_y

        super().__init__(PortRect.color, rect_y, rect_x, (x, y))

        # setup 'exchange', i.e. the leftmost char of the rect which will
        # be colored based on the resource this port is associated with
        self.resource = resource
        if resource == Resource.ANY_RESOURCE:
            exchange_rate = '3'
        else:
            exchange_rate = '2'
        self.exchange = Text(font, exchange_rate, resource.value)

        self.exchange.rect.x = self.rect.x + margin_x
        self.exchange.rect.y = self.rect.y + margin_y

        # base text always the same ':1' after the exchange rate
        self.base_text = Text(font, ' :1', BLACK)
        margin_adjuster = 2  # to better center text
        self.base_text.rect.x = self.rect.x + margin_x + margin_adjuster
        self.base_text.rect.y = self.rect.y + margin_y

    def get_width(self):
        """Get the width of this object's rect object"""
        return self.rect.width

    def get_height(self):
        """Get the height of this object's rect object"""
        return self.rect.height

    def draw(self, screen):
        """Draw the rect and the exchange rate text"""
        super().draw(screen)
        self.exchange.draw(screen)
        self.base_text.draw(screen)


class Port:
    """Represents a graphical Catan port: two docks coming out of its
    associated nodes and the rectangle of the exchange rate"""
    length = 80
    thickness = 2
    brown = (140, 140, 15)

    def __init__(self, point1, point2, theta1, theta2, box_x, box_y, resource):
        # setup docks as a lines between two points based on angle
        self.dock1_end1 = point1
        self.dock1_end2 = (point1[0] + math.cos(theta1) * Port.length,
                           point1[1] + math.sin(theta1) * Port.length)
        self.dock2_end1 = point2
        self.dock2_end2 = (point2[0] + math.cos(theta2) * Port.length,
                           point2[1] + math.sin(theta2) * Port.length)

        self.dock_draw_color = Port.brown

        # the rectangle displaying the exchange rate
        self.port_rect = PortRect(box_x, box_y, resource)

        # to check for mouse collision
        collision_multiplier = 2
        collision_width = int(self.port_rect.get_width() * collision_multiplier)
        collision_height = int(self.port_rect.get_height() * collision_multiplier)
        self.collision_rect = pygame.rect.Rect(0, 0, collision_width, collision_height)
        self.collision_rect.center = self.port_rect.rect.center

    def select(self):
        """Displays this port as selected"""
        self.dock_draw_color = WHITE

    def deselect(self):
        """Sets the display of this port back to normal"""
        self.dock_draw_color = Port.brown

    def check_for_mouse(self, mouse_pos):
        """Checks if the mouse is sufficiently close to this port
        to consider selecting it"""
        if self.collision_rect.collidepoint(mouse_pos):
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        pygame.draw.line(screen, self.dock_draw_color, self.dock1_end1, self.dock1_end2,
                         Port.thickness)
        pygame.draw.line(screen, self.dock_draw_color, self.dock2_end1, self.dock2_end2,
                         Port.thickness)
        self.port_rect.draw(screen)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

screen.fill((100, 100, 250))
port = Port((100, 100), (250, 100), math.radians(45), math.radians(180), 300, 300, Resource.WHEAT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(1)
        mouse_pos = pygame.mouse.get_pos()

    pygame.display.flip()
    select = port.check_for_mouse(mouse_pos)
    if select:
        select.select()
    port.draw(screen)
