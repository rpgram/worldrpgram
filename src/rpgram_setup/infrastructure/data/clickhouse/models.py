import uuid
from typing import TypedDict


from rpgram_setup.domain.user_types import BattleId, PlayerId


# engine = create_engine("clickhouse+asynch://localhost:9000/rpgram")
# metadata = MetaData(bind=engine)
#
# Base = get_declarative_base(metadata)
#
#
# class Trade(Base):
#
#     __tablename__ = "trade"
#
#     id = Column(types.UUID, primary_key=True)
#     timestamp = Column(types.Float32)
#     token_units = Column(types.UInt32)
#     good_name = Column(types.String)
#     quantity = Column(types.UInt16)
#     buy = Column(types.Boolean)


class BattleResult(TypedDict):
    battle_id: BattleId
    start_timestamp: float
    end_timestamp: float
    opponent_id: PlayerId
    player_id: PlayerId
    timeout: bool
    winner_id: PlayerId


class Trade(TypedDict):
    id: uuid.UUID
    timestamp: float
    token_units: int
    good_name: str
    quantity: int
    buy: bool
