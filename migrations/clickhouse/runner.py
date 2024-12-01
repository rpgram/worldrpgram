import asyncio
import json

from asynch import connect


async def main():
    with open('state.json') as sf:
        current_state_data = json.load(sf)
    if not isinstance(current_state_data, list):
        current_state_data = []
    connection = await connect("clickhouse://localhost:9000")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute('CREATE DATABASE IF NOT EXISTS rpgram')
            if 'trade' not in current_state_data:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS rpgram.trade
            (
                `id`              UUID,
                `timestamp`       Float32,
                `token_units`     UInt32,
                `good_name`       String,
                `quantity`        UInt16,
                `buy`             Bool
            )    PRIMARY KEY id
            """)
            current_state_data.append('trade')
    finally:
        with open('state.json', 'w') as sf:
            json.dump(current_state_data, sf)


if __name__ == '__main__':
    asyncio.run(main())