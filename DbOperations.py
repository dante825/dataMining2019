import sqlite3

INSERT_LINK_SQL = '''INSERT INTO Stocks_link (symbol, link, sector) VALUES (?,?,?);'''
INSERT_STOCK = '''INSERT INTO Stocks(date, time, stock_name, stock_code, open, high, low, close, vol, buy_vol, sell_vol)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
VIEW_STOCKS_LINK = '''SELECT * FROM Stocks_link;'''
VIEW_STOCKS = '''SELECT * FROM Stocks;'''
TRUNCATE_STOCKS_LINK = '''DELETE FROM Stocks_link;'''
TRUNCATE_STOCKS = '''DELETE FROM Stocks;'''
DB_LOCATION = 'E:\\development\\repo\\icedTeaSpider\\stockDb.sqlite'
DROP_STOCKS_LINK_TABLE = '''DROP TABLE IF EXISTS Stocks_link;'''
DROP_STOCKS_TABLE = '''DROP TABLE IF EXISTS Stocks;'''
CREATE_STOCKS_LINK_SQL = '''CREATE TABLE Stocks_link (
    symbol TEXT NOT NULL PRIMARY KEY,
    link TEXT,
    sector TEXT
    );
'''
CREATE_STOCKS_TABLE = '''CREATE TABLE Stocks (
    date TEXT,
    time TEXT,
    stock_name TEXT,
    stock_code TEXT,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    vol NUMERIC,
    buy_vol TEXT,
    sell_vol TEXT
    );    
'''


class DbOperations:
    def __init__(self):
        self.conn = sqlite3.connect(DB_LOCATION)

    def create_table(self, drop_script, create_script):
        """
        Create a database table
        :param drop_script: drop the table if exists
        :param create_script: sql script to create the table
        :return: void
        """
        cur = self.conn.cursor()
        cur.execute(drop_script)
        cur.execute(create_script)

    def insert_symlink(self, symbol, link, sector):
        """
        Insert a record into the stocks_link table
        :param symbol: stock symbol
        :param link: the link to the stock page
        :param sector: sector of the stock
        :return: void
        """
        cur = self.conn.cursor()
        cur.execute(INSERT_LINK_SQL, (symbol, link, sector))

    def insert_stocks(self, date, time, name, code, open, high, low, close, vol, buy_vol, sell_vol):
        """
        Inserting a stock details into stock table
        :param date: date last updated
        :param time: time last updated
        :param name: company name
        :param code: the code of the company in KLSE
        :param open: the opening price of the stock on that day
        :param high: the highest price of the stock on that day
        :param low: the lowest price of the stock on that day
        :param close: the closing price of the stock on that day
        :param vol: the volume of the stock on that day
        :param buy_vol: the stock volume bought on that day
        :param sell_vol: the stock volume sold on that day
        :return: void
        """
        cur = self.conn.cursor()
        cur.execute(INSERT_STOCK, (date, time, name, code, open, high, low, close, vol, buy_vol, sell_vol))

    def view_table(self, select_script):
        """
        View the content of a table
        :param select_script: the sql script to select items from the table
        :return: the list of records
        """
        cur = self.conn.cursor()
        cur.execute(select_script)
        result = cur.fetchall()
        return result

    def clear_table(self, truncate_script):
        """
        Clear all the content of the table
        :param truncate_script: the sql script to truncate the table
        :return: void
        """
        cur = self.conn.cursor()
        cur.execute(truncate_script)

    def close_conn(self):
        """
        Commit and close the database connection
        :return: void
        """
        self.conn.commit()
        self.conn.close()


def main():
    db_op = DbOperations()
    # db_op.insert_symlink('sapura', 'star/business/sapura', 'sector')
    # db_op.create_table(DROP_TABLE, CREATE_STOCKS_LINK_SQL)
    # records = db_op.view_table(VIEW_STOCKS_LINK)

    # db_op.create_table(DROP_STOCKS_TABLE, CREATE_STOCKS_TABLE)
    # db_op.insert_stocks('2019-02-10', '7.00', 'sapura holdings', '5211', 10.0, 1.20, 1.01, 1.15, 5200, '5300', '5866')
    # db_op.clear_table(TRUNCATE_STOCKS)
    records = db_op.view_table(VIEW_STOCKS)
    db_op.close_conn()

    print(len(records))
    for record in records:
        print(record)


if __name__ == '__main__':
    main()