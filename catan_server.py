import PodSixNet.Server
import PodSixNet.Channel

from time import sleep

from player import ServerPlayer

class ClientChannel(PodSixNet.Channel.Channel):
    """The interface through which the server receives messages from the client"""
    # when the user wants to validate their hosting / game preferences
    def Network_check_hosting(self, data):
        player_id = data['player_id']
        host = data['host']
        options = data['options']
        options = data['options']
        self._server.check_hosting(host, player_id, options)

    # when the user wants to supply their desired username and color
    def Network_user_color_selection(self, data):
        player_id = data['player_id']
        game_id = data['game_id']
        username = data['username']
        color = data['color']
        self._server.check_user_color(player_id, game_id, username, color)

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
            self.players[player_id].Send({'action': 'check_hosting', 'accepted': False,
                                          'game_id': -1})

        # always accept a new host, as we can always make a new game
        if host:
            self.games.append(Game(options['num_players'], options['randomize']))
            self.players[player_id].Send({'action': 'check_hosting', 'accepted': True,
                                          'game_id': len(self.games) - 1})

        else:
            # this player is trying to join a game. check if a game of their
            # specification exists
            game = self.check_games(options['num_players'], options['randomize'])
            if game is None:
                # no games met the specification, tell user to try again
                self.players[player_id].Send({'action': 'check_hosting', 'accepted': False,
                                              'game_id': -1})
            else:
                # there is a game for the user to join
                game.num_active_players += 1
                self.players[player_id].Send({'action': 'check_hosting', 'accepted': True,
                                              'game_id': self.games.index(game)})
                if game.is_full():
                    # the game has reached the max # of players
                    # start the game
                    pass

    # check if the user's desired username and color have already been taken
    def check_user_color(self, player_id, game_id, username, color):
        game = self.games[game_id]
        valid_user = game.validate_username(username)
        valid_color = game.validate_color(color)
        if valid_user and valid_color:
            # the user has provided all needed information
            # they are finally able to join the game
            game.add_player(player_id, self.players[player_id], username, color)
        self.players[player_id].Send({'action': 'check_user_color',
                                      'accept_username': valid_user,
                                      'accept_color': valid_color})


# each game will depend on the specifications of the initial host
class Game:
    """An individual game of Catan to be played be some number of users"""
    def __init__(self, max_num_players, randomize):
        # the number of players that must be in the game before it starts
        self.max_num_players = max_num_players
        self.randomize = randomize
        # number of players currently connected to this game (start w/ just ho t)
        self.num_active_players = 1
        # mechanism to access all players connected to this game
        self.players = []

    # add the full info of a player into this game
    def add_player(self, player_id, player_channel, username, color):
        # when a player is added to the game, the should first inform the incoming player
        # of all players already connected. Then all already-connected players should
        # be informed of the incoming player
        existing_players = [{'username': player.username, 'color': player.color}
                            for player in self.players]
        player_channel.Send({'action': 'current_players', 'players': existing_players})

        # tell other players about this new player
        for player in self.players:
            player.send({'action': 'new_player', 'username': username,
                         'color': color})

        # now actually add the player
        self.players.append(ServerPlayer(player_id, username, color, player_channel))





    def is_full(self):
        return self.num_active_players == self.max_num_players

    def validate_username(self, username):
        for player in self.players:
            if player.username == username:
                return False
        return True

    def validate_color(self, color):
        for player in self.players:
            if player.color == color:
                return False
        return True


if __name__ == '__main__':
    server = CatanServer()
    while True:
        server.Pump()
        sleep(0.01)