import psycopg2
import constants.psql_constants as psql_const


class Psql:
    def __init__(self, platform: str):
        if platform not in psql_const.PLATFORMS:
            print(f"ERROR: Platform must be in {psql_const.PLATFORMS}")
            raise ValueError

        self.platform = platform
        self.conn = psycopg2.connect(database=psql_const.DATABASE,
                                     user=psql_const.USER,
                                     host=psql_const.HOST,
                                     password=psql_const.PASSWORD,
                                     port=psql_const.PORT)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""
            DROP TABLE IF EXISTS {platform}; 
        """)
        self.cur.execute(f"""
        CREATE TABLE {platform}(
            id UUID PRIMARY KEY,
            market VARCHAR (10) NOT NULL,
            spread REAL NOT NULL,
            slippage REAL NOT NULL,
            time_received TIMESTAMP NOT NULL);
        """)
        self.conn.commit()

    def push_row(self, id, market, spread, slippage):
        self.cur.execute(f"""
            INSERT INTO {self.platform}(id, market, spread, slippage, time_received)
            VALUES ('{id}', '{market}', {spread}, {slippage}, NOW()::TIMESTAMP);
        """)
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
