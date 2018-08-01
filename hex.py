from die import *
from enum import Enum
from text import HexText


# fonts
# note they are functions so that pygame needn't be initialized here
def frequency_font():
    return pygame.font.Font('freesansbold.ttf', 25)  # displayed on each hex


# just an enum
class HexType(Enum):
    """Enum class for hex tile types in Catan"""
    # values of enum correspond to the color that the tiles should usually be
    FOREST = DARK_GREEN
    SHEEP = LIGHT_GREEN
    WHEAT = GOLDENROD
    MOUNTAIN = SLATE_GRAY
    REDDISH_ORANGE = ORANGE_RED
    CACTUS = YELLOW
    UNDEFINED = BLACK


# for server use. for client representation of a hex, see below
class Hex:
    """A Catan Hexagon, with associated nodes"""
    def __init__(self, nodes):
        self.nodes = nodes
        self.type = HexType.UNDEFINED
        self.roll_num = None  # will be set for all Hexes except CACTUS tile

    def set_type(self, hex_type):
        self.type = hex_type

    # set the number which must be rolled to collect resources from this hex
    def set_roll_num(self, num):
        self.roll_num = num


FREQUENCY_CIRCLE_RADIUS = 2

SETTLEMENT_CIRCLE_RADIUS = 12  # how large a settlement appears on the board


# for client use. for server representation of a hex, see above
class GameHex:
    """Hexagonal tile to be displayed on board"""

    # (x, y) mark the center of the Hex. offsets is to construct the points around the center
    def __init__(self, nodes):
        self.points = [node.center for node in nodes]
        self.center = (self.points[1][0], int((self.points[4][1] + self.points[1][1])/2))
        self.color = None
        # following will be set (except for CACTUS tile)
        self.text = None

    def set_color(self, color):
        self.color = color

    def set_frequency(self, num):
        self.text = HexText(frequency_font(), str(num), BLACK, self.center[0], self.center[1])

    def deselect(self):
        self.text.deselect()

    def check_for_mouse(self, mouse_pos):
        if self.text is not None:
            self.text.check_for_mouse(mouse_pos)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        # now draw the frequency at the center of the Hex
        if self.text is not None:
            self.text.draw(screen)


