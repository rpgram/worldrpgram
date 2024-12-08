from rpgram_setup.domain.exceptions import WorldError


class NotAuthenticatedError(WorldError):
    def __str__(self):
        return """You are not authenticated"""
