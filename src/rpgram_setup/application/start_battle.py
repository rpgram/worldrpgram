import dataclasses

from rpgram_setup.domain.protocols.core import Interactor, I, O


@dataclasses.dataclass
class StartBattleDTO: ...


@dataclasses.dataclass
class BattleStartedDTO: ...


# class StartBattleInteractor(Interactor[StartBattleDTO, BattleStartedDTO]):
#     def execute(self, in_dto: I) -> O:
#         raise NotImplemented
        # return BattleStartedDTO()
