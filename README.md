# foresee_liquidity

Implemented two sockets that retrieve market data for 20 markets on Binance and Kucoin.<br><br>
The data is stored to PostgreSQL, to the database market_db and tables kucoin and binance. Data retrieving was implemented with websocket-client and python-kucoin SDK (another WebSocket and REST solutions) <br><br>
To test the code, copy the source code and run ```docker-compose up -d```. To do that Docker Desktop (for MacOS) should be running. <br>
This command will run the kucoin_socket.py file, which recieves the information from Kucoin. To run other scripts (kucoin_socketV2.py, kucoin_api.py and binance_socket.py) simply change the CMD command in Dockerfile.

