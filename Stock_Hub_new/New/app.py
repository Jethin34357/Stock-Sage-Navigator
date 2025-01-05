import streamlit as st
st.set_page_config(
    page_title="Stock Sense",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
from datetime import datetime
import time 
import os

col1, col2 = st.columns([1, 9], vertical_alignment="bottom")
with col1:
    st.image("Images/App_Logo/Small_Logo.png", width=35)
with col2:
    st.header("Stock Sense")

# with st.sidebar:
    # st.logo(
    #     "Images\App_Logo\Full_Logo.png",
    #     icon_image="Images\App_Logo\Small_Logo.png",
    # )

pages = {
    "Home": [
        st.Page("pages/home.py", title="Home", icon="🏠"),
    ],
    "Stock Prediction": [
        st.Page("pages/prediction.py", title="Stock Prediction", icon="📈"),
    ],
    "Stock News": [
        st.Page("pages/news.py", title="Stock News", icon="📰"),
    ],
    "Stock Comparison": [
        st.Page("pages/comparison.py", title="Stock Comparison", icon="📊"),
    ],
    "Technical Indicators": [
        st.Page("pages/indicators.py", title="Technical Indicators", icon="🔍"),
    ],
    "Revenue Calculator": [
        st.Page("pages/revenue_calculator.py", title="Revenue Calculator", icon="💵"),
    ],
    "Download Stock Data": [
        st.Page("pages/stock_data.py", title="Download Stock Data", icon="⬇️")]
   
}

pg = st.navigation(pages)
pg.run()

def save_text_to_file(text):
    with open("Insights.txt", "a") as file:
        file.write(text + "\n")

with st.sidebar:
    st.subheader("Add Insights")
    insights_text = st.text_area("Type your insights here", height=200)
    current_time = datetime.now().strftime("%H:%M - %d/%m/%Y")
    insights_text_with_datetime = f"{current_time}\n{insights_text}\n\n"

    if st.button("Save Insights"):
        save_text_to_file(insights_text_with_datetime)
        st.markdown('<style>div[data-baseweb="toast"] div {color: green;}</style>', unsafe_allow_html=True)
        st.toast('Insights saved successfully!')
        time.sleep(.5)

    if not os.path.exists("Insights.txt"):
        with open("Insights.txt", "w") as file:
            file.write("Stock Hub(Insights): \n\n")

