from rpgram_setup.domain.exceptions import WorldException


class BadRequest(WorldException):

    def __init__(self, service: str, details: str):
        self.service = service
        self.details = details

    def __str__(self):
        return f"Cross service interaction error. {self.service} responded with {self.details}."
