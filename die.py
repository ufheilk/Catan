import random
from shapes import *

# how big is the die
DIE_SIDE_LENGTH = 30


# this class is only referenced inside of the Dice class below
class Die:
    """A die object to be drawn onto the screen"""
    def __init__(self, number, x, y):
        self.rect = Rect(WHITE, DIE_SIDE_LENGTH, DIE_SIDE_LENGTH, (x, y))
        self.number = number
        die_circle_size = int(DIE_SIDE_LENGTH / 8)
        self.circles = []
        # now put the circles onto the die
        if number == 1:
            self.circles.append(Circle(BLACK, self.rect.center, die_circle_size))
        elif number == 2:
            center_1 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_2 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            self.circles.append(Circle(BLACK, center_1, die_circle_size))
            self.circles.append(Circle(BLACK, center_2, die_circle_size))
        elif number == 3:
            center_1 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_2 = self.rect.center
            center_3 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            self.circles.append(Circle(BLACK, center_1, die_circle_size))
            self.circles.append(Circle(BLACK, center_2, die_circle_size))
            self.circles.append(Circle(BLACK, center_3, die_circle_size))
        elif number == 4:
            center_1 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_2 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_3 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            center_4 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            self.circles.append(Circle(BLACK, center_1, die_circle_size))
            self.circles.append(Circle(BLACK, center_2, die_circle_size))
            self.circles.append(Circle(BLACK, center_3, die_circle_size))
            self.circles.append(Circle(BLACK, center_4, die_circle_size))
        elif number == 5:
            center_1 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_2 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_3 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            center_4 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            center_5 = self.rect.center
            self.circles.append(Circle(BLACK, center_1, die_circle_size))
            self.circles.append(Circle(BLACK, center_2, die_circle_size))
            self.circles.append(Circle(BLACK, center_3, die_circle_size))
            self.circles.append(Circle(BLACK, center_4, die_circle_size))
            self.circles.append(Circle(BLACK, center_5, die_circle_size))
        elif number == 6:
            center_1 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_2 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] - 2*die_circle_size)
            center_3 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1])
            center_4 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1])
            center_5 = (self.rect.center[0] - 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            center_6 = (self.rect.center[0] + 2*die_circle_size,
                        self.rect.center[1] + 2*die_circle_size)
            self.circles.append(Circle(BLACK, center_1, die_circle_size))
            self.circles.append(Circle(BLACK, center_2, die_circle_size))
            self.circles.append(Circle(BLACK, center_3, die_circle_size))
            self.circles.append(Circle(BLACK, center_4, die_circle_size))
            self.circles.append(Circle(BLACK, center_5, die_circle_size))
            self.circles.append(Circle(BLACK, center_6, die_circle_size))

    def draw(self, screen):
        self.rect.draw(screen)
        for circle in self.circles:
            circle.draw(screen)


# a collection of dice that can be 'rolled' onscreen
# x and y mark the centerpoint between the two dice
class Dice:
    def __init__(self, x, y):
        self.left_die_set = get_dice_set(x - DIE_SIDE_LENGTH, y)
        self.right_die_set = get_dice_set(x + DIE_SIDE_LENGTH, y)
        # the selections are actually displayed on screen
        self.left_selection = self.left_die_set[0]
        self.right_selection = self.right_die_set[0]

    # change the numbers on each die
    def next(self):
        self.left_selection = random.choice([die for die in self.left_die_set
                                            if die is not self.left_selection])

        self.right_selection = random.choice([die for die in self.right_die_set
                                             if die is not self.right_selection])

    def set(self, left, right):
        self.left_selection = self.left_die_set[left]
        self.right_selection = self.right_die_set[right]
        print('left selection now {}'.format(self.left_selection))
        print('right selection now {}'.format(self.right_selection))

    def draw(self, screen):
        self.left_selection.draw(screen)
        self.right_selection.draw(screen)


# returns list of all 6 possible die types
def get_dice_set(x, y):
    return [Die(1, x, y), Die(2, x, y),
            Die(3, x, y), Die(4, x, y),
            Die(5, x, y), Die(6, x, y)]
