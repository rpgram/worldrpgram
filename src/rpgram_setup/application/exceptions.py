from rpgram_setup.domain.exceptions import WorldError


class NotAuthenticatedError(WorldError):
    def __str__(self) -> str:
        return """You are not authenticated"""
