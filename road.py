import pygame
from common import *
class Road:
    """Represents the connections between Nodes"""
    def __init__(self, nodes):
        self.nodes = nodes
        self.owner = None
        self.color = BLACK
        self.regular_color = BLACK

        # where the rect for collision detection gets set up
        if nodes[0].center[0] == nodes[1].center[0]:
            # this road is vertical. hence its collision box needs to
            # be slightly shortened vertically and widened horizontally
            height = int(abs(nodes[0].center[1] - nodes[1].center[1])*.98)
            width = int(height*0.5)
            center_x = nodes[0].center[0]
            center_y = int((nodes[0].center[1] + nodes[1].center[1])/2)
            self.collision_rect = pygame.Rect(0, 0, width, height)
            self.collision_rect.center = (center_x, center_y)
        else:
            # this road is partly horizontal, partly vertical
            # must be
            height = int(abs(nodes[0].center[1] - nodes[1].center[1]))
            width = int(abs(nodes[0].center[0] - nodes[1].center[0]))
            center_x = int((nodes[0].center[0] + nodes[1].center[0])/2)
            center_y = int((nodes[0].center[1] + nodes[1].center[1])/2)
            self.collision_rect = pygame.Rect(0, 0, width, height)
            self.collision_rect.center = (center_x, center_y)

    def deselect(self):
        self.color = self.regular_color

    def check_for_mouse(self, mouse_pos):
        if self.collision_rect.collidepoint(mouse_pos):
            # mouse is over this road, make it white
            self.color = WHITE
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.nodes[0].center, self.nodes[1].center, 5)