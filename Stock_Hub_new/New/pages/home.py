import streamlit as st
import yfinance as yf
import pandas as pd
import math

ticker_list = pd.read_csv('Tickers\Stock_Tickers').squeeze().tolist()

tab1, tab2= st.tabs(["Company Insights", "Ticker Insights Report"])
with tab1:
    col1, col2, col3,col4 = st.columns([3, 1, 1, 1],gap="large")
    with col1:
        selected_tickers = st.multiselect('Search and Select Stock Ticker(s)', ticker_list)

    if len(selected_tickers) == 0:
        selected_tickers = ticker_list

    tickers_per_page = 9
    total_pages = math.ceil(len(selected_tickers) / tickers_per_page)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
        
    if selected_tickers != st.session_state.get('last_selected_tickers'):
        st.session_state.page_number = 1
        st.session_state.last_selected_tickers = selected_tickers

    
    with col2:
        if st.button("Previous") and st.session_state.page_number > 1:
            st.session_state.page_number -= 1
    with col4:
        if st.button("Next") and st.session_state.page_number < total_pages:
            st.session_state.page_number += 1
    with col3:
        st.write(f"Page {st.session_state.page_number} of {total_pages}")

    start_index = (st.session_state.page_number - 1) * tickers_per_page
    end_index = start_index + tickers_per_page
    current_tickers = selected_tickers[start_index:end_index]

    for i in range(0, len(current_tickers), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(current_tickers):
                tickerSymbol = current_tickers[i + j]
                tickerData = yf.Ticker(tickerSymbol)
                string_name = tickerData.info.get('longName')
                symbol = tickerData.info.get('symbol')
                address1 = tickerData.info.get('address1')
                city = tickerData.info.get('city')
                state = tickerData.info.get('state')
                country = tickerData.info.get('country')
                industry = tickerData.info.get('industry')
                sector = tickerData.info.get('sector')
                previousClose = str(tickerData.info.get('previousClose'))
                exchange = str(tickerData.info.get('exchange'))
                full_time_employees = str(tickerData.info.get('fullTimeEmployees'))
                website = tickerData.info.get('website')
                longBusinessSummary = tickerData.info.get('longBusinessSummary')
                companyOfficers = tickerData.info.get('companyOfficers')

                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"### {string_name}\n##### ({symbol})")
                        if address1 and city and state and country:
                            st.write(f"**Headquarters :** {address1}, {city}, {state}, {country}")
                        if industry:
                            st.write(f"**Industry :** {industry}")
                        if sector:
                            st.write(f"**Sector :** {sector}")
                        if previousClose:
                            st.write(f"**Previous Close :** {previousClose}")
                        if exchange:
                            st.write(f"**Exchange :** {exchange}")
                        if full_time_employees:
                            st.write(f"**Employees :** {full_time_employees}")
                        if longBusinessSummary: 
                            with st.popover("Business Summary"):
                                st.info(longBusinessSummary)
                        if companyOfficers: 
                            with st.popover("Company Officers"):
                                st.dataframe(companyOfficers)
                        if website:
                            st.markdown(f'**Website :** [{string_name}]({website})')

with tab2:
    tickerSymbols = st.multiselect('Select stock tickers', ticker_list, default=['GOOGL', 'AMZN', 'NVDA', 'MSFT']) 
    for tickerSymbol in tickerSymbols:
        tickerData = yf.Ticker(tickerSymbol) 
        with st.expander(f'{tickerSymbol}', expanded=False, icon=":material/account_tree:"):
            st.write(tickerData.info)
            
            st.markdown(f'##### {tickerSymbol} Income Statement')
            st.write(tickerData.income_stmt)

            st.markdown(f'##### {tickerSymbol} Balance Sheet')
            st.write(tickerData.balance_sheet)

            st.markdown(f'##### {tickerSymbol} Latest News')
            st.dataframe(tickerData.news)

            st.markdown(f'##### {tickerSymbol} Major Holders')
            st.write(tickerData.major_holders)
        
            st.markdown(f'##### {tickerSymbol} Institutional Holders')
            st.write(tickerData.institutional_holders)
            
            st.markdown(f'##### {tickerSymbol} Mutual Fund Holders')
            st.write(tickerData.mutualfund_holders)
            
            st.markdown(f'##### {tickerSymbol} Insider Transactions')
            st.write(tickerData.insider_transactions)
            
            st.markdown(f'##### {tickerSymbol} Insider Purchases')
            st.write(tickerData.insider_purchases)
            
            st.markdown(f'##### {tickerSymbol} Insider Roster Holders')
            st.write(tickerData.insider_roster_holders)
            
            st.markdown(f'##### {tickerSymbol} Recommendations')
            st.write(tickerData.recommendations)
            
            st.markdown(f'##### {tickerSymbol} Recommendations Summary')
            st.write(tickerData.recommendations_summary)
            
            st.markdown(f'##### {tickerSymbol} Upgrades and Downgrades')
            st.write(tickerData.upgrades_downgrades)

