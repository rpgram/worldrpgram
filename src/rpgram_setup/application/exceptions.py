from rpgram_setup.domain.exceptions import WorldException


class NotAuthenticated(WorldException):
    def __str__(self):
        return """You are not authenticated"""
