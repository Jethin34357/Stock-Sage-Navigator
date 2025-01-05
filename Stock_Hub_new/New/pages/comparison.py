import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import plotly.graph_objs as go

def add_arrow_marks(fig, data, percent_change, threshold):
    # Add up arrows for rapid stock increases
    up_indices = percent_change[percent_change > threshold].index
    up_prices = data[percent_change > threshold]
    fig.add_trace(go.Scatter(x=up_indices, y=up_prices, mode='markers', name='Up', marker=dict(symbol='triangle-up', color='green', size=10)))

    # Add down arrows for rapid stock decreases
    down_indices = percent_change[percent_change < -threshold].index
    down_prices = data[percent_change < -threshold]
    fig.add_trace(go.Scatter(x=down_indices, y=down_prices, mode='markers', name='Down', marker=dict(symbol='triangle-down', color='red', size=10)))

# Define function to compare multiple stocks
def compare_stocks(tickers, start_date, end_date, threshold):
    data = pd.DataFrame()
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)['Close']
        data[ticker] = stock_data

    # Calculate percentage change in closing prices for the entire data
    percent_change = data.pct_change() * 100

    fig = go.Figure()

    # Add line traces for each stock
    for ticker in tickers:
        fig.add_trace(go.Scatter(x=data.index, y=data[ticker], mode='lines', name=ticker))

        # Add arrow marks for rapid stock changes for each stock
        add_arrow_marks(fig, data[ticker], percent_change[ticker], threshold)

    # Customize plot layout
    fig.update_layout(title='Stock Comparison', xaxis_title='Date', yaxis_title='Price')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(legend=dict(orientation='h', yanchor='top', y=-0.2))

    # Display plot
    st.plotly_chart(fig)
st.subheader("Stock Price Comparison")
stock_ticker_file = 'Tickers\Stock_Tickers'
stock_list = pd.read_csv(stock_ticker_file).squeeze().tolist()

user_input = st.multiselect('Select stocks to analyze', stock_list,  default=['GOOGL', 'AMZN'])
# Add date input widgets for start and end dates
today = date.today()
col1,col2 = st.columns(2)
with col1:
    start = st.date_input("Start date", date(2012, 1, 1), max_value=today)
with col2:
    end = st.date_input("End date", date(2022, 12, 31), max_value=today)

threshold = st.slider('Threshold for Rapid Stock Changes (%)', min_value=1, max_value=20, value=10)
submit_button = st.button(label='Compare')

# If the user has selected stocks and submitted the form, compare them
if submit_button and len(user_input) > 1:
    compare_stocks(user_input, start, end, threshold)
elif submit_button:
    st.write('Please select at least two stocks to compare.')


