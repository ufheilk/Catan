import pygame

from common import *
from die import Dice
from hex_board import GameHexBoard
from player import OtherPlayerView
from shapes import NonCenteredRect
from text import SelectableText, get_font_height, get_font_width

pygame.init()

large_font_size = 18
font_type = 'graph-35.ttf'
large_font = pygame.font.Font(font_type, large_font_size)
large_font_height = get_font_height(large_font)

class ResourceRow:
    """A single line of colored text within a ResourceBlock (itself within the sidebar) representing a single resource"""
    
    def __init__(self, x, y, resource, color):
        self.resource = resource
        self.color = color
        self.num_resource = 0  # always start with zero of a resource
        self.text = SelectableText(large_font, self.resource + ': ' + str(self.num_resource), self.color, x, y)

    def check_for_mouse(self, mouse_pos):
       return self.text.check_for_mouse(mouse_pos)

    # change the value of this Row's resource to new
    def update(self, new):
        self.num_resource = new
        self.text.text = self.resource + ': ' + str(self.num_resource)
        # make sure to re-render text
        self.text.render()

    def draw(self, screen):
        self.text.draw(screen)

class ResourceBlock:
    """A block of colored text within the sidebar representing the resources associated with a player"""

    def __init__(self, x, start_y):
        self.resources = []
        y_displacements = [large_font_height * i for i in range(5)] 
        resources = ['Wood', 'Brick', 'Sheep', 'Wheat', 'Ore']
        colors = [DARK_GREEN, ORANGE_RED, LIGHT_GREEN, GOLDENROD, SLATE_GRAY]
        for y_displacement, resource, color in zip(y_displacements, resources, colors):
            self.resources.append(ResourceRow(x, start_y + y_displacement, resource, color))

    def draw(self, screen):
        for resource in self.resources:
            resource.draw(screen)

class SideBar:
    """All the info to be displayed at the side of the screen"""
    x = 875  # left side of the bar
    y = 0  # top of the bar
    background = MAROON
    font_type = 'graph-35.ttf'
    large_font_size = 18
    small_font_size = 15
    normal_header_text_color = WHITE
    normal_text_color = BLACK
    chars_per_line = 15

    def __init__(self, num_players):
        # font stuff
        self.large_font = pygame.font.Font(SideBar.font_type, SideBar.large_font_size)
        self.small_font = pygame.font.Font(SideBar.font_type, SideBar.small_font_size)
        self.large_font_height = get_font_height(self.large_font)
        self.small_font_height = get_font_height(self.small_font)

        # now begin adding Text items to the SideBar from the top to the bottom
        self.player_header = SelectableText(self.large_font, 'Players: ', SideBar.normal_header_text_color,
                                            SideBar.x, SideBar.y)
        self.cur_player_top = SideBar.y + self.large_font_height
        self.players = []

        # players can't be added yet, so skip down and create everything else
        self.cur_top = self.cur_player_top + (self.large_font_height + 3 * self.small_font_height)  \
                                           * num_players

        # resources are the first thing after the players
        self.resources_header = SelectableText(self.large_font, 'Resources: ', SideBar.normal_header_text_color, SideBar.x, self.cur_top)
        self.cur_top += self.large_font_height
        self.resources = ResourceBlock(SideBar.x, self.cur_top)
        self.cur_top += 5 * self.large_font_height  # 5 for the number of different resources

        # next come the development cards
        self.cards_header = SelectableText(self.large_font, 'Dev Cards: ', SideBar.normal_header_text_color,
                                           SideBar.x, self.cur_top)
        self.cur_top += self.large_font_height
        self.cards = self.create_cards()

        # then the actions a user can take when it is their turn
        self.action_header = SelectableText(self.large_font, 'Actions: ', SideBar.normal_header_text_color,
                                            SideBar.x, self.cur_top)
        self.cur_top += self.large_font_height
        self.actions = self.create_actions()

        # finally, create the box that will be in the background
        box_width = SideBar.chars_per_line * get_font_width(self.large_font)
        self.box = NonCenteredRect(SideBar.background, self.cur_top - SideBar.y, box_width,
                                   SideBar.x, SideBar.y)

    # create the 4 different development cards
    def create_cards(self):
        cards = []
        cards.append(SelectableText(self.large_font, 'Knight: 0', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        cards.append(SelectableText(self.large_font, 'Rd. Builder: 0', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        cards.append(SelectableText(self.large_font, 'V. Point: 0', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        cards.append(SelectableText(self.large_font, 'Monopoly: 0', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        return cards

    # create the __ different actions a user can take on their turn
    def create_actions(self):
        actions = []
        actions.append(SelectableText(self.large_font, 'Buy Road', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        actions.append(SelectableText(self.large_font, 'Buy Sett.', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        actions.append(SelectableText(self.large_font, 'Buy City', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        actions.append(SelectableText(self.large_font, 'Buy Dev Card', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        actions.append(SelectableText(self.large_font, 'Use Dev Card', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        actions.append(SelectableText(self.large_font, 'Trade', SideBar.normal_text_color, SideBar.x, self.cur_top))
        self.cur_top += self.large_font_height
        return actions

    # add a player and their associated info to the sidebar under the Players section
    def add_player(self, username, color):
        self.players.append(OtherPlayerView(username, color, self.large_font, self.small_font,
                                            self.large_font_height, self.small_font_height, SideBar.x,
                                            self.cur_player_top))
        self.cur_player_top += self.large_font_height + 3 * self.small_font_height

    # select among players
    def select_player(self, mouse_pos):
        self.select_common(self.players, mouse_pos)

    # select among resources
    def select_resource(self, mouse_pos):
        self.select_common(self.resources.resources, mouse_pos)

    # select among development cards
    def select_card(self, mouse_pos):
        self.select_common(self.cards, mouse_pos)

    # select among player actions
    def select_action(self, mouse_pos):
        self.select_common(self.actions, mouse_pos)

    # utility for selection
    # if the mouse is between 2 text items, they will both try to be highlighted
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

    def deselect(self, category):
        for item in category:
            item.deselect()

    def draw(self, screen):
        self.box.draw(screen)

        self.player_header.draw(screen)
        for player in self.players:
            player.draw(screen)

        self.resources_header.draw(screen)
        self.resources.draw(screen)

        self.cards_header.draw(screen)
        for card in self.cards:
            card.draw(screen)

        self.action_header.draw(screen)
        for action in self.actions:
            action.draw(screen)


class GameBoard:
    """Represents everything to be drawn to the screen"""
    def __init__(self, hex_board_x, hex_board_y, layout, num_players, dice_y=80):
        self.hex_board = GameHexBoard(hex_board_x, hex_board_y, layout)
        self.dice = Dice(self.hex_board.center_x(), dice_y)
        self.sidebar = SideBar(num_players)

    def select_settlement(self, mouse_pos):
        return self.hex_board.select_settlement(mouse_pos)

    def select_road(self, mouse_pos):
        return self.hex_board.select_road(mouse_pos)

    def select_hex(self, mouse_pos):
        return self.hex_board.select_hex(mouse_pos)

    # color the node representing a new settlement
    def new_settlement(self, settlement_index, color):
        self.hex_board.nodes[settlement_index].settle(color)

    # color the road representing a new road
    def new_road(self, road_index, color):
        self.hex_board.roads[road_index].color = color
        self.hex_board.roads[road_index].draw_color = color

    def draw(self, screen):
        self.hex_board.draw(screen)
        self.dice.draw(screen)
        self.sidebar.draw(screen)


