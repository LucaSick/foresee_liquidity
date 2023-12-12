import psycopg2
import constants.psql_constants as psqlc


class Psql:
    def __init__(self, platform: str):
        if platform != "kucoin" and platform != "binance":
            print("Platform must be either kucoin or binance")
            raise ValueError

        self.platform = platform
        self.conn = psycopg2.connect(database=psqlc.DATABASE,
                                     user=psqlc.USER,
                                     host=psqlc.HOST,
                                     password=psqlc.PASSWORD,
                                     port=psqlc.PORT)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""
            DROP TABLE IF EXISTS {platform}; 
        """)
        self.cur.execute(f"""
        CREATE TABLE {platform}(
            id UUID PRIMARY KEY,
            first_coin_name VARCHAR (10) NOT NULL,
            second_coin_name VARCHAR (10) NOT NULL,
            spread REAL NOT NULL,
            slippage REAL NOT NULL);
        """)
        self.conn.commit()

    def push_row(self, id, first_coin, second_coin, spread, slippage):
        self.cur.execute(f"""
            INSERT INTO {self.platform}(id, first_coin_name, second_coin_name, spread, slippage)
            VALUES ('{id}', '{first_coin}', '{second_coin}', {spread}, {slippage});
        """)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
