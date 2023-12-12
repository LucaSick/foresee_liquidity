import asyncio
import constants.currency_constants as curr_const
from psql_class import Psql
import uuid
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient


async def main():
    async def handle_evt(msg):
        if '/market/ticker:' in msg['topic']:
            market: str = msg['topic'].split(':')[-1]
            first_coin = market.split('-')[0]
            second_coin = market.split('-')[-1]
            id = uuid.uuid1()
            best_bid = float(msg['data']['bestBid'])
            best_ask = float(msg['data']['bestAsk'])
            spread = (1 - best_bid / best_ask) * 100
            print(f"INFO: {id}, {first_coin}-{second_coin} spread: {spread}")
            psql.push_row(id, first_coin, second_coin, spread)

    client = WsToken()
    ws_client = await KucoinWsClient.create(None, client=client, callback=handle_evt, private=False)
    for currency in curr_const.CURR_ARR:
        await ws_client.subscribe('/market/ticker:' + currency)
    while True:
        print("INFO: Sleeping to keep running")
        await asyncio.sleep(30)


psql = Psql(platform='kucoin')
asyncio.run(main())
