import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
from newsapi import NewsApiClient
import math

# Set up the Streamlit app
st.subheader("Stock News")

# Function to get emoji based on sentiment score
def get_sentiment_emoji(sentiment_score):
    if sentiment_score > 0:
        return "😃 (Positive Sentiment)"
    elif sentiment_score < 0:
        return "😔 (Negative Sentiment)"
    else:
        return "😐 (Neutral Sentiment)"

# Function to fetch news articles
def fetch_news_articles(ticker, api_key, date_range):
    news_api = NewsApiClient(api_key=api_key)
    return news_api.get_everything(
        q=ticker,
        language='en',
        from_param=date_range['from_date'],
        to=date_range['to_date'],
        sort_by='relevancy',
        page_size=100
    )

# Function to display articles
def display_articles(articles, start_index, end_index, total_articles):
    for article in articles:
        st.write('---')
        st.write(f"**Title:** [{article['title']}]({article['url']})")
        st.write(f"**Description:** {article['description']}")
        st.write(f"**Source:** {article['source']['name']}")

        # Perform sentiment analysis
        sentiment_analysis = TextBlob(article['description'])
        sentiment_score = sentiment_analysis.sentiment.polarity
        sentiment_emoji = get_sentiment_emoji(sentiment_score)
        st.write(f"**Sentiment:** {sentiment_score:.2f} {sentiment_emoji}")

    st.write(f"Showing articles {start_index + 1} - {end_index} out of {total_articles}")

# Load stock tickers
stock_ticker_file = 'Tickers\Stock_Tickers'
stock_list = pd.read_csv(stock_ticker_file).squeeze().tolist()

# User input
selected_ticker = st.selectbox('Select stocks to analyze', stock_list)
st.subheader(f"News articles related to {selected_ticker}")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# Initialize parameters
api_key = '517da00e19094775ae25b3cbf6dfaa80'
date_range = {
    'from_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
    'to_date': datetime.now().strftime('%Y-%m-%d')
}

# Fetch news articles
news_data = fetch_news_articles(selected_ticker, api_key, date_range)

# Handle pagination
if news_data['totalResults'] == 0:
    st.write('No news articles found')
else:
    total_articles = news_data["totalResults"]
    articles_per_page = 5
    num_of_pages = math.ceil(total_articles / articles_per_page)

    # Pagination controls
    col1, col2 = st.columns([9, 1])
    with col1:
        if st.button('Previous') and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
    with col2:
        if st.button('Next') and st.session_state.current_page < num_of_pages:
            st.session_state.current_page += 1

    # Display current page articles
    start_index = (st.session_state.current_page - 1) * articles_per_page
    end_index = start_index + articles_per_page
    articles = news_data['articles'][start_index:end_index]

    display_articles(articles, start_index, end_index, total_articles)
