import sqlite3

INSERT_LINK_SCRIPT = '''INSERT INTO Stocks_link (symbol, link, sector, subsector) VALUES (?,?,?,?);'''

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

def insertLink(mapPair):
    conn = sqlite3.connect('E:\\development\\repo\\icedTeaSpider\\stockDb.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Stocks_link''')
    result = cur.fetchall()
    print(result)
    conn.commit()
    conn.close()


# cur.execute(INSERT_LINK_SCRIPT, ('testSym3', 'link/link3', 'main', 'finance'))
# cur.execute('''INSERT INTO Stocks_link (symbol, link, sector, subsector) VALUES (?,?,?,?);''', ('testSym2', 'link/link2', 'main', 'health'))
insertLink({'adf':'asdf'})