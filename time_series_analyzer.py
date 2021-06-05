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


  def mean_percentage_error(actual, predicted) -> float:
    return np.mean(np.abs((actual - predicted) / actual)) * 100


  def read_data(self) -> pd.DataFrame:
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
    

  def __double_exponential_smoothing(series, alpha, beta):

    result = [series[0]]
    for n in range(1, len(series)+1):
      if n == 1:
        level, trend = series[0], series[1] - series[0]
      if n >= len(series): # forecasting
        value = result[-1]
      else:
        value = series[n]
      last_level, level = level, alpha * value + (1 - alpha) * (level + trend)
      trend = beta * (level - last_level) + (1 - beta) * trend
      result.append(level + trend)
    return result

  def plot_double_exponential_smoothing(self, series, alphas, betas):
     
    plt.figure(figsize=(17, 8))
    for alpha in alphas:
      for beta in betas:
        plt.plot(self.__double_exponential_smoothing(series, alpha, beta), label="Alpha {}, beta {}".format(alpha, beta))
    plt.plot(series.values, label = "Actual")
    plt.legend(loc="best")
    plt.axis('tight')
    plt.title("Double Exponential Smoothing")
    plt.grid(True)

  def tsplot(y, lags=None, figsize=(12, 7), syle='bmh'):
    
    if not isinstance(y, pd.Series):
      y = pd.Series(y)
        
    with plt.style.context(style='bmh'):
      fig = plt.figure(figsize=figsize)
      layout = (2,2)
      ts_ax = plt.subplot2grid(layout, (0,0), colspan=2)
      acf_ax = plt.subplot2grid(layout, (1,0))
      pacf_ax = plt.subplot2grid(layout, (1,1))
      
      y.plot(ax=ts_ax)
      p_value = sm.tsa.stattools.adfuller(y)[1]
      ts_ax.set_title('Time Series Analysis Plots\n Dickey-Fuller: p={0:.5f}'.format(p_value))
      smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
      smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
      plt.tight_layout()
    
  


  # Train many SARIMA models to find the best set of parameters
  def optimize_SARIMA(self, parameters_list, d, D, s, data):
    """
    Return dataframe with parameters and corresponding AIC
    
    parameters_list - list with (p, q, P, Q) tuples
    d - integration order
    D - seasonal integration order
    s - length of season
    """
    
    results = []
    best_aic = float('inf')
    
    for param in tqdm_notebook(parameters_list):
      try: model = sm.tsa.statespace.SARIMAX(data.Close, order=(param[0], d, param[1]),
                                            seasonal_order=(param[2], D, param[3], s)).fit(disp=-1)
      except:
        continue
            
      aic = model.aic
        
      #Save best model, AIC and parameters
      if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
      results.append([param, model.aic])
        
    result_table = pd.DataFrame(results)
    result_table.columns = ['parameters', 'aic']
    #Sort in ascending order, lower AIC is better
    result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)
    
    return result_table

TSA = TimeSeriesAnalyzer('TSLA')

data = TSA.read_data()


ps = range(0, 3)
d = 1
qs = range(0, 3)
Ps = range(0, 3)
D = 1
Qs = range(0, 3)
s = 3

#Create a list with all possible combinations of parameters
parameters = product(ps, qs, Ps, Qs)
parameters_list = list(parameters)
len(parameters_list)

result_table = TSA.optimize_SARIMA(parameters_list, d, D, s, data)

#Set parameters that give the lowest AIC (Akaike Information Criteria)
p, q, P, Q = result_table.parameters[0]

best_model = sm.tsa.statespace.SARIMAX(data.Close, order=(p, d, q),
                                       seasonal_order=(P, D, Q, s)).fit(disp=-1)

print(best_model.summary())





# #Smooth by the previous 5 days (by week)
# plot_moving_average(data.Close, 5)

# #Smooth by the previous month (30 days)
# plot_moving_average(data.Close, 30)

# #Smooth by previous quarter (90 days)
# plot_moving_average(data.Close, 90, plot_intervals=True, scale=.5)

# plot_double_exponential_smoothing(data.Close, alphas=[0.9, 0.02], betas=[0.9, 0.02])

# tsplot(data.Close, lags=30)

# # Take the first difference to remove to make the process stationary
# data_diff = data.Close - data.Close.shift(1)

# tsplot(data_diff[1:], lags=30)


"""
Time Series Analysis:







"""




