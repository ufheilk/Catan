from text import SelectableText
import pygame


class ServerPlayer:
    """Server view of a player"""
    def __init__(self, channel):
        self.channel = channel
        self.username = None
        self.color = None
        self.resources = {'wood': 0, 'sheep': 0, 'wheat': 0, 'reddish-orange': 0,
                          'ore': 0}
        self.victory_points = 0
        self.dev_cards = {'knight': 0, 'road_builder': 0, 'monopoly': 0}

    def send(self, data):
        self.channel.Send(data)


class ClientMyPlayer:
    """Holds a player's personal info"""
    def __init__(self, username, color):
        self.username = username
        self.color = color
        self.resources = {'wood': 0, 'sheep': 0, 'wheat': 0, 'reddish-orange': 0,
                          'ore': 0}
        self.victory_points = 0
        self.dev_cards = {'knight': 0, 'road_builder': 0, 'monopoly': 0}


class ClientOtherPlayer:
    """The players view of other players in the game"""
    def __init__(self, username, color):
        self.username = username
        self.color = color
        self.num_resources = 0
        # the client should only know about victory points of other players
        # that can be determined by observing the board (e.g. cities, or longest road)
        self.known_victory_points = 0
        # shouldn't be able to see other players dev cards' types
        self.num_dev_cards = 0
        self.knights_played = 0

        self.name_text = None
        self.victory_point_text = None
        self.dev_card_text = None
        self.knights_played_text = None
        self.text_items = None


    def set_text(self, large_font, small_font):
        self.name_text = SelectableText(large_font, self.username + ':', self.color, 0, 0)
        self.victory_point_text = SelectableText(small_font, 'Victory Points: ' +
                                                 str(self.known_victory_points), self.color,
                                                 0, 0)
        self.dev_card_text = SelectableText(small_font, 'Dev Cards: ' + str(self.num_dev_cards),
                                            self.color, 0, 0)
        self.knights_played_text = SelectableText(small_font, 'Knights Played: ' +
                                                  str(self.knights_played), self.color, 0, 0)
        self.text_items = [self.name_text, self.victory_point_text, self.dev_card_text,
                           self.knights_played_text]

    # deselect all text associated with this player
    def deselect(self):
        for item in self.text_items:
            item.deselect()

    def check_for_mouse(self, mouse_pos):
        selected = False
        for item in self.text_items:
            if item.rect.collidepoint(mouse_pos):
                selected = True
        if selected:
            for item in self.text_items:
                item.select()
        else:
            for item in self.text_items:
                item.deselect()

    def draw(self, screen):
        self.name_text.draw(screen)
        self.victory_point_text.draw(screen)
        self.dev_card_text.draw(screen)
        self.knights_played_text.draw(screen)


