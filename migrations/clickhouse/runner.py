import asyncio
import json

from asynch import connect

from clickhouse import trade, results

# Migrations

TRADE = 'trade'
RESULTS = 'results'


async def main():
    with open('state.json') as sf:
        current_state_data = json.load(sf)
    if not isinstance(current_state_data, list):
        current_state_data = []
    connection = await connect("clickhouse://localhost:9000")
    try:
        async with connection.cursor() as cursor:
            await cursor.execute('CREATE DATABASE IF NOT EXISTS rpgram')
            if TRADE not in current_state_data:
                await cursor.execute(trade.UPGRADE)
                current_state_data.append(TRADE)
            if RESULTS not in current_state_data:
                await cursor.execute(results.UPGRADE)
                current_state_data.append(RESULTS)
    finally:
        with open('state.json', 'w') as sf:
            json.dump(current_state_data, sf)


if __name__ == '__main__':
    asyncio.run(main())