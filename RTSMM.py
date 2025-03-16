import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_KEY = "N8LB12BE4WMB81UK"

#Function to fetch stock data with caching
@st.cache_data
def fetch_stock_data(symbol, interval):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    
    if f"Time Series ({interval})" in data:
        df = pd.DataFrame.from_dict(data[f"Time Series ({interval})"], orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df
    else:
        return None

#Function to fetch company name with caching
@st.cache_data
def fetch_company_name(symbol):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "bestMatches" in data and len(data["bestMatches"]) > 0:
        return data["bestMatches"][0]["2. name"]
    return "Unknown Company"


st.set_page_config(page_title="Stock Price Dashboard", layout="wide")
st.title("📈 Live Stock Price Dashboard")

selected_symbol = st.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc):").strip().upper()

intervals = ["1min", "5min", "15min", "30min", "60min"]
selected_interval = st.selectbox("Select time interval:", intervals, index=2)

if selected_symbol:
    company_name = fetch_company_name(selected_symbol)
    st.subheader(f"Stock Data for {selected_symbol} ({company_name})")
    df = fetch_stock_data(selected_symbol, selected_interval)
    
    if df is not None:
        st.dataframe(df.tail(7))
        
        # Plot stock price trend
        fig = px.line(df, x=df.index, y="Close", title=f"Stock Price Trend of {selected_symbol}", labels={"index": "Time", "Close": "Price in USD"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Invalid stock symbol! Please check and try again.")
elif selected_symbol == "":
    st.info("🔍 Please enter a stock symbol to fetch data.")
