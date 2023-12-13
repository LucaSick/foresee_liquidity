import asyncio
import constants.kucoin_constants as kucoin_const
from psql_class import Psql
import uuid
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient


async def main():
    async def handle(response):
        if '/market/candles:' in response['topic']:
            if (response.get('data') is None or response['data'].get('candles') is None):
                print(
                    f"ERROR: the data was not recieved correctly for {response['topic']}")
                return
            market: str = response['data']['symbol']
            first_coin = market.split('-')[0]
            second_coin = market.split('-')[-1]
            id = uuid.uuid1()
            open = float(response['data']['candles'][1])
            close = float(response['data']['candles'][2])
            # high = float(response['data']['candles'][3])
            # low = float(response['data']['candles'][4])
            spread = ((open - close) / open) * 100
            slippage = (open - close) * 0.02
            print(
                f"INFO: Retrieving data for symbol {first_coin}-{second_coin}")
            psql.push_row(id, first_coin, second_coin, spread, slippage)

    client = WsToken()
    ws_client = await KucoinWsClient.create(None, client=client, callback=handle, private=False)
    for currency in kucoin_const.CURR_ARR:
        await ws_client.subscribe(f'/market/candles:{currency}_3min')
    print("INFO: All subscriptions are successfull")
    while True:
        print("INFO: Sleeping to keep running")
        await asyncio.sleep(30)


psql = Psql(platform='kucoin')
asyncio.run(main())
