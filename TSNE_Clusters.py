import quandl
import numpy as np
import csv
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn


def get_tickers(csvfile):
    """Return tickers from csv file"""
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        data = [x[0] for x in reader][1:]
    return data


def quandl_adj_close(tickers):
    """Retrieve Adj Close data from quandl"""
    quandl.ApiConfig.api_key = "ZF5iyY2nC7DHiWx49VhG"
    tickers = ["WIKI/" + x + ".11" for x in tickers]
    close_data = quandl.get(tickers, start_date="2015-01-01")
    close_data.fillna(method='ffill', inplace=True)
    return close_data


def corr_matrix(close_data):
    """Return correlation matrix on absolute stock levels"""
    return close_data.corr()


def tsne(corr, tickers):
    """Use t-sne algorithm to reduce dimensionality to 2 and plot"""
    model = TSNE(n_components=2)
    x = model.fit_transform(corr)
    plt.scatter(x[:, 0], x[:, 1], marker='o')
    for label, a, b in zip(tickers, x[:, 0], x[:, 1]):
        plt.annotate(
            label,
            xy=(a, b), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5))
    plt.title('T-SNE Clustering on the S&P 500 Correlation Matrix')
    plt.show()


if __name__ == "__main__":
    tickers = get_tickers('sp500.csv')
    close_data = quandl_adj_close(tickers)
    corr = corr_matrix(close_data)
    tsne(corr, tickers)
