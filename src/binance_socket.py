import websocket
import json
import time
import hashlib
import hmac
import constants.binance_constants as bin_const
from urllib.parse import urlencode


websocket.enableTrace(False)


def subscribe_to_klines(wsapp):
    params = []
    for currency in bin_const.CURR_ARR:  # <symbol>@kline_<interval>
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


def on_message(wsapp, message):
    json_message = json.loads(message)
    print(json_message)


def on_error(wsapp, error):
    print(error)


def on_close(wsapp, close_status_code, close_msg):
    print("Connection close")
    print(close_status_code)
    print(close_msg)


def on_ping(wsapp, message):
    print("received ping from server")


def on_pong(wsapp, message):
    print("received pong from server")


if __name__ == "__main__":
    wsapp = websocket.WebSocketApp("wss://stream.binance.com:443/ws/lucas_stream",
                                   on_message=on_message,
                                   on_open=on_open,
                                   on_error=on_error,
                                   on_ping=on_ping,
                                   on_pong=on_pong)
    wsapp.run_forever(ping_interval=40, ping_timeout=30)
