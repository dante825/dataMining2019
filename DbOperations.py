import sqlite3

INSERT_LINK_SCRIPT = '''INSERT INTO Stocks_link (symbol, link, sector, subsector) VALUES (?,?,?,?);'''
DB_LOCATION = 'E:\\development\\repo\\icedTeaSpider\\stockDb.sqlite'

# cur.executescript('''
#     DROP TABLE IF EXISTS Stocks_link;
#
#     CREATE TABLE Stocks_link (
#     symbol TEXT NOT NULL PRIMARY KEY,
#     link TEXT,
#     sector TEXT,
#     subsector TEXT
#     );
# ''')

def insertSymLink(stockList):
    """
    Insert a row of stock symbol, url link, sector and subsector into the db
    :param stockList: the list that contains the information
    :return: void
    """
    conn = sqlite3.connect(DB_LOCATION)
    cur = conn.cursor()
    cur.execute(INSERT_LINK_SCRIPT, (stockList[0], stockList[1], stockList[2], stockList[3]))
    conn.commit()
    conn.close()

def viewSymLink():
    """
    View the content of the stock symbol table
    :return: void
    """
    conn = sqlite3.connect(DB_LOCATION)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Stocks_link''')
    result = cur.fetchall()
    print(result)
    conn.commit()
    conn.close()

def clearSymLink():
    """
    Clear all the content of the table
    :return: void
    """
    conn = sqlite3.connect(DB_LOCATION)
    cur = conn.cursor()
    # TRUNCATE TABLE Stocks_link
    cur.execute('''DELETE FROM Stocks_link''')
    conn.commit()
    conn.close()

# testList = ['sapura', 'star/business/sapura', 'main', 'subsector']
# insertSymLink(testList)
# clearSymLink()
# viewSymLink()
