import PodSixNet.Server
import PodSixNet.Channel

from time import sleep

from game import Game


class ClientChannel(PodSixNet.Channel.Channel):
    """The interface through which the server receives messages from the client"""
    # when the user wants to validate their hosting / game preferences
    def Network_check_hosting(self, data):
        host = data['host']
        channel = self
        options = data['options']
        self._server.check_hosting(host, channel, options)

    # when the user wants to supply their desired username and color
    def Network_user_color_selection(self, data):
        channel = self
        game_id = data['game_id']
        self._server.delegate_to_game(channel, game_id, 'check_user_color', data)

    # the user wants to select an initial settlement
    def Network_select_settlement(self, data):
        channel = self
        game_id = data['game_id']
        self._server.delegate_to_game(channel, game_id, 'select_settlement', data)

    # the user wants to select an initial road
    def Network_select_road(self, data):
        channel = self
        game_id = data['game_id']
        self._server.delegate_to_game(channel, game_id, 'select_road', data)

    def Network_stop_dice(self, data):
        channel = self
        game_id = data['game_id']
        self._server.delegate_to_game(channel, game_id, 'stop_dice', data)


class CatanServer(PodSixNet.Server.Server):
    """Server for hosting games of Catan"""
    channelClass = ClientChannel
    max_players = 6

    def __init__(self, host='localhost', port=4200):
        print('Server started on ' + host + ' : ' + str(port))
        PodSixNet.Server.Server.__init__(self, localaddr=(host, port))

        self.player_count = 0
        self.players = {}

        self.games = []

    def Connected(self, channel, addr):
        print('New connection with {}'.format(channel))
        self.player_count += 1
        channel.Send({'action': 'init'})

    # check all games for a game matching the supplied specifications
    # returns a reference to the game if it matches the specs and isn't full
    def check_games(self, num_players, randomize):
        for game in self.games:
            if game.max_num_players == num_players and game.randomize == randomize:
                if not game.is_full():
                    return game
        return None

    # respond to client about hosting / game preferences
    def check_hosting(self, host, channel, options):

        # double check that the client hasn't sent faulty info
        if not 1 < options['num_players'] <= self.max_players:
            channel.Send({'action': 'check_hosting', 'accepted': False, 'game_id': -1})

        # always accept a new host, as we can always make a new game
        elif host:
            self.games.append(Game(options['num_players'], options['randomize']))
            self.games[-1].add_player(channel)
            channel.Send({'action': 'check_hosting', 'accepted': True,
                          'game_id': len(self.games) - 1})

        else:
            # this player is trying to join a game. check if a game of their
            # specification exists
            game = self.check_games(options['num_players'], options['randomize'])
            if game is None:
                # no games met the specification, tell user to try again
                channel.Send({'action': 'check_hosting', 'accepted': False,
                              'game_id': -1})
            else:
                # there is a game for the user to join
                # note that the game's # of active players increases
                # so that their place in the game is reserved, but their
                # actual player object (w/ username, color) hasn't been added yet
                game.add_player(channel)
                channel.Send({'action': 'check_hosting', 'accepted': True,
                              'game_id': self.games.index(game)})

    # check if the user's desired username and color have already been taken
    def check_user_color(self, channel, game_id, data):
        game = self.games[game_id]
        game.handle_network(channel, 'check_user_color', data)

    # to handle user input when the game has already been set up
    def delegate_to_game(self, channel, game_id, action, data):
        try:
            game = self.games[game_id]
            game.handle_network(channel, action, data)
        except IndexError:
            # the user sent a faulty game id, so ignore this
            return


if __name__ == '__main__':
    server = CatanServer()
    while True:
        server.Pump()
        sleep(0.01)
