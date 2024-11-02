class WorldException(Exception):
    """Base RPGram exception"""


class LevelTooLow(WorldException):
    def __str__(self) -> str:
        return """This hero is too young"""


class BalanceTooLow(WorldException):
    def __str__(self) -> str:
        return """Need more gold."""


class BattleContinues(WorldException):
    def __str__(self) -> str:
        return """You are in battle now."""
