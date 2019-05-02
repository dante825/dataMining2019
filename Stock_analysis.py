import pandas as pd
import numpy as np

from DbOperations import *

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)

# Retrieve the stock prices data from database
db_op = DbOperations()
stock_table = db_op.view_table('SELECT date, stock_code, open, close, high, low, vol FROM stock_prices;')

# Convert the data into a pandas data frame
df = pd.DataFrame(stock_table, columns=['date', 'stock_code', 'open', 'close', 'high', 'low', 'vol'])
df = df.fillna(0)
df = df.replace(np.inf, 0)

# Calculate the percentage change for each stock, a new column in df
df['change_percentage'] = (df['close'] - df['open']) / df['open'] * 100
simeDarby = df.loc[df['stock_code'] == '5285']
kawan = df.loc[df['stock_code'] == '7216']
hockHeng = df.loc[df['stock_code'] == '5165']


def change_period(sdf):
    end = sdf.iloc[sdf.shape[0]-1]['close']
    start = sdf.iloc[0]['close']
    return (end - start) / start * 100


# Highest positive correlation with Sime Darby: Kawan Food Bhd (7216)
# Highest negative correlation with Sime Darby: Hock Heng Stone Industries Berhad (5165)
print('\nSime Darby')
print(simeDarby)
print(simeDarby.describe())
print('The percentage of change during this period: %2f%%' % (change_period(simeDarby)))
print('\n\nKawan')
print(kawan)
print(kawan.describe())
print('The percentage of change during this period: %2f%%' % (change_period(kawan)))
print('\n\nHock Heng')
print(hockHeng)
print(hockHeng.describe())
print('The percentage of change during this period: %2f%%' % (change_period(hockHeng)))
