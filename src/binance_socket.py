import websocket
import json
import time
import uuid
import constants.binance_constants as bin_const
from psql_class import Psql


websocket.enableTrace(False)
psql = Psql("binance")


def subscribe_to_klines(wsapp):
    params = []
    for currency in bin_const.CURR_ARR:
        params.append(f'{currency.lower()}@kline_3m')
    to_send = json.dumps(
        {
            "method": "SUBSCRIBE",
            "params": params,
            "id": 1
        }
    )
    print("Sending message to server:")
    print(to_send)
    time.sleep(1)
    wsapp.send(to_send)


def on_open(wsapp):
    print("connection open")
    subscribe_to_klines(wsapp)


def on_message(_wsapp, message):
    response = json.loads(message)
    if response.get('k') is None:
        print(
            f"ERROR: the data was not recieved correctly for {response.get('e')}")
        return
    market: str = response['s']
    id = uuid.uuid1()
    open = float(response['k']['o'])
    close = float(response['k']['c'])
    # high = float(response['data']['candles'][3])
    # low = float(response['data']['candles'][4])
    spread = ((open - close) / open) * 100
    slippage = (open - close) * 0.02
    print(
        f"INFO: Retrieving data for symbol {market}")
    psql.push_row(id, market, spread, slippage)
    time.sleep(30)


def on_error(_wsapp, error):
    print("Received error")
    print(error)


def on_close(_wsapp, close_status_code, close_msg):
    print("Connection close")
    print(close_status_code)
    print(close_msg)


def on_ping(wsapp, message):
    print("Received ping from server")
    message = message.replace('PING', 'PONG')
    wsapp.send(message)


def on_pong(_wsapp, message):
    print("Received pong from server")
    message = message.replace('PONG', 'PING')
    wsapp.send(message)


if __name__ == "__main__":
    wsapp = websocket.WebSocketApp("wss://stream.binance.com:443/ws/lucas_stream",
                                   on_message=on_message,
                                   on_open=on_open,
                                   on_error=on_error,
                                   on_ping=on_ping,
                                   on_pong=on_pong)
    wsapp.run_forever(ping_interval=40, ping_timeout=30)
