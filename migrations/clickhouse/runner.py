import asyncio
import json
import os

from asynch import connect
from clickhouse import add_ts_key, trade

# Migrations

TRADE = "trade"
RESULTS = "results"
RESULTS_REWORK = "res_rev.2"

STATE_FILE = "state.json"


async def main():
    with open(STATE_FILE) as sf:
        current_state_data = json.load(sf)
    if not isinstance(current_state_data, list):
        current_state_data = []
    # connection = await connect("clickhouse://localhost:9000")
    connection = await connect(os.environ["CH_DSN"])
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("CREATE DATABASE IF NOT EXISTS rpgram")
            # await cursor.execute(results.DOWNGRADE)
            # current_state_data.remove(RESULTS)
            if TRADE not in current_state_data:
                await cursor.execute(trade.UPGRADE)
                current_state_data.append(TRADE)
            if RESULTS_REWORK not in current_state_data:
                await cursor.execute(add_ts_key.UPGRADE)
                current_state_data.append(RESULTS_REWORK)
            # if RESULTS not in current_state_data:
            #     await cursor.execute(results.UPGRADE)
            #     current_state_data.append(RESULTS)
    finally:
        with open(STATE_FILE, "w") as sf:
            json.dump(current_state_data, sf)


if __name__ == "__main__":
    asyncio.run(main())
