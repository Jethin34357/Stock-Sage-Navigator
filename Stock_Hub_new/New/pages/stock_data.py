import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.subheader("Download Historical Stock Data")

# Load stock tickers from CSV file
stock_ticker_file = 'Tickers\Stock_Tickers'
stock_tickers = pd.read_csv(stock_ticker_file).squeeze().tolist()

# Function to retrieve stock data
def fetch_stock_data(ticker_symbol, start_date, end_date, selected_attributes):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return stock_data[selected_attributes]

# User inputs for stock selection and date range
selected_ticker = st.selectbox("Select Stock Ticker", stock_tickers)
current_date = datetime.now().date()
start_date_column, end_date_column = st.columns(2)

with start_date_column:
    start_date = st.date_input("Start Date", max_value=current_date)

with end_date_column:
    end_date = st.date_input("End Date", max_value=current_date) + timedelta(days=1)

# User input for selecting data attributes
selected_attributes = st.multiselect("Select Attributes", ["Open", "High", "Low", "Close", "Volume", "Adj Close"])

# Fetch and display data when the button is clicked
if st.button(f"Show {selected_ticker} Data"):
    stock_data = fetch_stock_data(selected_ticker, start_date, end_date, selected_attributes)

    # Plot the data
    fig = go.Figure()
    for attribute in selected_attributes:
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[attribute], name=attribute))
    fig.update_layout(
        title=f"{selected_ticker} Stock Data",
        xaxis_title="Date",
        yaxis_title="Value"
    )
    st.plotly_chart(fig)
    st.markdown(f" #### {selected_ticker} Stock Data from {start_date} to {end_date}")
    st.write(stock_data)

    # Prepare and provide a CSV download
    stock_data_reset = stock_data.reset_index()
    stock_data_reset.rename(columns={'index': 'Date'}, inplace=True)
    csv_data = stock_data_reset.to_csv(index=False)
    csv_filename = f"{selected_ticker}_Stock_Data.csv"

    st.download_button(
        label=f"Download {selected_ticker} Data as CSV",
        data=csv_data,
        file_name=csv_filename,
        key=f"{csv_filename}-key"
    )
