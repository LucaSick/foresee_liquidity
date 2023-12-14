import asyncio
import constants.kucoin_constants as kucoin_const
import constants.psql_constants as psql_const
from psql_class import Psql
import uuid
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient


async def main():
    def get_data(response):
        market = response['topic'].split(':')[-1]
        id = uuid.uuid1()
        bestAsk = float(response['data']['bestAsk'])
        bestBid = float(response['data']['bestBid'])
        lastPrice = float(response['data']['price'])
        spread = ((bestAsk - bestBid) / bestAsk) * 100
        expected_price = bestBid * 1.02
        slippage = ((lastPrice - expected_price) / expected_price) * 100
        return market, id, spread, slippage

    async def handle(response):
        if '/market/ticker:' in response['topic']:
            if response.get('data') is None:
                print(
                    f"ERROR: the data was not recieved correctly: {response}")
                return
            market, id, spread, slippage = get_data(response)
            print(
                f"INFO: Retrieving data for symbol {market}")
            psql.push_row(id, market, spread, slippage)

    client=WsToken()
    ws_client=await KucoinWsClient.create(None, client=client, callback=handle, private=False)
    await ws_client.subscribe(f"/market/ticker:{','.join(kucoin_const.CURR_ARR)}")
    print("INFO: Subscriptions were successfull")
    while True:
        print("INFO: Sleeping to keep running")
        await asyncio.sleep(30)


psql=Psql(psql_const.KUCOIN_PLATFORM)
asyncio.run(main())
