from shapes import NonCenteredRect
from text import SelectableText, get_font_width, get_font_height
from player import ClientOtherPlayer, ClientMyPlayer
from common import *


class PlayerBox:
    """Box that holds all the usernames of the players in the game"""
    def __init__(self, x, y, max_num_players, chars_per_line, large_font, small_font,
                 background_color):
        self.x = x
        self.y = y
        self.max_num_players = max_num_players
        self.chars_per_line = chars_per_line
        self.large_font = large_font
        self.small_font = small_font
        self.large_font_height = get_font_height(large_font)
        self.small_font_height = get_font_height(small_font)
        large_font_width = get_font_width(large_font)
        small_font_width = get_font_width(small_font)
        box_height = self.large_font_height * (max_num_players + 1) + self.small_font_height * max_num_players * 3
        box_width = large_font_width * chars_per_line
        self.box = NonCenteredRect(background_color, box_height, box_width, x, y)
        # note: title_text is a SelectableText but will never actually be selected
        self.title_text = SelectableText(large_font, "Players: ", WHITE, self.x, self.y)
        self.current_top = y + self.large_font_height  # where the next text item should go
        self.players = []

    def add_player(self, player_username, player_color):
        new_player = ClientOtherPlayer(player_username, player_color)
        new_player.set_text(self.large_font, self.small_font)

        # set up where the info regarding this player will be displayed
        # inside the player box
        # 1st, all the new text should be at the same x position as the box
        new_player.name_text.rect.x = self.x
        new_player.victory_point_text.rect.x = self.x
        new_player.dev_card_text.rect.x = self.x
        new_player.knights_played_text.rect.x = self.x

        # 2nd, heights have to be arranged, noting the different font sizes
        new_player.name_text.rect.y = self.current_top
        self.current_top += self.large_font_height
        new_player.victory_point_text.rect.y = self.current_top
        self.current_top += self.small_font_height
        new_player.dev_card_text.rect.y = self.current_top
        self.current_top += self.small_font_height
        new_player.knights_played_text.rect.y = self.current_top
        self.current_top += self.small_font_height

        self.players.append(new_player)

    def check_for_mouse(self, mouse_pos):
        for player in self.players:
            player.check_for_mouse(mouse_pos)

    def draw(self, screen):
        self.box.draw(screen)
        self.title_text.draw(screen)
        for player in self.players:
            player.draw(screen)




