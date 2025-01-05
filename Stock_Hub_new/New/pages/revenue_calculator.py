import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Set up the subheader
st.subheader("Stock Revenue Calculator")

# Path to the file containing stock tickers
ticker_file_path = 'Tickers\Stock_Tickers'
stock_tickers = pd.read_csv(ticker_file_path).squeeze().tolist()

# Function to calculate return and final amount
def calculate_investment_return(ticker_symbol, start_date, end_date, invested_amount):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    if stock_data.empty:
        return None, None
    closing_prices = stock_data['Close']
    if len(closing_prices) < 2:
        st.error("Not enough data to calculate returns. Please choose a different date range.")
        return None, None
    initial_price = closing_prices.iloc[0]
    final_price = closing_prices.iloc[-1]
    return_rate, final_amount = compute_total_return(initial_price, final_price, invested_amount)
    return return_rate, final_amount

# Function to compute total return and final amount
def compute_total_return(initial_price, final_price, initial_investment):
    return_rate = (final_price / initial_price) - 1
    final_amount = initial_investment * (1 + return_rate)
    return return_rate, final_amount

# User inputs for stock ticker and dates
selected_ticker = st.selectbox("Select Stock Ticker", stock_tickers)
max_date = datetime.now().date()
column1, column2 = st.columns(2)

with column1:
    start_date = st.date_input("Start Date", max_value=max_date)
    
with column2:
    end_date = st.date_input("End Date", max_value=max_date) + timedelta(days=1)

invested_amount = st.number_input("Invested Amount (in dollars)", min_value=0.0, format="%.2f")

if st.button("Calculate"):
    # Perform calculations
    return_rate, final_amount = calculate_investment_return(selected_ticker, start_date, end_date, invested_amount)
    if return_rate is None:
        st.write("Calculation could not be performed as start and end dates are same.")
    else:
        profit_or_loss = final_amount - invested_amount
        
        # Determine styling based on profit or loss
        if profit_or_loss >= 0:
            result_color = "green"
            result_message = f"Your total profit is ${profit_or_loss:.2f}."
        else:
            result_color = "red"
            result_message = f"Your total loss is ${abs(profit_or_loss):.2f}."

        # Display the results
        st.markdown(
            f'<p>If you had invested <strong>${invested_amount:.2f}</strong> in <strong>{selected_ticker}</strong> stock from <strong>{start_date}</strong> to <strong>{end_date}</strong>, the investment would be worth <strong>${final_amount:.2f}</strong>.</p>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<p style="color: {result_color}">{result_message}</p>',
            unsafe_allow_html=True
        )
        
        # Create and display summary table
        summary_data = pd.DataFrame({
            "Stock Ticker": [selected_ticker],
            "Start Date": [start_date],
            "End Date": [end_date],
            "Invested Amount": [invested_amount],
            "Profit/Loss": [profit_or_loss]
        })
        
        st.write("Summary Table:")
        st.write(summary_data)
