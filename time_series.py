# Dependencies for time-series analysis and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import os
import matplotlib

# Use non-interactive backend before importing pyplot (for use in server environments)
matplotlib.use('Agg')

# Directory to save plots
PLOTS_DIR = "static/plots/"
os.makedirs(PLOTS_DIR, exist_ok=True)  # Ensure the directory exists

def test_stationarity(timeseries, filename):
    """
    Perform the stationarity test by plotting the original time series, 
    rolling mean, and rolling standard deviation.
    """
    # Calculate rolling statistics
    rolmean = timeseries.rolling(window=12).mean()
    rolstd = timeseries.rolling(window=12).std()

    # Plot rolling statistics
    plt.figure(figsize=(10, 6))
    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')

    # Save the plot to the static/plots directory
    plot_path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(plot_path)
    plt.close()
    print(f"Stationarity plot saved to {plot_path}")

def perform_arima(ts, order, symbol, forecast_length):
    """
    Perform ARIMA forecasting on the provided time series data (ts).
    """
    # Fit ARIMA model
    model = ARIMA(ts, order=order)
    results_ARIMA = model.fit()

    # Generate in-sample predictions (for training data)
    predictions_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    predictions_diff_cumsum = predictions_diff.cumsum()
    predictions_log = pd.Series(ts.iloc[0], index=ts.index).add(predictions_diff_cumsum, fill_value=0)

    # Apply np.exp safely to avoid overflow
    in_sample_predictions = np.exp(np.clip(predictions_log, None, 700))  # Cap at log(1e+300)

    # Generate out-of-sample forecast
    forecast = results_ARIMA.get_forecast(steps=forecast_length)
    forecast_index = pd.date_range(start=ts.index[-1], periods=forecast_length + 1, freq='D')[1:]
    forecast_values = np.exp(forecast.predicted_mean)  # Convert from log scale
    forecast_series = pd.Series(forecast_values, index=forecast_index)

    # Plot ARIMA results
    plt.figure(figsize=(10, 6))
    plt.plot(ts, label='Original')
    plt.plot(in_sample_predictions, color='red', label='In-Sample Predictions')
    plt.plot(forecast_series, color='green', label='Forecast')
    plt.title(f'ARIMA Forecast for {symbol}')
    plt.legend()

    # Save the ARIMA plot to the static/plots directory
    plot_filename = f"arima_forecast_{symbol}.png"
    plot_path = os.path.join(PLOTS_DIR, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    print(f"ARIMA forecast plot saved to {plot_path}")

    # Return the in-sample predictions, out-of-sample forecast, and plot path
    return in_sample_predictions, forecast_series, plot_path
