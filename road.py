import pygame
from common import *


# for server use. for client road representation see below
class Road:
    """Represents the roads connecting nodes"""
    def __init__(self, nodes):
        self.nodes = nodes
        self.owner = None


# for client use. for server road representation see above
class GameRoad:
    """Represents the roads drawn around the hexes in the board"""
    select_color = WHITE

    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.color = BLACK
        self.draw_color = self.color

        # where the rect for collision detection gets set up
        if endpoints[0][0] == endpoints[1][0]:
            # this road is vertical. hence its collision box needs to
            # be slightly shortened vertically and widened horizontally
            height = int(abs(endpoints[0][1] - endpoints[1][1])*.98)
            width = int(height*0.5)
            center_x = endpoints[0][0]
            center_y = int((endpoints[0][1] + endpoints[1][1])/2)
            self.collision_rect = pygame.Rect(0, 0, width, height)
            self.collision_rect.center = (center_x, center_y)
        else:
            # this road is partly horizontal, partly vertical
            # must be
            height = int(abs(endpoints[0][1] - endpoints[1][1]))
            width = int(abs(endpoints[0][0] - endpoints[1][0]))
            center_x = int((endpoints[0][0] + endpoints[1][0])/2)
            center_y = int((endpoints[0][1] + endpoints[1][1])/2)
            self.collision_rect = pygame.Rect(0, 0, width, height)
            self.collision_rect.center = (center_x, center_y)

    def deselect(self):
        self.draw_color = self.color

    def select(self):
        print('reeeeee')
        self.draw_color = WHITE

    def check_for_mouse(self, mouse_pos):
        if self.collision_rect.collidepoint(mouse_pos):
            # mouse is over this road, make it white
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        pygame.draw.line(screen, self.draw_color, self.endpoints[0], self.endpoints[1], 5)
