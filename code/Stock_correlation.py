import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation, OneD_SymbolicAggregateApproximation

from DbOperations import *

# Retrieve the stock prices data from database
db_op = DbOperations()
stock_table = db_op.view_table('SELECT date, stock_code, open, close FROM stock_prices;')

# Convert the data into a pandas data frame
df = pd.DataFrame(stock_table, columns=['date', 'stock_code', 'open', 'close'])

# Calculate the percentage change for each stock, a new column in df
df['change_percentage'] = (df['close'] - df['open']) / df['open'] * 100
# print(df.head(10))

# Subset the table to the columns needed
stock_df = df[['date', 'stock_code', 'change_percentage']]
# print(stock_df.head(10))

# Pivot the table
pivoted_df = pd.pivot_table(df, index='date', columns='stock_code', values='change_percentage')
# print(pivoted_df.head(10))

# Checking the number of missing values in the data
print(pivoted_df.isnull().sum().sum())

# Replace the missing values and infinity values with 0
pivoted_df = pivoted_df.fillna(0)
pivoted_df = pivoted_df.replace(np.inf, 0)
# print(pivoted_df.head(10))

# Calculate the covariance of all the stocks
covariance_df = pivoted_df.cov()
print('Covariance dataframe')
print(covariance_df)

# Calculate the correlation between all the stocks
correlation_df = pivoted_df.corr()
print('Correlation dataframe')
print(correlation_df)

# Select one of the stock 5285 Sime Darby Plantation Berhad
stock_cor_pos = correlation_df['5285'].sort_values(ascending=False)
stock_cor_neg = correlation_df['5285'].sort_values(ascending=True)
print('Positive correlation for Sime Darby Plantation Berhad (5285):')
print(stock_cor_pos.head(10))
print('Negative correlation for Sime Darby Plantation Berhad (5285):')
print(stock_cor_neg.head(10))

# Visualize the correlation
# plt.matshow(ijm)
# plt.show()
# scatter_matrix(pivoted_df, figsize=(16,12), alpha=0.3)


def saa_pax(dataset, title):
    """
    Show the graph of PAA and SAX of time series data
    :param dataset: time series of a stock
    :return:
    """
    n_ts, sz, d = 1, 100, 1
    scaler = TimeSeriesScalerMeanVariance(mu=0., std=1.)  # Rescale time series
    dataset = scaler.fit_transform(dataset)

    # PAA transform (and inverse transform) of the data
    n_paa_segments = 10
    paa = PiecewiseAggregateApproximation(n_segments=n_paa_segments)
    paa_dataset_inv = paa.inverse_transform(paa.fit_transform(dataset))

    # SAX transform
    n_sax_symbols = 8
    sax = SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols)
    sax_dataset_inv = sax.inverse_transform(sax.fit_transform(dataset))

    # 1d-SAX transform
    n_sax_symbols_avg = 8
    n_sax_symbols_slope = 8
    one_d_sax = OneD_SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols_avg,
                                                    alphabet_size_slope=n_sax_symbols_slope)
    one_d_sax_dataset_inv = one_d_sax.inverse_transform(one_d_sax.fit_transform(dataset))

    plt.figure()
    plt.subplot(2, 2, 1)  # First, raw time series
    plt.plot(dataset[0].ravel(), "b-")
    plt.title("Raw time series " + title)

    plt.subplot(2, 2, 2)  # Second, PAA
    plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
    plt.plot(paa_dataset_inv[0].ravel(), "b-")
    plt.title("PAA " + title)

    plt.subplot(2, 2, 3)  # Then SAX
    plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
    plt.plot(sax_dataset_inv[0].ravel(), "b-")
    plt.title("SAX, %d symbols" % n_sax_symbols)

    plt.subplot(2, 2, 4)  # Finally, 1d-SAX
    plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
    plt.plot(one_d_sax_dataset_inv[0].ravel(), "b-")
    plt.title("1d-SAX, %d symbols (%dx%d)" % (n_sax_symbols_avg * n_sax_symbols_slope,
                                              n_sax_symbols_avg,
                                              n_sax_symbols_slope))

    plt.tight_layout()
    plt.show()
    # return sax


saa_pax(pivoted_df['5285'], 'Sime Darby')
saa_pax(pivoted_df['7216'], 'Kawan Bhd')
saa_pax(pivoted_df['7154'], 'Caely Holdings')
saa_pax(pivoted_df['9091'], 'Emico Holdings')
saa_pax(pivoted_df['5165'], 'Hock Heng')
saa_pax(pivoted_df['8125'], 'Daibochi')
saa_pax(pivoted_df['2984'], 'FACB')
saa_pax(pivoted_df['7086'], 'Ablegroup')
