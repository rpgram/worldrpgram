class WorldException(Exception):
    """Base RPGram exception"""


class LevelTooLow(WorldException):
    def __str__(self):
        return """This hero is too young"""


class BalanceTooLow(WorldException):
    def __str__(self):
        return """Need more gold."""
