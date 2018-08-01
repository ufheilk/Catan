import pygame

from time import sleep

from PodSixNet.Connection import connection, ConnectionListener

from player import ClientMyPlayer

from game_board import GameBoard


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

PLAYER_COLORS = {'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (60, 60, 60),
                 'brown': (160, 82, 45), 'purple': (128, 0, 128), 'yellow': (204, 204, 0)}


class OptionGetter:
    """Utility class used to acquire user's game preferences"""
    max_players = 7

    # determines whether the user would like to host a game or join a game
    @classmethod
    def hosting_preference(cls):
        preference = input('Would you like to [h]ost or [j]oin a game? (Pick one): ')
        while preference.lower() not in ['h', 'host', 'j', 'join']:
            preference = input('Invalid selection. Enter "join" to join or "host" to host: ')
        return preference.lower() in ['h', 'host']

    # is the string a valid int?
    @classmethod
    def is_valid_int(cls, user_input):
        try:
            print(user_input)
            return 1 < int(user_input) < OptionGetter.max_players
        except ValueError or TypeError:
            return False

    @classmethod
    def game_specs(cls):
        # OPTION 1: how many players in this game
        num_players = input('How many players do you want in the game? ')
        while not OptionGetter.is_valid_int(num_players):
            num_players = input('Invalid selection. Number must be between 2 and 6: ')
        num_players = int(num_players)

        # OPTION 2: default tiles or randomize?
        randomize = input('Do you want the board to be randomized? ')
        while randomize.lower() not in ['y', 'yes', 'n', 'no']:
            randomize = input('Invalid selection. Answer [y]es or [n]o ')
        randomize = randomize.lower() in ['y', 'yes']

        return {'num_players': num_players, 'randomize': randomize}

    @classmethod
    def valid_user(cls, username):
        # is the username valid ASCII?
        try:
            username.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return 1 < len(username) < 10

    @classmethod
    def valid_color(cls, color):
        try:
            return PLAYER_COLORS[color.lower()]
        except KeyError:
            return None

    # gets the username and color from the client
    @classmethod
    def user_and_color(cls):
        username = input('Username: ')
        color = input('Color (WHITE BLACK PURPLE BROWN GRAY YELLOW): ')
        while not OptionGetter.valid_user(username) or OptionGetter.valid_color(color) is None:
            if not OptionGetter.valid_user(username):
                username = input('Invalid username selection: ').strip()
            if not OptionGetter.valid_color(color):
                color = input('Invalid color: ')

        # the user has finally managed the herculean task of picking a username and color
        return username, PLAYER_COLORS[color.lower()]


class CatanClient(ConnectionListener):
    """Client for Catan game. Manages all displays"""
    def __init__(self, host='localhost', port=4200):
        pygame.init()

        self.game_board = None
        self.screen = None

        self.game_id = None

        self.my_player = None

        self.other_players = []

        self.Connect((host, port))
        self.server_response = False
        while not self.server_response:
            self.pump()
            sleep(0.01)

        print('You have connected to the central server!')

        # need to keep asking user
        self.accepted_by_server = False
        while not self.accepted_by_server:
            will_host = OptionGetter.hosting_preference()
            game_options = OptionGetter.game_specs()

            # send the server these options
            self.send({'action': 'check_hosting', 'host': will_host,
                       'options': game_options})

            # wait on the server for a response
            self.server_response = False
            print('Waiting on server...')
            while not self.server_response:
                self.pump()
                sleep(0.01)

        print('Ready to play at game: ' + str(self.game_id))

        # user must now pick a username and color that are unique from
        # other players already in the game
        self.accepted_by_server = False
        while not self.accepted_by_server:
            username, color = OptionGetter.user_and_color()
            self.my_player = ClientMyPlayer(username, color)

            # send server this selection
            self.send({'action': 'user_color_selection', 'username': username,
                       'color': color})

            # wait on server for a response
            self.server_response = False
            print('Waiting on server...')
            while not self.server_response:
                self.pump()
                sleep(0.01)

        print('Username and color have been accepted!')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((100, 100, 250))
        # the user's game specs have been accepted by the server.
        # must wait until the max # of players has been reached

    # to improve readability. adds the game id to what is being sent to
    # the server
    def send(self, message):
        if self.game_id is not None:
            message['game_id'] = self.game_id
        connection.Send(message)

    # the server is informing the client that they have connected
    def Network_init(self, data):
        self.server_response = True
        print('Connected to the server...')

    # receive message from server about whether the desired game specifications
    # exist. (note: if user is trying to host, their request will always be
    # accepted)
    def Network_check_hosting(self, data):
        self.server_response = True
        if data['accepted']:
            self.accepted_by_server = True
            self.game_id = data['game_id']

    # the server is informing the client if their username / color choices
    # have already been taken
    def Network_check_user_color(self, data):
        self.server_response = True
        accept_username = data['accept_username']
        accept_color = data['accept_color']
        if accept_username and accept_color:
            # add the client's own player to the sidebar
            self.accepted_by_server = True
            self.game_board.player_box.add_player(self.my_player.username,
                                                  self.my_player.color)
            pygame.display.set_caption('Settlers of Catan')
        elif accept_username and not accept_color:
            print('Color was already taken by another player')
        elif not accept_username and accept_color:
            print('Username was already taken by another player')
        else:
            print('Username and color already taken by another player, lmao')

    # the server is informing the client of the players who are already in the game
    def Network_current_players(self, data):
        for player in data['players']:
            self.game_board.player_box.add_player(player['username'], player['color'])
            print('I have been informed of {}, who is {}'.format(player['username'],
                                                                 player['color']))

    # the server is informing the client of a new player who has joined the game
    def Network_new_player(self, data):
        self.game_board.player_box.add_player(data['username'], data['color'])
        print('I have been informed of {}, who is {}'.format(data['username'],
                                                             data['color']))

    # the server is giving the client the game board layout
    def Network_game_board(self, data):
        layout = data['layout']
        for item in layout:
            print(item)
        self.game_board = GameBoard(200, 200, layout, 950, 0)

    def draw(self, screen):
        self.game_board.draw(screen)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)
        self.game_board.player_box.check_for_mouse(pygame.mouse.get_pos())
        self.draw(self.screen)
        pygame.display.flip()

    # if self.Pump() is called twice in a row events will occur twice,
    # which is bad. use this instead
    def pump(self):
        connection.Pump()
        self.Pump()


if __name__ == '__main__':
    client = CatanClient()
    while True:
        client.pump()
        client.update()
        sleep(0.01)