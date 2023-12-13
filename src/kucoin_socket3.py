import websocket
import json
import time
import uuid
import constants.kucoin_constants as kucoin_const
from psql_class import Psql


def on_open(wsapp):
    print("INFO: Connection open")
    for market in kucoin_const.CURR_ARR:
        topic = f'/market/candles:{market}_1hour'
        to_send = {
            'type': 'subscribe',
            'topic': topic,
            'id': int(time.time()),
            'return': True,
            "privateChannel": False,
        }
        print(f"INFO: Subbing to {topic}")
        wsapp.send(json.dumps(to_send))
    print("INFO: All subbed")


def get_data(response):
    market = response['data']['symbol']
    id = uuid.uuid1()
    open = float(response['data']['candles'][1])
    close = float(response['data']['candles'][2])
    # high = float(response['data']['candles'][3])
    # low = float(response['data']['candles'][4])
    spread = ((open - close) / open) * 100
    slippage = (open - close) * 0.02
    return market, id, spread, slippage


def on_message(_wsapp, message):
    response = json.loads(message)
    if (response['type'] == 'welcome'):
        print("INFO: Welcome")
    if (response['type'] == 'ack'):
        print("INFO: Subscription is successfull")
    else:
        if (response.get('data') is None or response['data'].get('candles') is None):
            print(
                f"ERROR: the data was not recieved correctly: {response}")
            return
        market, id, spread, slippage = get_data(response)
        print(
            f"INFO: Retrieving data for symbol {market}")
        psql.push_row(id, market, spread, slippage)
        time.sleep(10)


def on_error(_wsapp, error):
    print(f"ERROR: {error}")


def on_close(_wsapp, close_status_code, close_msg):
    print(f"INFO: Connection closed: {close_status_code}, {close_msg}")


def on_ping(wsapp, message):
    message = message.replace('ping', 'pong')
    wsapp.send(message)


def on_pong(wsapp, _message):
    to_send = {
        "id": str(int(time.time())),
        "type": "ping"
    }
    wsapp.send(json.dumps(to_send))


psql = Psql("kucoin")
wsapp = websocket.WebSocketApp(f'wss://ws-api-spot.kucoin.com/?token={kucoin_const.TOKEN}',
                               on_message=on_message,
                               on_open=on_open,
                               on_error=on_error,
                               on_ping=on_ping,
                               on_pong=on_pong)
wsapp.run_forever(ping_interval=10)
