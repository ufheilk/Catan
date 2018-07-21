

class ServerPlayer:
    def __init__(self, player_id, username, color, channel):
        self.username = username
        self.color = color
        self.channel = channel
        self.resources = {'wood': 0, 'sheep': 0, 'wheat': 0, 'reddish-orange': 0,
                          'ore': 0}
        self.victory_points = 0
        self.dev_cards = {'knight': 0, 'road_builder': 0, 'monopoly': 0}


class ClientMyPlayer:
    def __init__(self, username, color):
        self.username = username
        self.color = color
        self.resources = {'wood': 0, 'sheep': 0, 'wheat': 0, 'reddish-orange': 0,
                          'ore': 0}
        self.victory_points = 0
        self.dev_cards = {'knight': 0, 'road_builder': 0, 'monopoly': 0}


class ClientOtherPlayer:
    def __init__(self, username, color):
        self.username = username
        self.color = color
        self.resources = {'wood': 0, 'sheep': 0, 'wheat': 0, 'reddish-orange': 0,
                          'ore': 0}
        # the client should only know about victory points of other players
        # that can be determined by observing the board (e.g. cities, or longest road)
        self.known_victory_points = 0
        # shouldn't be able to see other players dev cards' types
        self.num_dev_cards = 0
        self.knights_played = 0