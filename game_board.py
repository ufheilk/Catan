from hex_board import GameHexBoard
from die import Dice


class GameBoard():
    def __init__(self, hex_board_x, hex_board_y, layout, dice_x=100, dice_y=100):
        self.hex_board = GameHexBoard(hex_board_x, hex_board_y, layout)
        self.dice = Dice((dice_x, dice_y))

    def draw(self, screen):
        self.hex_board.draw(screen)
        self.dice.draw(screen)
