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

    def view_symlink(self):
        """
        View the content of the stock symbol table
        :return: void
        """
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM Stocks_link''')
        result = cur.fetchall()
        print(result)

    def clear_symlink(self):
        """
        Clear all the content of the table
        :return: void
        """
        cur = self.conn.cursor()
        # TRUNCATE TABLE Stocks_link
        cur.execute('''DELETE FROM Stocks_link''')

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
    db_op.view_symlink()
    # db_op.clear_symlink()
    # db_op.view_symlink()
    db_op.close_conn()


if __name__ == '__main__':
    main()