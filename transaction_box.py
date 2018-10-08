# classes for a variety of "dialog" boxes in which the user
# has to select a resource, or some number of resources,
# which is required for some step of the game
from enum import Enum
import pygame

import common
from shapes import Rect, Triangle
from text import SelectableText, get_font_width, get_font_height

pygame.init()
pygame.font.init()


class ResourceBox(Rect):
    """A rect matched up with a resource, which also decides the box's color"""

    # used in creating larger white box in background to show when box is selected
    outer_box_margin = 1.2

    def __init__(self, x, y, size, resource):
        super().__init__(resource.value, size, size, (x, y))
        self.resource = resource
        self.selection_box = Rect(common.WHITE, size * ResourceBox.outer_box_margin,
                                  size * ResourceBox.outer_box_margin, (x, y))
        self.selected = False

    def draw(self, screen):
        if self.selected:
            self.selection_box.draw(screen)
        super().draw(screen)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def check_for_mouse(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self
        else:
            # don't auto-deselect as selection state might need to be saved
            return None


class ResourceCounter:
    """A colored number for each resource representing how much has been selected
    along with up / down arrows to change how much is selected"""

    arrow_size_modifier = 0.3
    arrow_separation = 0.3
    arrow_color = common.BLACK

    font_x_offset = 0.15  # centering the font intuitively looks off-center :\
    font_y_offset = 0.1

    min_value = 0
    max_value = 15

    arrow_color = common.BLACK

    def __init__(self, x, y, resource, font):
        self.resource = resource
        self.font = font

        # counter number initialization
        self.num = SelectableText(font, '0', resource.value, 0, 0)

        font_height = get_font_height(font)
        font_width = get_font_width(font)
        # store this center location long-term for re-centering
        self.num_center = (int(x + ResourceCounter.font_x_offset * font_width),
                           int(y + ResourceCounter.font_y_offset * font_height))
        self.num.rect.center = self.num_center

        # arrow initialization
        arrow_size = int(font_height * ResourceCounter.arrow_size_modifier)
        arrow_offset = int(font_height/2 + font_height * ResourceCounter.arrow_separation)
        self.up_arrow = Triangle(x, y - arrow_offset, arrow_size, ResourceCounter.arrow_color)
        self.down_arrow = Triangle(x, y + arrow_offset, arrow_size, ResourceCounter.arrow_color,
                                   pointed_up=False)

        # collision rects for detecting mouse / clicks
        self.up_arrow_collision = pygame.rect.Rect(0, 0, arrow_size, arrow_size)
        self.up_arrow_collision.center = (x, y - arrow_offset)
        self.down_arrow_collision = pygame.rect.Rect(0, 0, arrow_size, arrow_size)
        self.down_arrow_collision.center = (x, y + arrow_offset)

    def check_for_mouse(self, mouse_pos, mouse_click):
        """"Checks if the mouse is close enough to either arrows to highlight them,
        and if there was a click updates the counter (assuming bounds not passed)"""
        if self.up_arrow_collision.collidepoint(mouse_pos):
            # mouse is near the up arrow
            self.up_arrow.color = common.WHITE
            if mouse_click:
                cur_val = int(self.num.text)
                new_val = cur_val + 1

                # bounds checking
                if new_val <= ResourceCounter.max_value:
                    if cur_val == 9:
                        # need to re-initialize text obj for centering
                        self.num = SelectableText(self.font, str(new_val),
                                                  self.resource.value, 0, 0)
                        self.num.rect.center = self.num_center

                    else:
                        self.num.text = str(new_val)
                        self.num.deselect()

            # up arrow is being moused over, so down arrow shouldn't be selected
            self.down_arrow.color = ResourceCounter.arrow_color

        elif self.down_arrow_collision.collidepoint(mouse_pos):
            # mouse is near the down arrow
            self.down_arrow.color = common.WHITE
            if mouse_click:
                cur_val = int(self.num.text)
                new_val = cur_val - 1
                if new_val >= ResourceCounter.min_value:
                    if cur_val == 10:
                        # need to re-initialize text obj for centering
                        self.num = SelectableText(self.font, str(new_val),
                                                  self.resource.value, 0, 0)
                        self.num.rect.center = self.num_center

                    else:
                        self.num.text = str(cur_val - 1)
                        self.num.deselect()

            # down arrow is being moused over, so up arrow shouldn't be selected
            self.up_arrow.color = ResourceCounter.arrow_color

        else:
            # mouse is away; deselect all
            self.up_arrow.color = ResourceCounter.arrow_color
            self.down_arrow.color = ResourceCounter.arrow_color

    def draw(self, screen):
        self.up_arrow.draw(screen)
        self.num.draw(screen)
        self.down_arrow.draw(screen)


class ResourcePicker:
    """Graphical interface for user to pick a resource. Consists of 5
    ResourceBoxes"""

    box_separation = 0.5  # boxes separated by half their size

    def __init__(self, x, y, box_size):
        self.resource_boxes = []
        # have a resource box for each of the five resource
        cur_x = x - 2 * box_size - 2 * ResourcePicker.box_separation * box_size
        for resource in common.Resource:
            self.resource_boxes.append(ResourceBox(cur_x, y, box_size, resource))
            cur_x += box_size + ResourcePicker.box_separation * box_size

        self.current_selection = None  # resource user clicked on last

    def check_for_mouse(self, mouse_pos, mouse_clicked):
        for box in self.resource_boxes:
            selection = box.check_for_mouse(mouse_pos)
            if selection:
                selection.select()
                if mouse_clicked:
                    self.current_selection = box
            elif box is not self.current_selection:
                box.deselect()

    # returns what the user has selected
    # if nothing selected: None
    def get_result(self):
        if self.current_selection:
            return self.current_selection.resource

    def draw(self, screen):
        for box in self.resource_boxes:
            box.draw(screen)


class ResourceSelector:
    """Graphical interface for user to select some number of the five types
    of resources"""

    counter_separation = 1.5  # separate counters so they don't overlap

    def __init__(self, x, y, font):
        font_width = get_font_width(font)
        self.counters = []

        # have a counter for each of the five resource
        cur_x = x - 2 * font_width - 2 * ResourceSelector.counter_separation * font_width
        for resource in common.Resource:
            self.counters.append(ResourceCounter(cur_x, y, resource, font))
            cur_x += font_width + ResourceSelector.counter_separation * font_width

    def check_for_mouse(self, mouse_pos, mouse_click):
        for counter in self.counters:
            counter.check_for_mouse(mouse_pos, mouse_click)

    # returns how many of each resource the user has picked
    def get_result(self):
        return {counter.resource: int(counter.num.text) for counter in self.counters}

    def draw(self, screen):
        for counter in self.counters:
            counter.draw(screen)


class TextRect(Rect):
    """A colored rectangle with centered text in it. That's it."""

    color = common.LIGHT_BLUE
    text_color = common.BLACK

    def __init__(self, x, y, width, height, text, font):
        # setup rect
        super().__init__(TextRect.color, height, width, (x, y))

        # setup text
        self.text = SelectableText(font, text, TextRect.text_color, x, y)
        self.text.rect.center = self.rect.center

    def draw(self, screen):
        super().draw(screen)
        self.text.draw(screen)


class TBoxState(Enum):
    OK = 0
    CANCEL = 1
    CONTINUE = 2


class TBox(Rect):
    """Base class for all interactive, boxed prompts which require
    the user to select resource or some number of resources, including
    their own resources and those of other players"""

    color = common.BROWN
    width = 400
    height = 300

    font_type = 'graph-35.ttf'
    font_size = 18

    prompt_box_height = 40
    prompt_box_offset = height / 10

    # response boxes consist of OK, CANCEL boxes
    response_box_height = 40
    response_box_width = 90
    response_box_y_offset = height * 9/10

    ok_box_x_offset = width / 3
    lone_ok_box_x_offset = width / 2  # if there is no cancel button
    cancel_box_x_offset = width * 2/3

    error_text_color = common.BLACK
    error_text_y_offset = height * 7/10

    def __init__(self, x, y, prompt, allow_cancel):
        super().__init__(TBox.color, TBox.height, TBox.width, (x, y))

        self.x = x

        self.font = pygame.font.Font(TBox.font_type, TBox.font_size)

        # setup prompt
        prompt_width = get_font_width(self.font) * len(prompt)
        self.prompt = TextRect(x, self.rect.y + TBox.prompt_box_offset, prompt_width,
                               TBox.prompt_box_height, prompt, self.font)

        # setup response buttons
        if allow_cancel:
            self.ok = TextRect(self.rect.left + TBox.ok_box_x_offset,
                               self.rect.top + TBox.response_box_y_offset,
                               TBox.response_box_width, TBox.response_box_height,
                               'OK', self.font)
            self.cancel = TextRect(self.rect.left + TBox.cancel_box_x_offset,
                                   self.rect.top + TBox.response_box_y_offset,
                                   TBox.response_box_width, TBox.response_box_height,
                                   'CANCEL', self.font)
        else:
            self.ok = TextRect(self.rect.left + TBox.lone_ok_box_x_offset,
                               self.rect.top + TBox.response_box_y_offset,
                               TBox.response_box_width, TBox.response_box_height,
                               'OK', self.font)
            self.cancel = None

        # text for if the user does something bad and should be scolded
        self.error_text = None

    def check_for_mouse(self, mouse_pos, mouse_click):
        """Checks if the mouse is over any of the response buttons. Additionally
        checks for mouse click and will return what the user is trying to do"""
        if self.ok.text.check_for_mouse(mouse_pos):
            self.ok.text.select()
            if mouse_click:
                return TBoxState.OK
        elif self.cancel:
            if self.cancel.text.check_for_mouse(mouse_pos):
                self.cancel.text.select()

                if mouse_click:
                    return TBoxState.CANCEL

        return TBoxState.CONTINUE

    def error(self, text):
        self.error_text = SelectableText(self.font, text, TBox.error_text_color, 0, 0)
        self.error_text.rect.center = (self.x, self.rect.y + TBox.error_text_y_offset)

    def draw(self, screen):
        super().draw(screen)
        self.prompt.draw(screen)
        self.ok.draw(screen)
        if self.cancel:
            self.cancel.draw(screen)
        if self.error_text:
            self.error_text.draw(screen)


class SingleResourceBox(TBox):
    """TBox which asks you to pick a single resource. Used both for monopoly
    and year of plenty development cards"""

    r_box_size = 40  # size of the resource boxes

    def __init__(self, x, y, prompt):
        super().__init__(x, y, prompt, allow_cancel=True)

        self.picker = ResourcePicker(x, y, SingleResourceBox.r_box_size)

    def check_for_mouse(self, mouse_pos, mouse_click):
        self.picker.check_for_mouse(mouse_pos, mouse_click)
        box_state = super().check_for_mouse(mouse_pos, mouse_click)

        if box_state == TBoxState.CONTINUE:
            pass  # user is still deciding
        elif box_state == TBoxState.CANCEL:
            print('*teleports behind you* nothin\' personnel... kid')
        elif box_state == TBoxState.OK:
            # ensure the user has selected something
            user_selection = self.picker.get_result()
            if user_selection:
                print('user has chosen: ' + str(user_selection))
            else:
                self.error('You must choose a resource')

    def draw(self, screen):
        super().draw(screen)
        self.picker.draw(screen)


class SingleCounterBox(TBox):
    """TBox which asks for the user to specify a number of each
    resource. Used for when the player must give up cards to the robber"""

    counter_font = 'graph-35.ttf'
    counter_font_size = 30

    def __init__(self, x, y, prompt):
        super().__init__(x, y, prompt, False)
        font = pygame.font.Font(SingleCounterBox.counter_font,
                                SingleCounterBox.counter_font_size)

        self.selector = ResourceSelector(x, y, font)

    def check_for_mouse(self, mouse_pos, mouse_click):
        self.selector.check_for_mouse(mouse_pos, mouse_click)
        box_state = super().check_for_mouse(mouse_pos, mouse_click)

        if box_state == TBoxState.OK:
            return self.selector.get_result()
        elif box_state == TBoxState.CANCEL:
            pass

    def draw(self, screen):
        super().draw(screen)
        self.selector.draw(screen)


class MultiCounterBox(TBox):
    """Asks user to select two different sets of different numbers of the
    five resources. Used when trading with another player, the bank, or the port"""

    counter_font = 'graph-35.ttf'
    counter_font_size = 20

    counter_offset = 0.35
    
    def __init__(self, x, y, prompt):
        super().__init__(x, y, prompt, True)

        font = pygame.font.Font(MultiCounterBox.counter_font,
                                MultiCounterBox.counter_font_size)

        # center the two selectors at each side of the box
        left_x = x - self.height * MultiCounterBox.counter_offset
        right_x = x + self.height * MultiCounterBox.counter_offset
        self.left_selector = ResourceSelector(left_x, y, font)
        self.right_selector = ResourceSelector(right_x, y, font)

    def check_for_mouse(self, mouse_pos, mouse_click):
        self.left_selector.check_for_mouse(mouse_pos, mouse_click)
        self.right_selector.check_for_mouse(mouse_pos, mouse_click)

        box_state = super().check_for_mouse(mouse_pos, mouse_click)

        if box_state == TBoxState.OK:
            print(self.left_selector.get_result())
            print(self.right_selector.get_result())
        elif box_state == TBoxState.CANCEL:
            print('nothin\' personnel...')


    def draw(self, screen):
        super().draw(screen)
        self.left_selector.draw(screen)
        self.right_selector.draw(screen)

# THE BELOW ARE ALL CHILD CLASSES THAT WILL ACTUALLY BE USED IN-GAME