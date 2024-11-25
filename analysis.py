import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

# Load stock data
data = pd.read_csv("E:\\PYTHON PROJECTS\\STKpredictor\\GOOGL.csv", parse_dates=['Date'], index_col='Date')
ts = data['Adj Close']

# Plot the time series
plt.plot(ts)
plt.title("Time Series: Adjusted Close Prices")
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price")
plt.show()

# Log transformation and plot
ts_log = np.log(ts)
plt.plot(ts_log)
plt.title("Log Transformed Time Series")
plt.xlabel("Date")
plt.ylabel("Log Adjusted Close Price")
plt.show()

# Moving average and plot
moving_avg = ts_log.rolling(10, min_periods=1).mean()
plt.plot(ts_log, label="Log Transformed")
plt.plot(moving_avg, color='red', label="Moving Average (10)")
plt.title("Moving Average Smoothing")
plt.legend()
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()

# Differencing and plot
ts_log_diff = ts_log - ts_log.shift()
ts_log_diff.dropna(inplace=True)
plt.plot(ts_log_diff)
plt.title("Differenced Log Transformed Time Series")
plt.xlabel("Date")
plt.ylabel("Differenced Value")
plt.show()

# Decomposition of the time series
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts_log, period=52)

plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(decomposition.trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(decomposition.seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(decomposition.resid, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# ACF and PACF plots
from statsmodels.tsa.stattools import acf, pacf
lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')

# Plot ACF
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

# Plot PACF
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()
