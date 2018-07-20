import PodSixNet.Server
import PodSixNet.Channel

from time import sleep


class ClientChannel(PodSixNet.Channel.Channel):
    """The interface through which the server receives messages from the client"""
    # when the user wants to validate their hosting / game preferences
    def Network_check_hosting(self, data):
        player_id = data['player_id']
        host = data['host']
        options = data['options']
        self._server.check_hosting(host, player_id, options)


class CatanServer(PodSixNet.Server.Server):
    """Server for hosting games of Catan"""
    channelClass = ClientChannel
    max_players = 7

    def __init__(self, host='localhost', port=4200):
        print('Server started on ' + host + ' : ' + str(port))
        PodSixNet.Server.Server.__init__(self, localaddr=(host, port))

        self.player_count = 0
        self.players = {}

        self.games = []

    def Connected(self, channel, addr):
        print('New connection with {}'.format(channel))
        self.player_count += 1
        channel.Send({'action': 'init', 'player_id': self.player_count})
        self.players[self.player_count] = channel

    # check all games for a game matching the supplied specifications
    # returns a reference to the game if it matches the specs and isn't full
    def check_games(self, num_players, randomize):
        for game in self.games:
            if game.max_num_players == num_players and game.randomize == randomize:
                if not game.is_full():
                    return game
        return None

    # respond to client about hosting / game preferences
    def check_hosting(self, host, player_id, options):

        # double check that the client hasn't sent faulty info
        if not 1 < options['num_players'] < self.max_players:
            self.players[player_id].Send({'action': 'check_hosting', 'accepted': False})

        # always accept a new host, as we can always make a new game
        if host:
            self.games.append(Game(options['num_players'], options['randomize']))
            self.games[-1].add_player(self.players[player_id])
            self.players[player_id].Send({'action': 'check_hosting', 'accepted': True})
        else:
            # this player is trying to join a game. check if a game of their
            # specification exists
            game = self.check_games(options['num_players'], options['randomize'])
            if game is None:
                # no games met the specification, tell user to try again
                self.players[player_id].Send({'action': 'check_hosting', 'accepted': False})
            else:
                game.add_player(self.players[player_id])
                self.players[player_id].Send({'action': 'check_hosting', 'accepted': True})


# each game will depend on the specifications of the initial host
class Game:
    """An individual game of Catan to be played be some number of users"""
    def __init__(self, max_num_players, randomize):
        # the number of players that must be in the game before it starts
        self.max_num_players = max_num_players
        self.randomize = randomize
        # number of players currently connected to this game
        self.num_active_players = 0
        # mechanism to access all players connected to this game
        self.player_channels = []

    def add_player(self, channel):
        self.player_channels.append(channel)
        self.num_active_players += 1

    def is_full(self):
        return self.num_active_players == self.max_num_players


if __name__ == '__main__':
    server = CatanServer()
    while True:
        server.Pump()
        sleep(0.01)