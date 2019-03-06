import psycopg2
from configparser import ConfigParser
import locale
import logging

# Setup the log level
logging.basicConfig(level=logging.INFO)

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

INSERT_LINK_SQL = '''INSERT INTO Stocks_link (symbol, link, sector) VALUES (%s,%s,%s);'''
INSERT_STOCK = '''INSERT INTO stocks (date, time, stock_code, stock_name, open, high, low, close, vol, buy_vol, 
        sell_vol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
VIEW_STOCKS_LINK = '''SELECT * FROM Stocks_link;'''
VIEW_STOCKS = '''SELECT * FROM Stocks;'''
TRUNCATE_STOCKS_LINK = '''TRUNCATE TABLE stocks_link;'''
TRUNCATE_STOCKS = '''TRUNCATE TABLE stocks;'''
DROP_STOCKS_LINK_TABLE = '''DROP TABLE IF EXISTS stocks_link;'''
DROP_STOCKS_TABLE = '''DROP TABLE IF EXISTS stocks;'''
CREATE_STOCKS_LINK_SQL = '''CREATE TABLE stocks_link (
    symbol TEXT NOT NULL PRIMARY KEY,
    link TEXT,
    sector TEXT
    );
'''
CREATE_STOCKS_TABLE = '''CREATE TABLE stocks (
    date DATE NOT NULL,
    time TIME NOT NULL,
    stock_code TEXT NOT NULL,
    stock_name TEXT,
    open FLOAT(3),
    high FLOAT(3),
    low FLOAT(3),
    close FLOAT(3),
    vol INTEGER,
    buy_vol TEXT,
    sell_vol TEXT,
    PRIMARY KEY (date, time, stock_code)
    );    
'''


class DbOperations:
    def __init__(self, configfile='database.ini', section='postgresql'):
        # Create a parser
        parser = ConfigParser()
        # Read the config file
        parser.read(configfile)

        # Get section, default to postgresql
        db = {}
        if parser.has_section(section):
            logging.info('Reading database config file')
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            logging.error('Section {0} not found in {1} file'. format(section, configfile))

        logging.info('Connecting to database...')
        self.conn = psycopg2.connect(**db)

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

    def insert_stocks(self, date, time, code, name, open, high, low, close, vol, buy_vol, sell_vol):
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
        try:
            cur.execute(INSERT_STOCK, (date, time, code, name, open, high, low, close, clean_volume(vol), buy_vol, sell_vol))
            self.conn.commit()
        except psycopg2.IntegrityError as e:
            logging.error('Record {0}, {1}, {2}, {3} already exists.'.format(date, time, code, name))
            self.conn.rollback()

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
        logging.info('Committing changes and close database connection.')
        self.conn.commit()
        self.conn.close()


def clean_volume(numstr):
    if type(numstr) is int:
        return numstr
    else:
        return locale.atoi(numstr)


def main():
    db_op = DbOperations()
    # Create tables
    # db_op.create_table(DROP_STOCKS_LINK_TABLE, CREATE_STOCKS_LINK_SQL)
    # db_op.create_table(DROP_STOCKS_TABLE, CREATE_STOCKS_TABLE)

    # Record inserting test
    # db_op.insert_symlink('sapura2', 'star/business/sapura', 'sector')
    # db_op.insert_stocks('28 Feb 2019', '5:00 pm', '5211', 'sapura holdings', 10.0, 1.20, 1.01, 1.15, 12500,
    #                     '0.101 / 125', '0.111 / 153')

    # Truncate the table
    # db_op.clear_table(TRUNCATE_STOCKS_LINK)
    # db_op.clear_table(TRUNCATE_STOCKS)

    # Viewing the records in the table
    records = db_op.view_table(VIEW_STOCKS)
    # records = db_op.view_table(VIEW_STOCKS_LINK)
    print(len(records))
    for record in records:
        print(record)
    db_op.close_conn()


if __name__ == '__main__':
    main()
