from rpgram_setup.domain.protocols.general import Display


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


class NotUnique(WorldException):
    def __init__(self, subject: Display, value: Display):
        self.subject = subject
        self.value = value

    def __str__(self):
        return f"""{self.subject} is not unique({self.value} already exists)."""


class ActionFailed(WorldException):

    def __str__(self):
        return """Unbelievable happens."""


class SomethingIsMissing(WorldException):
    def __init__(self, subject: Display):
        self.subject = subject

    def __str__(self):
        return f"Seems {self.subject} is missing..."


class ValidationError(WorldException):
    def __init__(self, subject: Display, hint: Display | None = None):
        self.subject = subject
        self.hint = hint

    def __str__(self):
        error_text = f"Validation failed for {self.subject}."
        if self.hint:
            error_text += f"Try this: {self.hint}."
        return error_text
