from datetime import date
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
    self.ticker = ticker
    sns.set()
    warnings.filterwarnings('ignore')
    return


  def mean_absolute_percentage_error(self, actual, predicted) -> float:
    return np.mean(np.abs((actual - predicted) / actual)) * 100


  def read_data(self) -> pd.DataFrame:
    path = f'./data_retriever_storage/prices/{self.ticker}_prices.csv'
    data = pd.read_csv(path, index_col=['Date'], parse_dates=['Date'])
    return data


  def plot_moving_average(self, series, window, plot_intervals=False, scale=1.96):

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
    plt.show()
    
  
  def exponential_smoothing(self, series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result


  def plot_exponential_smoothing(self, series, alphas):
 
    plt.figure(figsize=(17, 8))
    for alpha in alphas:
        plt.plot(self.exponential_smoothing(series, alpha), label="Alpha {}".format(alpha))
    plt.plot(series.values, "c", label = "Actual")
    plt.legend(loc="best")
    plt.axis('tight')
    plt.title("Exponential Smoothing")
    plt.grid(True)


  def double_exponential_smoothing(self, series, alpha, beta):

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
        plt.plot(self.double_exponential_smoothing(series, alpha, beta), label="Alpha {}, beta {}".format(alpha, beta))
    plt.plot(series.values, label = "Actual")
    plt.legend(loc="best")
    plt.axis('tight')
    plt.title("Double Exponential Smoothing")
    plt.grid(True)


  def tsplot(self, y, lags=None, figsize=(12, 7), syle='bmh'):
    
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
    
    return p_value
    
  


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
  
  def plot_SARIMA(self, series, model, n_steps):
    """
        Plot model vs predicted values
        
        series - dataset with time series
        model - fitted SARIMA model
        n_steps - number of steps to predict in the future
    """
    s = 1
    d = 3
    data = series.copy().rename(columns = {'Close': 'actual'})
    drop_cols = ["Open", "High", "Low", "Adj Close", "Volume"]
    data.drop(drop_cols, axis=1, inplace=True)
    data['arima_model'] = model.fittedvalues
    #Make a shift on s+d steps, because these values were unobserved by the model due to the differentiating
    data['arima_model'][:s+d] = np.NaN
    
    #Forecast on n_steps forward
    forecast = model.predict(start=data.shape[0], end=data.shape[0] + n_steps)
    forecast = data.arima_model.append(forecast)
    #Calculate error
    error = self.mean_absolute_percentage_error(data['actual'][s+d:], data['arima_model'][s+d:])
    
    plt.figure(figsize=(17, 8))
    plt.title('Mean Absolute Percentage Error: {0:.2f}%'.format(error))
    plt.plot(forecast, color='r', label='model')
    plt.axvspan(data.index[-1], forecast.index[-1],alpha=0.5, color='lightgrey')
    plt.plot(data, label='actual')
    plt.legend()
    plt.grid(True)
    plt.show()
    

  def analyze(self):
    data = self.read_data()
    series = self.exponential_smoothing(data.Close, 0.05)
    self.plot_exponential_smoothing(data.Close, [0.05, 0.15])
    series = self.double_exponential_smoothing(data.Close, 0.02, 0.02)
    self.plot_double_exponential_smoothing(data.Close, [.02, .9], [.02, .9])
    lags = len(data.index) * 0.25
    p_value = self.tsplot(data.Close, lags=int(lags))
    if p_value:
      data_diff = data.Close - data.Close.shift(1) # get rid of autocorrelation
      self.tsplot(data_diff[1:], lags=int(lags))
      # makes dickey-fuller p_value = 0, indicating no autocorrelation
    
    ps = range(0, 3)
    d = 1
    qs = range(0, 3)
    Ps = range(0, 3)
    D = 1
    Qs = range(0, 3)
    s = 3
    parameters = product(ps, qs, Ps, Qs)
    parameters_list = list(parameters)
    result_table = self.optimize_SARIMA(parameters_list, d, D, s, data)
    p, q, P, Q = result_table.parameters[0]
    best_model = sm.tsa.statespace.SARIMAX(data.Close, order=(p, d, q),
                                       seasonal_order=(P, D, Q, s)).fit(disp=-1)
    self.plot_SARIMA(data, best_model, 10)
    print(best_model.predict(start=data.Close.shape[0], end=data.Close.shape[0] + 10))
    print(self.mean_absolute_percentage_error(data.Close[s+d:], best_model.fittedvalues[s+d:]))
    with open(f"./data_retriever_storage/timeseries/{TSA.ticker}.txt", 'w') as tracker:
      tracker.write(str(data))
      tracker.write('\n\nFrom the above data, our modelling predicted:\n')
      tracker.write(str(best_model.predict(start=data.Close.shape[0], end=data.Close.shape[0] + 10)) + '\n')
      tracker.write(str(TSA.mean_absolute_percentage_error(data.Close[s+d:], best_model.fittedvalues[s+d:])))
    

TSA = TimeSeriesAnalyzer('DOCU')
TSA.analyze()
