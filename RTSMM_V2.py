import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import google.generativeai as genai

# API Keys
ALPHA_VANTAGE_API_KEY = "N8LB12BE4WMB81UK"
genai.configure(api_key="AIzaSyCmuKjn1l2YSccuZsiB-xiN1ezrXg8MAg8")

# Function to fetch stock data from Alpha Vantage
@st.cache_data
def fetch_stock_data(symbol, interval):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact"
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
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey=N8LB12BE4WMB81UK"
    response = requests.get(url)
    data = response.json()
    
    if "bestMatches" in data and len(data["bestMatches"]) > 0:
        return data["bestMatches"][0]["2. name"]
    return "Unknown Company"


# Function to fetch AI stock predictions from Gemini
def get_stock_prediction(stock_data):
    prompt = f"""
    Analyze the following stock market data:
    - Open Price: {stock_data['o']}
    - High Price: {stock_data['h']}
    - Low Price: {stock_data['l']}
    - Close Price: {stock_data['c']}
    - Previous Close: {stock_data['pc']}
    - Percentage Change: {stock_data['dp']}%
    
    **Instructions:**
    1️⃣ Assign probabilities for **each outcome** in the next **15 minutes** and **1 hour**:
       - 📈 Probability of price increase (%)
       - 📉 Probability of price decrease (%)
       - ➡️ Probability of price staying stable (%)
    
    2️⃣ If the probability of increase is **above 60%**, **recommend Buy**.  
       If the probability of decrease is **above 60%**, **recommend Sell**.  
       Otherwise, **recommend Hold**.

    **Output format:**
    **Probability Estimation (Next 15 Minutes)**  
    📈 Increase: XX%  
    📉 Decrease: XX%  
    ➡️ Stable: XX%  

    **Probability Estimation (Next 1 Hour)**  
    📈 Increase: XX%  
    📉 Decrease: XX%  
    ➡️ Stable: XX%  

    📢 **Recommendation: Buy/Hold/Sell**  
    (Explain decision in 2-3 lines)  
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  
    response = model.generate_content(prompt)
    
    return response.text  # Return AI-generated prediction

# Streamlit UI Setup
st.set_page_config(page_title="Stock Price Dashboard", layout="wide")
st.title("📈 Real-Time Stock Monitoring Dashboard")

selected_symbol = st.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc):").strip().upper()
intervals = ["1min", "5min", "15min", "30min", "60min"]
selected_interval = st.selectbox("Select time interval:", intervals, index=2)

if selected_symbol:
    company_name = fetch_company_name(selected_symbol)
    st.subheader(f"Stock Data for {selected_symbol} ({company_name})")
    df = fetch_stock_data(selected_symbol, selected_interval)
    
    if df is not None:
        latest_data = df.iloc[-1]  # Get the latest stock data
        stock_data = {
            "o": float(latest_data["Open"]),
            "h": float(latest_data["High"]),
            "l": float(latest_data["Low"]),
            "c": float(latest_data["Close"]),
            "pc": float(df.iloc[-2]["Close"]) if len(df) > 1 else float(latest_data["Close"]),
            "dp": round(((float(latest_data["Close"]) - float(df.iloc[-2]["Close"])) / float(df.iloc[-2]["Close"])) * 100, 2) if len(df) > 1 else 0.0
        }
        
        st.dataframe(df.tail(7))
        
        # Plot stock price trend
        fig = px.line(df, x=df.index, y="Close", title=f"Stock Price Trend of {selected_symbol}", labels={"index": "Time", "Close": "Price in USD"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Fetch AI prediction
        with st.spinner("Fetching AI prediction..."):
            ai_prediction = get_stock_prediction(stock_data)
        
        st.subheader("What does Gemini think?")
        st.write(ai_prediction)
    else:
        st.warning("⚠️ Invalid stock symbol! Please check and try again.")
elif selected_symbol == "":
    st.info("🔍 Please enter a stock symbol to fetch data.")
