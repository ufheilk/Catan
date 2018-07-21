import pygame

from time import sleep

from PodSixNet.Connection import connection, ConnectionListener


# determines whether the user would like to host a game or join a game
def hosting_preference():
    preference = input('Would you like to [h]ost or [j]oin a game? (Pick one): ')
    while preference.lower() not in ['h', 'host', 'j', 'join']:
        preference = input('Invalid selection. Enter "join" to join or "host" to host: ')
    return preference.lower() in ['h', 'host']


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
    

    # is the string a valid int?
    @classmethod
    def is_valid_int(cls, user_input):
        try:
            print(user_input)
            return 1 < int(user_input) < OptionGetter.max_players
        except ValueError or TypeError:
            return False


class CatanClient(ConnectionListener):
    """Client for Catan game. Manages all displays"""
    def __init__(self, host='localhost', port=4200):
        pygame.init()

        self.player_id = None
        self.game_id = None
        self.Connect((host, port))
        self.server_response = False
        while not self.server_response:
            self.pump()
            sleep(0.01)

        print(self.player_id)
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

        # the user's game specs have been accepted by the server.
        # must wait until the max # of players has been reached



    # to improve readability. adds the clients id to the message and
    # sends it to the server
    def send(self, message):
        message['player_id'] = self.player_id
        connection.Send(message)

    def Network_init(self, data):
        self.server_response = True
        self.player_id = data['player_id']

    # receive message from server about whether the desired game specifications
    # exist. (note: if user is trying to host, their request will always be
    # accepted)
    def Network_check_hosting(self, data):
        self.server_response = True
        if data['accepted']:
            self.accepted_by_server = True
            self.game_id = data['game_id']


    # if self.Pump() is called twice in a row events will occur twice,
    # which is bad. use this instead
    def pump(self):
        connection.Pump()
        self.Pump()



if __name__ == '__main__':
    client = CatanClient()
    while True:
        client.Pump()
        connection.Pump()
        sleep(0.01)