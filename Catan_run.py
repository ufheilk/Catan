import pygame
from game_board import GameBoard
import time

# window dimension
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1250

pygame.init()  # needs to be here so the fonts below can be defined

FRAMES_PER_SECOND = 15

def main():
    # set up window display stuff
    pygame.display.set_caption('Catan')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    game_board = GameBoard(300, 100, WINDOW_WIDTH/2, 100)

    running = True

    time_between_frames = 1/FRAMES_PER_SECOND

    # ~~~~~ MAIN GAME LOOP ~~~~~
    while running:
        screen.fill((100, 100, 200))
        start_time = time.time()

        game_board.draw(screen)
        game_board.hex_board.select(game_board.hex_board.roads)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sleep_time = (start_time + time_between_frames) - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)




if __name__ == '__main__':
    main()
