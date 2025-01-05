
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from datetime import date, datetime, timedelta
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

# Set page config
# st.set_page_config(
#     page_title="Stock Price Prediction",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Title
st.title("Stock Price Prediction")

# Date inputs
today = date.today()
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start date", date(2022, 1, 1), max_value=today)
with col2:
    end = st.date_input("End date", date.today(), max_value=today)

# Validate input
if start > today or end > today:
    st.error("Error: Date cannot be in the future. Please enter a valid date.")
elif start >= end:
    st.error("Error: Start date must be before end date. Please enter valid dates.")
else:
    st.success(f'Start date: `{start}`\n\nEnd date: `{end}`')

    # Stock selection
    stock_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "NVDA", "V", "NFLX"]
    user_input = st.selectbox('Select stock to analyze', stock_list)

    # Download data
    @st.cache_data
    def load_data(ticker, start, end):
        return yf.download(ticker, start=start, end=end)

    df = load_data(user_input, start, end)

    if df.empty:
        st.error("No data available for the selected date range. Please choose a different range.")
    else:
        st.subheader(f'Data description from {start.strftime("%Y-%m-%d")} to {end.strftime("%Y-%m-%d")} of {user_input} Stock')
        st.write(df.describe())

        # Closing Price vs Time chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Close'))
        fig.update_layout(title='Closing Price vs Time', xaxis_title='Time', yaxis_title='Closing Price')
        st.plotly_chart(fig, use_container_width=True)

        # Candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'])])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Time', yaxis_title='Price')
        st.plotly_chart(fig, use_container_width=True)

        # Prepare data for model
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
        training_data_len = int(np.ceil(len(scaled_data) * .95))
        train_data = scaled_data[0:training_data_len, :]
        x_train, y_train = [], []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Create and train model
        model = tf.keras.Sequential([
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(x_train.shape[1], 1))),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(32),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')

        history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_split=0.1, verbose=0)

        # Prepare test data
        test_data = scaled_data[training_data_len - 60:, :]
        x_test = []
        y_test = df['Close'][training_data_len:].values

        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # Make predictions
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        # Calculate metrics
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_test - predictions.flatten()) / y_test)) * 100
        r2 = r2_score(y_test, predictions)

        st.subheader('Model Performance Metrics')
        st.write(f'Root Mean Square Error (RMSE): {rmse:.2f}')
        st.write(f'Mean Absolute Percentage Error (MAPE): {mape:.2f}%')
        st.write(f'R2 Score: {r2:.2f}')

        # Plot training history
        st.subheader('Training History')
        fig, ax = plt.subplots()
        ax.plot(history.history['loss'], label='Training Loss')
        ax.plot(history.history['val_loss'], label='Validation Loss')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.legend()
        st.pyplot(fig)

        # Plot actual vs predicted prices
        train = df[:training_data_len]
        valid = df[training_data_len:]
        valid['Predictions'] = predictions

        st.subheader('Actual vs Predicted Prices')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=train.index, y=train['Close'], mode='lines', name='Actual Train Price'))
        fig.add_trace(go.Scatter(x=valid.index, y=valid['Close'], mode='lines', name='Actual Test Price'))
        fig.add_trace(go.Scatter(x=valid.index, y=valid['Predictions'], mode='lines', name='Predicted Test Price'))
        st.plotly_chart(fig, use_container_width=True)

        # Future price prediction
        future_days = 7
        last_days = df['Close'].tail(60).values.reshape(-1, 1)
        last_days_scaled = scaler.transform(last_days)

        future_predictions = []
        for _ in range(future_days):
            x_future = last_days_scaled[-60:].reshape(1, 60, 1)
            future_prediction = model.predict(x_future)[0]
            future_predictions.append(future_prediction)
            last_days_scaled = np.append(last_days_scaled, future_prediction).reshape(-1, 1)

        future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

        future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=future_days)

        st.subheader('Future Price Predictions for the Next 7 Days')
        future_df = pd.DataFrame({'Date': future_dates, 'Predicted Close Price': future_predictions.flatten()})
        st.table(future_df)