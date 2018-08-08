from hex_board import HexBoard
from enum import Enum
from player import ServerPlayer


# represents the different states that the game can be in
class GameState(Enum):
    PLAYER_SETUP = 0
    SETTLEMENT_SETUP = 1
    NEW_TURN = 2
    GET_CARDS = 3
    GET_TILE = 4
    GET_PLAYER = 5
    PLAYER_TURN = 6
    TRADE_MESSAGE = 7
    END_GAME = 8


# each game will depend on the specifications of the initial host
class Game:
    """An individual game of Catan to be played be some number of users"""
    def __init__(self, max_num_players, randomize):
        # the number of players that must be in the game before it starts
        self.max_num_players = max_num_players

        self.randomize = randomize

        # number of players currently connected to this game (start w/ just host)
        self.num_active_players = 0
        # mechanism to access all players connected to this game
        self.players = []

        self.hex_board = HexBoard(randomize)

        self.state = GameState.PLAYER_SETUP
        self.cur_player = None  # whose turn is it?

        # for visibility, define the fields which are going to be used only
        # in the context of the various state functions
        # used in SETTLEMENT_SETUP:
        self.select_settlement = True
        self.second_round = False

        self.state_methods = {GameState.PLAYER_SETUP: self.add_player_info}

    # handles incoming messages / actions from players
    def handle_network(self, channel, action_name, data):
        player = self.get_player(channel)
        if player is not None:
            # the player who sent this is actually in the game
            self.state_methods[self.state](player, action_name, data)

    # add a player into this game
    def add_player(self, player_channel):
        self.num_active_players += 1

        # now actually add the player
        self.players.append(ServerPlayer(player_channel))

    # to add player username and color info
    # called when in the PLAYER_SETUP state
    def add_player_info(self, new_player, action_name, data):
        try:
            username = data['username']
            color = data['color']
        except IndexError:
            pass

        valid_username = self.validate_username(username)
        valid_color = self.validate_color(color)

        if valid_username and valid_color:
            # new player is ready to be added
            new_player.username = username
            new_player.color = color

            # give new player the game board setup
            new_player.send({'action': 'game_board',
                             'layout': self.hex_board.serialize_types()})

            # when a player is added to the game, the should first inform the incoming player
            # of all players already connected. Then all already-connected players should
            # be informed of the incoming player
            existing_players = [{'username': player.username, 'color': player.color}
                                for player in self.players if player is not new_player]
            new_player.send({'action': 'current_players', 'players': existing_players})

            # tell other players about this new player
            for player in self.players:
                if player is not new_player:
                    player.send({'action': 'new_player', 'username': username,
                                 'color': color})

        # tell the user whether their choices of username / color have already
        # been taken
        new_player.send({'action': 'check_user_color', 'accept_username': valid_username,
                         'accept_color': valid_color})

        # this might be the last player to have their info accepted
        # check if it is time to go to the next state and actually start the game
        if self.game_ready():
            self.state = GameState.SETTLEMENT_SETUP
            # following 2 fields will be used by SETTLEMENT_SETUP's state function
            self.select_settlement = True
            self.second_round = False
            self.cur_player = self.players[0]
            # tell the first player that they need to select a settlement
            self.cur_player.send({'action': 'select_settlement'})
            # tell everyone else to wait
            self.broadcast_wait()

    # checks if the game is ready to start, i.e. if the game is full and
    # all players have their username and color
    def game_ready(self):
        if self.is_full():
            for player in self.players:
                if player.username is None or player.color is None:
                    return False  # someone hasn't set their user / color
            return True
        return False

    def is_full(self):
        return self.num_active_players == self.max_num_players

    # has somebody taken this username?
    def validate_username(self, username):
        for player in self.players:
            if player.username == username:
                return False
        return True

    # has somebody taken this color?
    def validate_color(self, color):
        for player in self.players:
            if player.color == color:
                return False
        return True

    # get player from channel
    def get_player(self, channel):
        for player in self.players:
            if player.channel == channel:
                return player
        return None

    # get the next player in the rotation from the current player
    # tries to get the next in line, if that fails the array has been stepped out
    # of, so go back to the beginning
    def get_next_player(self):
        try:
            return self.players[self.players.index(self.cur_player)]
        except IndexError:
            return self.players[0]

    # sends the wait message to all players besides the current player
    def broadcast_wait(self):
        for player in self.players:
            if player is not self.cur_player:
                player.send({'action': 'wait', 'cur_player': self.cur_player.username})