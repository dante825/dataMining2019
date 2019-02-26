import sqlite3

INSERT_LINK_SQL = '''INSERT INTO Stocks_link (symbol, link, sector) VALUES (?,?,?);'''
DB_LOCATION = 'E:\\development\\repo\\icedTeaSpider\\stockDb.sqlite'
DROP_TABLE = '''DROP TABLE IF EXISTS Stocks_link;'''
CREATE_STOCKS_LINK_SQL = '''CREATE TABLE Stocks_link (
    symbol TEXT NOT NULL PRIMARY KEY,
    link TEXT,
    sector TEXT
    );
'''

class DbOperations:
    def __init__(self):
        self.conn = sqlite3.connect(DB_LOCATION)

    def create_table(self, drop_script, create_script):
        """
        Create a table based on the SQL script provided
        :param sqlScript: SQL script to create table
        :return: void
        """
        # conn = sqlite3.connect(DB_LOCATION)
        cur = self.conn.cursor()
        cur.execute(drop_script)
        cur.execute(create_script)
        # conn.commit()
        # conn.close()

    def insert_symlink(self, symbol, link, sector):
        """
        Insert a row of stock symbol, url link, sector and subsector into the db
        :param conn: db connection
        :param stockList: the cleaned list of stocks
        :return: void
        """
        # conn = sqlite3.connect(DB_LOCATION)
        cur = self.conn.cursor()
        cur.execute(INSERT_LINK_SQL, (symbol, link, sector))
        # conn.commit()
        # conn.close()

    def view_symlink(self):
        """
        View the content of the stock symbol table
        :return: void
        """
        # conn = sqlite3.connect(DB_LOCATION)
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM Stocks_link''')
        result = cur.fetchall()
        print(result)
        # conn.commit()
        # conn.close()

    def clear_symlink(self):
        """
        Clear all the content of the table
        :return: void
        """
        # conn = sqlite3.connect(DB_LOCATION)
        cur = self.conn.cursor()
        # TRUNCATE TABLE Stocks_link
        cur.execute('''DELETE FROM Stocks_link''')
        # conn.commit()
        # conn.close()

    def close_conn(self):
        self.conn.commit()
        self.conn.close()


def main():
    db_op = DbOperations()
    # db_op.insert_symlink('sapura', 'star/business/sapura', 'sector')
    # db_op.create_table(DROP_TABLE, CREATE_STOCKS_LINK_SQL)
    db_op.view_symlink()
    # db_op.clear_symlink()
    # db_op.view_symlink()
    db_op.close_conn()


if __name__ == '__main__':
    main()