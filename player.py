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


class OtherPlayerView:
    """The players view of other players in the game"""
    def __init__(self, username, color, large_font, small_font, large_font_height,
                 small_font_height, x, y):
        self.username = username
        self.color = color

        self.small_font = small_font
        self.small_font_height = small_font_height

        self.name_text = SelectableText(large_font, self.username + ':', self.color, x, y)

        self.x = x
        self.y = y + large_font_height

        self.victory_point_text = None
        self.dev_card_text = None
        self.knights_played_text = None
        self.update({'vp': 0, 'dev': 0, 'knights': 22})

    # updates the text under player based on the dictionary passed
    def update(self, fields):
        y = self.y
        self.victory_point_text = SelectableText(self.small_font, 'Victory Points: ' +
                                                 str(fields['vp']), self.color, self.x, y)
        y += self.small_font_height
        self.dev_card_text = SelectableText(self.small_font, 'Dev Cards: ' + str(fields['dev']),
                                            self.color, self.x, y)
        y += self.small_font_height
        self.knights_played_text = SelectableText(self.small_font, 'Knights Played: ' +
                                                  str(fields['knights']), self.color, self.x, y)

    # deselect all text associated with this player
    def deselect(self):
        text_items = [self.name_text, self.victory_point_text, self.dev_card_text, self.knights_played_text]
        for item in text_items:
            item.deselect()

    # select all text associated with this player
    def select(self):
        text_items = [self.name_text, self.victory_point_text, self.dev_card_text, self.knights_played_text]
        for item in text_items:
            item.select()

    def check_for_mouse(self, mouse_pos):
        selected = False
        text_items = [self.name_text, self.victory_point_text, self.dev_card_text, self.knights_played_text]
        for item in text_items:
            if item.rect.collidepoint(mouse_pos):
                selected = True
        if selected:
            return self
        else:
            self.deselect()
            return None

    def draw(self, screen):
        self.name_text.draw(screen)
        self.victory_point_text.draw(screen)
        self.dev_card_text.draw(screen)
        self.knights_played_text.draw(screen)


