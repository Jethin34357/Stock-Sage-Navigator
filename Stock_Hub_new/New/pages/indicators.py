import streamlit as st
import pandas as pd
import pandas_datareader as data
import yfinance as yf
import ta
import base64
from datetime import date
import plotly.graph_objs as go
st.subheader("Stock Technical Indicators")
# Define function to add technical indicators
def add_technical_indicators(data, selected_indicators):
    for indicator in selected_indicators:
        if indicator == "Moving average of 20":
            data['Moving average of 20'] = ta.trend.sma_indicator(data['Close'], window=20)
        elif indicator == "Moving average of 50":
            data['Moving average of 50'] = ta.trend.sma_indicator(data['Close'], window=50)
        elif indicator == "Standard deviation":
            data['Standard deviation'] = ta.volatility.bollinger_mavg(data['Close'], window=20, fillna=True) - ta.volatility.bollinger_lband(data['Close'], window=20, window_dev=2, fillna=True)
        elif indicator == "Relative Strength Index":
            data['Relative Strength Index'] = ta.momentum.rsi(data['Close'], window=14)
        elif indicator == "Moving average convergence divergence":
            data['Moving average convergence divergence'] = ta.trend.macd(data['Close'])
        elif indicator == "Average Directional Index":
            try:
                data['Average Directional Index'] = ta.trend.adx(data['High'], data['Low'], data['Close'], window=14)
            except ValueError as e:
                st.warning(f"Unable to calculate ADX for {data['Ticker'][0]}: {e}")
                data.drop(columns=["Average Directional Index"], inplace=True)
        elif indicator == "Stochastic Oscillator (%K)":
            data['Stochastic Oscillator (%K)'] = ta.momentum.stoch(data['High'], data['Low'], data['Close'], window=14, smooth_window=3)
        elif indicator == "Stochastic Oscillator (%D)":
            data['Stochastic Oscillator (%D)'] = ta.momentum.stoch_signal(data['High'], data['Low'], data['Close'], window=14, smooth_window=3)
        elif indicator == "Bollinger Bands (bb_bbm)":
            data['Bollinger Bands (bb_bbm)'] = ta.volatility.bollinger_mavg(data['Close'], window=20)
        elif indicator == "Bollinger Bands (bb_bbh)":
            data['Bollinger Bands (bb_bbh)'] = ta.volatility.bollinger_hband(data['Close'], window=20, window_dev=2)
        elif indicator == "Bollinger Bands (bb_bbl)":
            data['Bollinger Bands (bb_bbl)'] = ta.volatility.bollinger_lband(data['Close'], window=20, window_dev=2)
        elif indicator == "Money Flow Index":
            data['Money Flow Index'] = ta.volume.money_flow_index(data['High'], data['Low'], data['Close'], data['Volume'], window=14)

    return data

# Define function to retrieve stock data within a specified date range
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", start=start_date, end=end_date)
    df['Ticker'] = ticker  # Add a column for the stock ticker symbol
    return df

# Define function to display stock chart with technical indicators
def display_stock_chart(ticker, data, selected_indicators):
    st.subheader(f"Close values for {ticker}")
    fig = go.Figure(data=go.Scatter(x=data.index, y=data['Close']))
    st.plotly_chart(fig)

    for indicator in selected_indicators:
        if indicator == "Moving average of 20":
            st.subheader(f"Moving average of 20 for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Moving average of 20'], name='SMA20'))
            st.plotly_chart(fig)

        if indicator == "Moving average of 50":
            st.subheader(f"Moving average of 50 for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Moving average of 50'], name='SMA50'))
            st.plotly_chart(fig)

        if indicator == "Standard deviation":
            st.subheader(f"Standard deviation for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Standard deviation']))
            st.plotly_chart(fig)

        if indicator == "Relative Strength Index":
            st.subheader(f"Relative Strength Index (RSI) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Relative Strength Index']))
            st.plotly_chart(fig)

        if indicator == "Moving average convergence divergence":
            st.subheader(f"Moving average convergence divergence (MACD) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Moving average convergence divergence']))
            st.plotly_chart(fig)

        if indicator == "Average Directional Index":
            st.subheader(f"Average Directional Index (ADX) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Average Directional Index']))
            st.plotly_chart(fig)

        if indicator == "Stochastic Oscillator (%K)":
            st.subheader(f"Stochastic Oscillator (%K) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Stochastic Oscillator (%K)']))
            st.plotly_chart(fig)

        if indicator == "Stochastic Oscillator (%D)":
            st.subheader(f"Stochastic Oscillator (%D) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Stochastic Oscillator (%D)']))
            st.plotly_chart(fig)

        if indicator == "Bollinger Bands (bb_bbm)":
            st.subheader(f"Bollinger Bands (bb_bbm) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Bollinger Bands (bb_bbm)']))
            st.plotly_chart(fig)

        if indicator == "Bollinger Bands (bb_bbh)":
            st.subheader(f"Bollinger Bands (bb_bbh) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Bollinger Bands (bb_bbh)']))
            st.plotly_chart(fig)

        if indicator == "Bollinger Bands (bb_bbl)":
            st.subheader(f"Bollinger Bands (bb_bbl) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Bollinger Bands (bb_bbl)']))
            st.plotly_chart(fig)

        if indicator == "Money Flow Index":
            st.subheader(f"Money Flow Index (MFI) for {ticker}")
            fig = go.Figure(data=go.Scatter(x=data.index, y=data['Money Flow Index']))
            st.plotly_chart(fig)

# Define function to export data as CSV file
def export_to_csv(data, ticker, selected_indicators):
    if not selected_indicators:
        return None

    selected_data = data[['Open', 'Close', 'High', 'Low', 'Volume'] + selected_indicators]
    csv = selected_data.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{ticker}_indicators.csv"><button style="background-color: #FF4B4B; color: white; padding: 0.5em 1em; border: none; border-radius: 4px; cursor: pointer;">Download {ticker} Indicators</button></a>'
    return href

stock_ticker_file = 'Tickers\Stock_Tickers'
stock_list = pd.read_csv(stock_ticker_file).squeeze().tolist()

# Add user input for selecting stocks to analyze
selected_stocks = st.multiselect('Select stocks to analyze', stock_list,  default=['GOOGL', 'AMZN'])

# Add user input for selecting start and end dates
today = date.today()
col1,col2 = st.columns(2)
with col1:
    start = st.date_input("Start date", date(2012, 1, 1), max_value=today)
with col2:
    end = st.date_input("End date", date(2022, 12, 31), max_value=today)

# Add multi-select input widget for technical indicators
technical_indicators = ["Moving average of 20", "Moving average of 50", "Standard deviation", "Relative Strength Index", "Moving average convergence divergence", "Average Directional Index", "Stochastic Oscillator (%K)", "Stochastic Oscillator (%D)", "Bollinger Bands (bb_bbm)", "Bollinger Bands (bb_bbh)", "Bollinger Bands (bb_bbl)", "Money Flow Index"]
selected_indicators = st.multiselect("Select technical indicators to display and download", technical_indicators)

# If at least one stock is selected, analyze them
if selected_stocks:
    for ticker in selected_stocks:
        # Retrieve stock data within the specified date range
        data = get_stock_data(ticker, start, end)
        # Add technical indicators to the data
        data = add_technical_indicators(data, selected_indicators)
        # Display stock chart with selected technical indicators
        st.write(f"## {ticker} Stock Price with Technical Indicators")
        display_stock_chart(ticker, data, selected_indicators)

        # Export selected technical indicators as a CSV file and display download button
        csv_link = export_to_csv(data, ticker, selected_indicators)
        if csv_link:
            st.markdown(csv_link, unsafe_allow_html=True)
else:
    st.write('Please select at least one stock to analyze.')
