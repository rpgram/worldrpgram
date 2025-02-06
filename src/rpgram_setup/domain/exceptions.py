from rpgram_setup.domain.protocols.general import Display


class WorldError(Exception):
    """Base RPGram exception"""


class LevelTooLow(WorldError):
    def __str__(self) -> str:
        return """This hero is too young"""


class BalanceTooLow(WorldError):
    def __str__(self) -> str:
        return """Need more gold."""


class BattleContinues(WorldError):
    def __str__(self) -> str:
        return """You are in battle now."""


class NotUniqueError(WorldError):
    def __init__(self, subject: Display, value: Display):
        self.subject = subject
        self.value = value

    def __str__(self) -> str:
        return f"""{self.subject} is not unique({self.value} already exists)."""


class ActionFailedError(WorldError):
    def __str__(self) -> str:
        return """Unbelievable happens."""


class SomethingIsMissingError(WorldError):
    def __init__(self, subject: Display):
        self.subject = subject

    def __str__(self) -> str:
        return f"Seems {self.subject} is missing..."


class ValidationError(WorldError):
    def __init__(self, subject: Display, hint: Display | None = None) -> None:
        self.subject = subject
        self.hint = hint

    def __str__(self) -> str:
        error_text = f"Validation failed for {self.subject}."
        if self.hint:
            error_text += f"Try this: {self.hint}."
        return error_text
