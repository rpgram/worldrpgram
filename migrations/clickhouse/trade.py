UPGRADE = """CREATE TABLE IF NOT EXISTS rpgram.trade
            (
                `id`              UUID,
                `timestamp`       Float32,
                `token_units`     UInt32,
                `good_name`       String,
                `quantity`        UInt16,
                `buy`             Bool
            )    PRIMARY KEY id"""
