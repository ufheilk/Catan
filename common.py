from enum import Enum

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)  # FOREST COLOR
LIGHT_GREEN = (0, 200, 0)  # SHEEP COLOR
GOLDENROD = (218, 165, 32)  # WHEAT COLOR
SLATE_GRAY = (112, 128, 144)  # MOUNTAIN COLOR
ORANGE_RED = (240, 69, 0)  # BRICK COLOR
YELLOW = (204, 204, 0)
PURPLE = (110, 0, 110)
PINK = (255, 105, 180)
LIGHT_BLUE = (0, 191, 255)
SILVER = (211, 211, 211)
BROWN = (160, 82, 45)
MAROON = (165, 42, 42)
CLEAR = (1, 1, 1)  # not actually meant to be drawn


class PortResource(Enum):
    """The types of resources that can be traded at a port"""
    FOREST = DARK_GREEN
    SHEEP = LIGHT_GREEN
    WHEAT = GOLDENROD
    MOUNTAIN = SLATE_GRAY
    REDDISH_ORANGE = ORANGE_RED
    ANY_RESOURCE = BLACK


class Resource(Enum):
    """The types of resources that can be traded at a port"""
    FOREST = DARK_GREEN
    SHEEP = LIGHT_GREEN
    WHEAT = GOLDENROD
    MOUNTAIN = SLATE_GRAY
    REDDISH_ORANGE = ORANGE_RED
