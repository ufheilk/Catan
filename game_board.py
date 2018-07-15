from hex_board import HexBoard
from die import Dice

class GameBoard():
    def __init__(self, hex_board_x, hex_board_y, dice_x, dice_y):
        self.hex_board = HexBoard(hex_board_x, hex_board_y)
        self.dice = Dice((dice_x, dice_y))

    def draw(self, screen):
        self.hex_board.draw(screen)
        self.dice.draw(screen)
