import psycopg2
import constants.psql_constants as psqlc


class Psql:
    def __init__(self, platform: str):
        if platform != "kucoin" and platform != "binance":
            print("ERROR: Platform must be either kucoin or binance")
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
            market VARCHAR (10) NOT NULL,
            spread REAL NOT NULL,
            slippage REAL NOT NULL);
        """)
        self.conn.commit()

    def push_row(self, id, market, spread, slippage):
        self.cur.execute(f"""
            INSERT INTO {self.platform}(id, market, spread, slippage)
            VALUES ('{id}', '{market}', {spread}, {slippage});
        """)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
