from shapes import *

SETTLEMENT_CIRCLE_RADIUS = 12  # how large a settlement appears on the board


class Node:
    """Node class representing vertices in a hexagonal grid"""
    def __init__(self, center):
        self.center = center
        self.owner = None
        self.regular_color = CLEAR
        self.neighbors = []
        self.circle = Circle(CLEAR, self.center, SETTLEMENT_CIRCLE_RADIUS)
        self.roads = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def add_road(self, road):
        self.roads.append(road)

    def settle(self):
        self.circle = Circle(BLACK, self.center, SETTLEMENT_CIRCLE_RADIUS)

    def deselect(self):
        self.circle.color = self.regular_color

    def check_for_mouse(self, mouse_pos):
        if self.circle.rect.collidepoint(mouse_pos):
            self.circle.color = WHITE
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        self.circle.draw(screen)

    def is_settled(self):
        return self.circle is not None
