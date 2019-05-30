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

df['change_flag'] = ['pos' if x > 0 else 'non' if x == 0 else 'neg' for x in df['change_percentage']]

sime_df = df[df.stock_code == '5285']
sime_df['trade_flag'] = ['buy' if x <= 5.03 else 'sell' if x >= 5.10 else 'hold' for x in sime_df['open']]

kawan_df = df[df.stock_code == '7216']
kawan_df['trade_flag'] = ['buy' if x <= 1.00 else 'sell' if x >= 1.50 else 'hold' for x in kawan_df['open']]

caely_df = df[df.stock_code == '7154']
caely_df['trade_flag'] = ['buy' if x <= 0.90 else 'sell' if x >= 1.00 else 'hold' for x in caely_df['open']]

emico_df = df[df.stock_code == '9091']
emico_df['trade_flag'] = ['buy' if x <= 0.15 else 'sell' if x >= 0.17 else 'hold' for x in emico_df['open']]

stone_df = df[df.stock_code == '5165']
stone_df['trade_flag'] = ['buy' if x <= 0.50 else 'sell' if x >= 0.60 else 'hold' for x in stone_df['open']]

daibochi_df = df[df.stock_code == '8125']
daibochi_df['trade_flag'] = ['buy' if x <= 1.20 else 'sell' if x >= 1.50 else 'hold' for x in daibochi_df['open']]

facb_df = df[df.stock_code == '2984']
facb_df['trade_flag'] = ['buy' if x <= 0.80 else 'sell' if x >= 1.20 else 'hold' for x in facb_df['open']]

stock7_df = pd.concat([sime_df, kawan_df, caely_df, emico_df, stone_df, daibochi_df, facb_df], ignore_index=True)
print(stock7_df)

stock7_df.to_csv('C:\\Users\\dante\\Documents\\My SAS Files\\extData\\stock7_df.csv', encoding='utf-8', index=False)
