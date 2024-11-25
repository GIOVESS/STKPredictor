# app.py

import os
import webbrowser
import threading
from flask import Flask, render_template, flash, redirect, session, url_for,request
import numpy as np
from eda import perform_eda
from time_series import perform_arima
from stock_data import load_stock_data, fetch_stock_data
from database import init_db  # Import init_db from database.py
from user import register_user, login_user, logout_user, is_logged_in  # Import user-related functions

# Flask app setup
app = Flask(__name__)
app.secret_key = "51e2313d32f598c11ce0b7f50fd5fd54"  # Use a secure key for production

# Flag to ensure stock data is only initialized once
data_initialized = False

# Initialize database and stock data before handling requests
def initialize_data():
    global data_initialized
    if not data_initialized:
        try:
            # Initialize the database tables (create tables if they don't exist)
            init_db()  # Create database tables
            print("Database tables created successfully.")
            
            # Load stock data into the database (load data from CSV)
            load_stock_data("E:\\PYTHON PROJECTS\\STKpredictor\\GOOGL.csv", "GOOGL")
            print("Stock data loaded successfully.")
            
            # Mark data as initialized
            data_initialized = True
        except Exception as e:
            print(f"Error during data initialization: {e}")
            flash(f"Error during data initialization: {e}", "danger")

# Initialize data directly before starting Flask app
initialize_data()

# Function to open the browser automatically
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

# Home route
@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("home.html")

# User Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        else:
            flash("Registration failed. Please try again.", "danger")
    return render_template('register.html')

# User Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['user_id'] = username  # Save the username or user_id in the session
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

# User Logout route
@app.route('/logout')
def logout():
    logout_user()  # Remove the user from the session
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

# Analyze data route (when the "Analyze" button is clicked)
@app.route('/analyze', methods=['POST'])
def analyze_data():
    try:
        # Execute the analysis.py script
        os.system("python analysis.py")  # Executes the analysis script
        
        # Flash a success message
        flash("The analysis of the data has been executed successfully.", "success!")
        
        # Redirect to home route after execution
        return redirect(url_for('home'))

    except Exception as e:
        flash(f"An error occurred while running the analysis script: {e}", "danger")
        return redirect(url_for('home'))

# Route for performing EDA (Exploratory Data Analysis)
@app.route('/eda', methods=['GET'])
def eda():
    try:
        # Define the file path for the dataset
        file_path = "E:\\PYTHON PROJECTS\\STKpredictor\\GOOGL.csv"
        
        # Perform EDA and retrieve the plot paths
        plot_paths = perform_eda(file_path)

        # Pass the plot paths to the template for rendering
        return render_template(
            'eda_report.html',
            plot_paths=plot_paths  # Pass the plot paths to the template
        )
    except Exception as e:
        flash(f"An error occurred during EDA: {e}", "danger")
        return redirect(url_for('home'))

# Forecasting route for performing ARIMA forecasting
@app.route('/forecast/<symbol>', methods=['GET', 'POST'])
def forecast(symbol):
    try:
        # Fetch stock data for the specified symbol
        stock_data = fetch_stock_data(symbol)

        if stock_data is None:
            flash("No stock data found for forecasting.", "danger")
            return redirect(url_for('home'))

        # Apply log transformation for stationarity
        ts = stock_data['Adj Close'].apply(np.log)

        # Get user-specified forecast length (default is 30 days)
        forecast_length = int(request.args.get('length', 30))

        # Perform ARIMA forecasting
        in_sample_preds, forecast_vals, arima_plot = perform_arima(
            ts, order=(2, 1, 2), symbol=symbol, forecast_length=forecast_length
        )

        # Pass the correct relative path for rendering
        return render_template(
            'forecast.html',
            symbol=symbol,
            forecast_length=forecast_length,
            in_sample_preds=in_sample_preds.to_dict(),
            forecast_vals=forecast_vals.to_dict(),
            arima_plot=f"plots/{os.path.basename(arima_plot)}"
        )

    except Exception as e:
        flash(f"An error occurred during forecasting: {e}", "danger")
        return redirect(url_for('home'))

# Run the Flask app and open the browser in a separate thread
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # Open the browser after a short delay (1 second)
    app.run(debug=True)
