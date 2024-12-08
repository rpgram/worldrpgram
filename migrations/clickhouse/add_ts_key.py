UPGRADE = """CREATE TABLE IF NOT EXISTS rpgram.battle_results
    (
    battle_id UInt64,
    start_timestamp Nullable(Float32),
    end_timestamp Float32,
    opponent_id  UInt32,
    player_id UInt32,
    timeout bool,
    winner_id UInt32
    ) PRIMARY KEY (battle_id, end_timestamp)"""
