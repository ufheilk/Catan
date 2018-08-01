import pygame

from hex_board import GameHexBoard
from die import Dice
from player_box import PlayerBox
from common import *


class ResourceBox:
    pass


class GameBoard:
    def __init__(self, hex_board_x, hex_board_y, layout, player_box_x, player_box_y,
                 dice_x=100, dice_y=100):
        self.hex_board = GameHexBoard(hex_board_x, hex_board_y, layout)
        self.dice = Dice((dice_x, dice_y))
        self.large_player_box_font = pygame.font.Font('Courier New.ttf', 25)
        self.small_player_box_font = pygame.font.Font('Courier New.ttf', 12)
        self.player_box = PlayerBox(player_box_x, player_box_y, 6, 10, self.large_player_box_font,
                                    self.small_player_box_font, SLATE_GRAY)

    def draw(self, screen):
        self.hex_board.draw(screen)
        self.dice.draw(screen)
        self.player_box.draw(screen)
