from data_retriever import DataRetriever 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error

from scipy.optimize import minimize
import statsmodels.tsa.api as smt
import statsmodels.api as sm

from tqdm import tqdm_notebook

from itertools import product

import warnings

class TimeSeriesAnalyzer:


  def __init__(self, ticker) -> None:
    self.__ticker = ticker
    sns.set()
    warnings.filterwarnings('ignore')
    return


  def __mean_percentage_error(actual, predicted) -> float:
    return np.mean(np.abs((actual - predicted) / actual)) * 100


  def __read_data(self) -> pd.DataFrame:
    path = f'./data_retriever_storage/prices/{self.__ticker}_prices.csv'
    data = pd.read_csv(path, index_col=['Date'], parse_dates=['Date'])
    return data


  def plot_moving_average(series, window, plot_intervals=False, scale=1.96):

    rolling_mean = series.rolling(window=window).mean()
    
    plt.figure(figsize=(17,8))
    plt.title('Moving average\n window size = {}'.format(window))
    plt.plot(rolling_mean, 'g', label='Rolling mean trend')
    
    #Plot confidence intervals for smoothed values
    if plot_intervals:
        mae = mean_absolute_error(series[window:], rolling_mean[window:])
        deviation = np.std(series[window:] - rolling_mean[window:])
        lower_bound = rolling_mean - (mae + scale * deviation)
        upper_bound = rolling_mean + (mae + scale * deviation)
        plt.plot(upper_bound, 'r--', label='Upper bound / Lower bound')
        plt.plot(lower_bound, 'r--')
            
    plt.plot(series[window:], label='Actual values')
    plt.legend(loc='best')
    plt.grid(True)
    
# #Smooth by the previous 5 days (by week)
# plot_moving_average(data.Close, 5)

# #Smooth by the previous month (30 days)
# plot_moving_average(data.Close, 30)

# #Smooth by previous quarter (90 days)
# plot_moving_average(data.Close, 90, plot_intervals=True, scale=.5)


"""
Time Series Analysis:







"""




