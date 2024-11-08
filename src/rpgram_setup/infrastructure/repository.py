from rpgram_setup.domain.protocols.data.players import PlayersMapper


class Repository:
    def __init__(
        self,
        player_mapper: PlayersMapper,
    ): ...
