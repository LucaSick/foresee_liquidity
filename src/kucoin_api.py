import asyncio
import constants.kucoin_constants as kucoin_const
import constants.psql_constants as psql_const
from psql_class import Psql
import uuid
from kucoin.client import Market


async def get_data(market, psql):
    response = client.get_ticker(market)
    id = uuid.uuid1()
    bestAsk = float(response['bestAsk'])
    bestBid = float(response['bestBid'])
    lastPrice = float(response['price'])
    spread = ((bestAsk - bestBid) / bestAsk) * 100
    expected_price = bestBid + (bestAsk - bestBid) * 0.02
    slippage = ((lastPrice - expected_price) / expected_price) * 100
    print(f"Add for {market}")
    psql.push_row(id, market, spread, slippage)
    await asyncio.sleep(10)


async def send_requests(client, psql):
    tasks = []
    for market in kucoin_const.CURR_ARR:
        tasks.append(get_data(market, psql))
    await asyncio.gather(*tasks)
    await send_requests(client, psql)


psql = Psql(psql_const.KUCOIN_PLATFORM)
client = Market()
asyncio.run(send_requests(client, psql))
