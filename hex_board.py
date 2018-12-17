import pygame

from math import ceil, sqrt
from node import Node, GameNode
from road import Road, GameRoad
from hex import Hex, HexType, GameHex
from random import sample
from player import ServerPlayer

# which nodes are connected by roads
ROAD_NODES_INDICES = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0],
                      [6, 7], [7, 0], [5, 8], [8, 9], [9, 6], [10, 11],
                      [11, 6], [9, 12], [12, 13], [13, 10], [3, 14],
                      [14, 15], [15, 16], [16, 17], [17, 4], [17, 18],
                      [18, 19], [8, 19], [19, 20], [20, 21], [22, 13],
                      [12, 21], [21, 23], [23, 24], [24, 22], [15, 25],
                      [25, 26], [26, 27], [27, 28], [28, 16], [28, 29],
                      [29, 30], [30, 18], [30, 31], [31, 32], [32, 20],
                      [32, 33], [33, 34], [34, 23], [35, 24], [34, 36],
                      [36, 37], [37, 35], [27, 38], [38, 39], [39, 40],
                      [40, 29], [40, 41], [41, 42], [42, 31], [42, 43],
                      [43, 44], [44, 33], [44, 45], [45, 46], [46, 36],
                      [39, 47], [47, 48], [48, 49], [49, 41], [49, 50],
                      [50, 51], [51, 43], [51, 52], [52, 53], [53, 45]]

# describes the nodes relative to each node
NODE_NEIGHBOR_INDICES = [[1, 5, 7],
                         [0, 2],
                         [1, 3],
                         [2, 4, 14],
                         [3, 5, 17],
                         [0, 4, 8],
                         [7, 9, 11],
                         [0, 6],
                         [5, 9, 19],
                         [6, 8, 12],
                         [11, 13],
                         [6, 10],
                         [9, 13, 21],
                         [10, 12, 22],
                         [3, 15],
                         [14, 16, 25],
                         [15, 17, 28],
                         [4, 16, 18],
                         [17, 19, 30],
                         [8, 18, 20],
                         [19, 21, 32],
                         [12, 20, 23],
                         [13, 24],
                         [21, 24, 34],
                         [22, 23, 35],
                         [15, 26],
                         [25, 27],
                         [26, 28, 38],
                         [16, 27, 29],
                         [28, 30, 40],
                         [18, 29, 31],
                         [30, 32, 42],
                         [20, 31, 33],
                         [32, 34, 44],
                         [23, 33, 36],
                         [24, 37],
                         [34, 37, 46],
                         [35, 36],
                         [27, 39],
                         [38, 40, 47],
                         [29, 39, 41],
                         [40, 42, 49],
                         [31, 41, 43],
                         [42, 44, 51],
                         [33, 43, 45],
                         [44, 46, 53],
                         [36, 45],
                         [39, 48],
                         [47, 49],
                         [41, 48, 50],
                         [49, 51],
                         [43, 50, 52],
                         [51, 53],
                         [45, 52]]

NUM_NODES = 54

# node setup (this is ugly, try not to pay it any attention)
# which nodes go to which Hex tiles (via index into main node list)
NODE_INDICES_TO_HEX = [[0, 1, 2, 3, 4, 5],
                        [6, 7, 0, 5, 8, 9],
                        [10, 11, 6, 9, 12, 13],
                        [4, 3, 14, 15, 16, 17],
                        [8, 5, 4, 17, 18, 19],
                        [12, 9, 8, 19, 20, 21],
                        [22, 13, 12, 21, 23, 24],
                        [16, 15, 25, 26, 27, 28],
                        [18, 17, 16, 28, 29, 30],
                        [20, 19, 18, 30, 31, 32],
                        [23, 21, 20, 32, 33, 34],
                        [35, 24, 23, 34, 36, 37],
                        [29, 28, 27, 38, 39, 40],
                        [31, 30, 29, 40, 41, 42],
                        [33, 32, 31, 42, 43, 44],
                        [36, 34, 33, 44, 45, 46],
                        [41, 40, 39, 47, 48, 49],
                        [43, 42, 41, 49, 50, 51],
                        [45, 44, 43, 51, 52, 53]]

# this is the default beginners Catan board layout according to the manual
DEFAULT_CATAN_LAYOUT = [HexType.FOREST, HexType.SHEEP, HexType.WHEAT,
                        HexType.REDDISH_ORANGE, HexType.MOUNTAIN, HexType.REDDISH_ORANGE, HexType.SHEEP,
                        HexType.CACTUS, HexType.FOREST, HexType.WHEAT, HexType.FOREST, HexType.WHEAT,
                        HexType.REDDISH_ORANGE, HexType.SHEEP, HexType.SHEEP, HexType.MOUNTAIN,
                        HexType.MOUNTAIN, HexType.WHEAT, HexType.FOREST]

# default beginners Catan board frequencies
DEFAULT_CATAN_FREQUENCIES = [11, 12, 9,
                             4, 6, 5, 10,
                             0, 3, 11, 4, 8,  # 0 is for CACTUS tile
                             8, 10, 9, 3,
                             5, 2, 6]


# Hex info (Hexagonal geometry stuff for different radii, etc)
HEX_RADIUS = 60
HEX_SIDE_LEN = ceil(HEX_RADIUS / 2 * sqrt(3))  # 52


def create_hex_at(x, y, offsets):
    return [GameNode((x + offset_pair[0], y + offset_pair[1])) for offset_pair in offsets]


# creates the 54 nodes (vertices) making up the board's 19 hexagons
# the catan board has a row of 3 on top, then 4, then 5, then 4, then 3
# NOTE: only for the creation of GameNodes, to be used be client
# Nodes are setup in the constructor of the HexBoard
def setup_nodes(start_x, start_y):

    # looking back at this code, I don't know what inspired me to specify
    # these hex offsets as 'big', as opposed to a small hex offset
    # leaving this for historical relevance
    big_hex_offsets = [(52, -30), (0, -60), (-52, -30), (-52, 30), (0, 60), (52, 30)]

    nodes = []
    # row 1
    cur_x = start_x
    cur_y = start_y
    for i in range(3):
        cur_nodes = create_hex_at(cur_x + i*2*HEX_SIDE_LEN, cur_y, big_hex_offsets)
        for cur_node in cur_nodes:
            if any(node.center == cur_node.center for node in nodes):
                # this node has already been added; do nothing
                pass
            else:
                nodes.append(cur_node)
    # row 2
    cur_x -= HEX_SIDE_LEN
    cur_y += HEX_RADIUS * 3/2
    for i in range(4):
        cur_nodes = create_hex_at(cur_x + i*2*HEX_SIDE_LEN, cur_y, big_hex_offsets)
        for cur_node in cur_nodes:
            if any(node.center == cur_node.center for node in nodes):
                # this node has already been added; do nothing
                pass
            else:
                nodes.append(cur_node)
    # row 3
    cur_x -= HEX_SIDE_LEN
    cur_y += HEX_RADIUS * 3/2
    for i in range(5):
        cur_nodes = create_hex_at(cur_x + i*2*HEX_SIDE_LEN, cur_y, big_hex_offsets)
        for cur_node in cur_nodes:
            if any(node.center == cur_node.center for node in nodes):
                # this node has already been added; do nothing
                pass
            else:
                nodes.append(cur_node)
    # row 4
    cur_x += HEX_SIDE_LEN
    cur_y += HEX_RADIUS * 3/2
    for i in range(4):
        cur_nodes = create_hex_at(cur_x + i*2*HEX_SIDE_LEN, cur_y, big_hex_offsets)
        for cur_node in cur_nodes:
            if any(node.center == cur_node.center for node in nodes):
                # this node has already been added; do nothing
                pass
            else:
                nodes.append(cur_node)
    # row 5
    cur_x += HEX_SIDE_LEN
    cur_y += HEX_RADIUS * 3/2
    for i in range(3):
        cur_nodes = create_hex_at(cur_x + i*2*HEX_SIDE_LEN, cur_y, big_hex_offsets)
        for cur_node in cur_nodes:
            if any(node.center == cur_node.center for node in nodes):
                # this node has already been added; do nothing
                pass
            else:
                nodes.append(cur_node)

    # now setup the roads
    roads = []
    for pair in ROAD_NODES_INDICES:
        endpoint_pair = []
        for item in pair:
            endpoint_pair.append(nodes[item].center)
        roads.append(GameRoad(endpoint_pair))

    return nodes, roads


def load_roads_into_nodes(roads):
    for road in roads:
        for node in road.nodes:
            node.add_road(road)


# constructs grid of Hex objects objects based on the already created
# Node grid (represented as a list of Nodes)
# returns a list of Hex objects
def construct_hexes(nodes, nodes_per_hexes):
    hexes = []
    for node_indices in nodes_per_hexes:
        nodes_in_hex = []
        for node_index in node_indices:
            nodes_in_hex.append(nodes[node_index])
        # all of the Nodes making up the Hex are now assembling. make the Hex
        new_hex = Hex(nodes_in_hex)
        hexes.append(new_hex)
        # let nodes know which hexes they are vertices of
        for node in nodes_in_hex:
            node.add_hex(new_hex)
    return hexes


# constructs grid of GameHex objects
def construct_game_hexes(nodes, nodes_per_hexes):
    hexes = []
    for node_indices in nodes_per_hexes:
        nodes_in_hex = []
        for node_index in node_indices:
            nodes_in_hex.append(nodes[node_index])
        # all of the Nodes making up the Hex are now assembling. make the Hex
        hexes.append(GameHex(nodes_in_hex))
    return hexes


def set_hex_frequencies(hexes, randomize):
    layout = DEFAULT_CATAN_LAYOUT
    if randomize:
        layout = sample(layout, len(layout))
        # if the layout is randomized, we must move the non-zero frequency
        # on the cactus tile to the tile that has the 0 frequency
        for hex_type, frequency in zip(layout, DEFAULT_CATAN_FREQUENCIES):
            if hex_type is HexType.CACTUS and frequency != 0:
                taken_by_cactus = frequency

    for h, hex_type, frequency in zip(hexes, layout, DEFAULT_CATAN_FREQUENCIES):
        h.set_type(hex_type)
        if hex_type is not HexType.CACTUS:
            if frequency == 0:
                # this is the tile who needs the frequency taken by the cactus
                h.set_roll_num(taken_by_cactus)
            else:
                h.set_roll_num(frequency)


# note that here, layout is being sent as a list of colors, so there is no
# need to try to get color values from a HexType enum
def set_game_hex_frequencies(hexes, layout):
    # if the layout is randomized, we must move the non-zero frequency
    # on the cactus tile to the tile that has the 0 frequency
    for hex_color, frequency in zip(layout, DEFAULT_CATAN_FREQUENCIES):
        if HexType(hex_color) is HexType.CACTUS and frequency != 0:
            taken_by_cactus = frequency

    for h, hex_color, frequency in zip(hexes, layout, DEFAULT_CATAN_FREQUENCIES):
        h.set_color(hex_color)
        if HexType(hex_color) is not HexType.CACTUS:
            if frequency == 0:
                h.set_frequency(taken_by_cactus)
            else:
                h.set_frequency(frequency)


# for server use. for client representation of hex board see below
class HexBoard:
    """A collection of interconnected Node and Road objects"""
    def __init__(self, randomize):
        self.nodes = [Node() for i in range(NUM_NODES)]
        # now we want to setup the nodes concept of their neighbors
        for relative_neighbors, node in zip(NODE_NEIGHBOR_INDICES, self.nodes):
            for relative_neighbor in relative_neighbors:
                node.add_neighbor(self.nodes[relative_neighbor])

        # now setup the roads
        self.roads = []
        for pair in ROAD_NODES_INDICES:
            node_pair = []
            for item in pair:
                node_pair.append(self.nodes[item])
            self.roads.append(Road(node_pair))

        load_roads_into_nodes(self.roads)

        self.hexes = construct_hexes(self.nodes, NODE_INDICES_TO_HEX)
        set_hex_frequencies(self.hexes, randomize)

    # turn the list of types of this HexBoard into a format that can be sent over the
    # network to create the user's GameHexBoard
    def serialize_types(self):
        serial_types = []
        for hx in self.hexes:
            serial_types.append(hx.type.value)
        return serial_types

    # checks if the settlement selection (node_index) is
    # 1) not already taken
    # 2) not adjacent to another existing settlement
    def valid_settlement(self, node_index):
        try:
            node = self.nodes[node_index]
        except IndexError:
            # user has sent a bad node_index
            return False
        if node.owner is None:
            valid = True
            for neighbor in node.neighbors:
                if neighbor.owner is not None:
                    valid = False
            return valid
        return False

    # checks if the road selection (road_index) is
    # 1) not already taken
    # 2) adjacent to one of the player's settlements
    # 3) adjacent to a node that is adjacent to another one of the player's road,
    # but only if that node is not owned by a different player
    def valid_road(self, road_index, player):
        try:
            road = self.roads[road_index]
        except IndexError:
            # user has sent bad road_index
            return False
        if road.owner is None:
            for node in road.nodes:
                if node.owner is player:
                    # the player has an adjacent settlement -> good
                    return True
                elif node.owner is None:
                    # check roads adjacent to the road's nodes
                    for other_road in node.roads:
                        if other_road.owner is player:
                            return True
        return False

    # make the player the new owner of the node given by node_index
    def settle(self, node_index, player):
        try:
            node = self.nodes[node_index]
            node.owner = player
        except IndexError:
            # user sent a bad node_index, do nothing
            return

    def set_road(self, road_index, player):
        self.roads[road_index].owner = player


class GameHexBoard:
    def __init__(self, start_x, start_y, layout):
        self.nodes, self.roads = setup_nodes(start_x, start_y)
        self.hexes = construct_game_hexes(self.nodes, NODE_INDICES_TO_HEX)
        set_game_hex_frequencies(self.hexes, layout)
        self.selection = None

    def draw(self, screen):
        for hx in self.hexes:
            hx.draw(screen)
        for road in self.roads:
            road.draw(screen)
        for node in self.nodes:
            node.draw(screen)
        if self.selection is not None:
            self.selection.draw(screen)

    # utility for selection
    # if the mouse is between 2 items, they will both try to be highlighted
    # this must be prevented by taking count of all items that think they are selected
    # and only actually going through with the selection for one of them
    def select_common(self, category, mouse_pos):
        selected = []
        for item in category:
            selection = item.check_for_mouse(mouse_pos)
            if selection:
                selected.append(selection)

        if len(selected) < 2:
            # either 1 thing selected or none
            for item in selected:
                item.select()
        else:
            # 2 (possibly more, but I hope this is not possible) possible selections
            selected[0].select()
            for item in selected[1:]:
                item.deselect()

        # return the selection
        try:
            return selected[0]
        except IndexError:
            return None

    def select_settlement(self, mouse_pos):
        selection = self.select_common(self.nodes, mouse_pos)
        if selection:
            # get index so the node can be communicated to the server
            return self.nodes.index(selection)

    def select_hex(self, mouse_pos):
        selection = self.select_common(self.hexes, mouse_pos)
        if selection:
            # get index so the hex can be communicated to the server
            return self.hexes.index(selection)

    def select_road(self, mouse_pos):
        selection = self.select_common(self.roads, mouse_pos)
        if selection:
            # get index so the road can be communicated to the server
            return self.roads.index(selection)

    def get_selection(self):
        return self.selection

    # deselects the selection
    def deselect(self):
        self.selection.deselect()
        self.selection = None

    # returns the x coordinate of the center of the hex board
    def center_x(self):
        # the 8th node of the hex board is at the center-top, hence why it is being used here
        return self.nodes[7].center[0]
