from die import *
from enum import Enum

FREQUENCY_CIRCLE_RADIUS = 2

SETTLEMENT_CIRCLE_RADIUS = 12  # how large a settlement appears on the board'


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


class Hex:
    """Hexagonal tile for Settlers of Catan game"""

    # (x, y) mark the center of the Hex. offsets is to construct the points around the center
    def __init__(self, nodes):
        self.nodes = nodes
        self.points = [node.center for node in self.nodes]
        self.center = (self.points[1][0], int((self.points[4][1] + self.points[1][1])/2))
        self.type = HexType.UNDEFINED
        self.color = self.type.value
        # following 2 will be set w/ set_roll_num (except for CACTUS tile)
        self.text = None
        self.roll_num = None

    def set_type(self, hex_type):
        self.type = hex_type
        self.color = self.type.value

    # set the number which, when rolled, will cause the resource
    # associated w/ this Hex to be collected
    def set_roll_num(self, num):
        self.roll_num = num
        self.text = Text(frequency_font(), str(num), BLACK, self.center[0], self.center[1])

    def deselect(self):
        self.text.deselect()

    def check_for_mouse(self, mouse_pos):
        if self.type is not HexType.CACTUS:
            self.text.check_for_mouse(mouse_pos)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        # now draw the roll_num at the center of the Hex
        if self.text is not None:
            self.text.draw(screen)


