# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the plot size
plt.rcParams['figure.figsize'] = 15, 6

# Function to perform EDA and return plot paths
def perform_eda(file_path):
    # Load the data
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

    # Ensure the output directory exists
    output_dir = "static/plots"
    os.makedirs(output_dir, exist_ok=True)

    # Display the first few rows of the dataset
    print("First 5 rows of the dataset:")
    print(data.head())

    # Display the summary statistics
    print("\nSummary statistics:")
    print(data.describe())

    # Check for missing values
    print("\nMissing values in the dataset:")
    print(data.isnull().sum())

    # Check the data types of each column
    print("\nData types of columns:")
    print(data.dtypes)

    # Convert 'Date' column to datetime format
    if 'Date' in data.columns:
        try:
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Convert invalid dates to NaT
            print("\nConverted 'Date' column to datetime format.")
        except Exception as e:
            print(f"\nError converting 'Date' column: {e}")
            return []

        # Drop rows with NaT in the 'Date' column
        data = data.dropna(subset=['Date'])
        print("\nDropped rows with invalid 'Date' values.")

    # Check if the dataset is empty after filtering invalid dates
    if data.empty:
        print("\nError: Dataset is empty after filtering invalid dates.")
        return []

    # Set 'Date' as the index if it's a time-series dataset
    if 'Date' in data.columns:
        data.set_index('Date', inplace=True)
        print("\n'Set 'Date' column as the index.")

    plot_paths = []

    # Plot the 'Adj Close' price over time if available
    if 'Adj Close' in data.columns:
        print("\nPlotting 'Adj Close' prices over time...")
        plt.plot(data['Adj Close'], label="Adjusted Close Price")
        plt.title("Adjusted Close Price Over Time")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plot_path = os.path.join(output_dir, 'adjusted_close_over_time.png')
        plt.savefig(plot_path)  # Save plot
        plt.close()  # Close the plot to avoid display in terminal
        print(f"Plot saved as {plot_path}")
        plot_paths.append('plots/adjusted_close_over_time.png')

    # Plot the distribution of 'Adj Close' prices if available
    if 'Adj Close' in data.columns:
        print("\nPlotting the distribution of 'Adj Close' prices...")
        data['Adj Close'].plot(kind='hist', bins=50, color='skyblue', edgecolor='black')
        plt.title("Distribution of Adjusted Close Prices")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        hist_plot_path = os.path.join(output_dir, 'adjusted_close_distribution.png')
        plt.savefig(hist_plot_path)  # Save plot
        plt.close()
        print(f"Plot saved as {hist_plot_path}")
        plot_paths.append('plots/adjusted_close_distribution.png')

    # Check for correlation between numerical columns
    print("\nCorrelation matrix:")
    correlation_matrix = data.corr()
    print(correlation_matrix)

    # Visualize the correlation matrix
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix Heatmap")
    corr_plot_path = os.path.join(output_dir, 'correlation_matrix.png')
    plt.savefig(corr_plot_path)  # Save plot
    plt.close()
    print(f"Plot saved as {corr_plot_path}")
    plot_paths.append('plots/correlation_matrix.png')

    # Pair plot of the dataset (if dataset isn't too large)
    try:
        print("\nGenerating pair plot for numerical columns...")
        sns.pairplot(data.select_dtypes(include=[np.number]))
        pair_plot_path = os.path.join(output_dir, 'pairplot.png')
        plt.savefig(pair_plot_path)  # Save plot
        plt.close()
        print(f"Plot saved as {pair_plot_path}")
        plot_paths.append('plots/pairplot.png')
    except Exception as e:
        print(f"Error generating pair plot: {e}")

    # Return the list of generated plot paths for web display
    return plot_paths

# If the script is run directly, this part will execute:
if __name__ == "__main__":
    file_path = 'E:\\PYTHON PROJECTS\\STKpredictor\\GOOGL.csv'
    plots = perform_eda(file_path)
    if plots:
        print("\nGenerated plots:")
        for plot in plots:
            print(plot)
    else:
        print("\nNo plots were generated.")
