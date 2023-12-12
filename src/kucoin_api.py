import asyncio
import constants.currency_constants as curr_const
from psql_class import Psql
import uuid
from kucoin.client import Market


async def get_data(market, psql):
    res = client.get_ticker(market)
    first_coin = market.split('-')[0]
    second_coin = market.split('-')[-1]
    id = uuid.uuid1()
    best_bid = float(res['bestBid'])
    best_ask = float(res['bestAsk'])
    spread = (1 - best_bid / best_ask) * 100
    print(f"INFO: {id}, {first_coin}-{second_coin} spread: {spread}")
    psql.push_row(id, first_coin, second_coin, spread)
    await asyncio.sleep(10)


async def send_requests(client, psql):
    tasks = []
    for market in curr_const.CURR_ARR:
        tasks.append(get_data(market, psql))
    await asyncio.gather(*tasks)
    await send_requests(client, psql)


psql = Psql(platform='kucoin')
client = Market()
asyncio.run(send_requests(client, psql))
