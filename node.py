from shapes import *


class Node:
    """Node class representing an abstract game node within a web of nodes"""
    def __init__(self):
        self.owner = None
        self.neighbors = []
        self.roads = []
        self.city = False

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def add_road(self, road):
        self.roads.append(road)


SETTLEMENT_CIRCLE_RADIUS = 12  # how large a settlement appears on the board


# for client use. for server node representation see above
class GameNode:
    """Node class representing a node to be drawn on the screen"""

    def __init__(self, center):
        self.center = center
        self.color = None
        self.circle = Circle(None, self.center, SETTLEMENT_CIRCLE_RADIUS)

    def settle(self, color):
        self.color = color
        self.circle.color = color

    def deselect(self):
        self.circle.color = self.color

    def select(self):
        self.circle.color = WHITE

    def check_for_mouse(self, mouse_pos):
        if self.circle.rect.collidepoint(mouse_pos):
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        self.circle.draw(screen)
