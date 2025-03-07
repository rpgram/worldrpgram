from rpgram_setup.domain.exceptions import WorldError


class BadRequest(WorldError):
    def __init__(self, service: str, details: str):
        self.service = service
        self.details = details

    def __str__(self) -> str:
        return f"Cross service interaction error. {self.service} responded with {self.details}."
