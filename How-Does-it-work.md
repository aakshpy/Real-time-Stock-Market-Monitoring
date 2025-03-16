# Code Explanation

## **1️⃣ Importing Necessary Libraries**
```python
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
```
🔹 `streamlit` → Used for building the web UI.  
🔹 `pandas` → Handles data manipulation.  
🔹 `requests` → Fetches stock data from Alpha Vantage API.  
🔹 `plotly.express` → Creates interactive stock price charts.  

---

## **2️⃣ API Key for Alpha Vantage**
```python
API_KEY = "N8LB12BE4WMB81UK"
```
🔹 Required to fetch stock data from **Alpha Vantage API**.  

---

## **3️⃣ Fetching Stock Data (with Caching)**
```python
@st.cache_data
def fetch_stock_data(symbol, interval):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
```
🔹 `@st.cache_data` → Caches API results to reduce redundant calls.  
🔹 Fetches real-time stock prices for a user-defined **symbol & interval**.  

---

## **4️⃣ Processing API Data**
```python
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
```
🔹 Converts JSON data into a **Pandas DataFrame**.  
🔹 Renames columns for better readability.  
🔹 Returns **sorted** stock data.  

---

## **5️⃣ Fetching Company Name (with Caching)**
```python
@st.cache_data
def fetch_company_name(symbol):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
```
🔹 Fetches **company name** using Alpha Vantage's `SYMBOL_SEARCH` API.  

---

## **6️⃣ Extracting Company Name**
```python
if "bestMatches" in data and len(data["bestMatches"]) > 0:
    return data["bestMatches"][0]["2. name"]
return "Unknown Company"
```
🔹 Returns **best-matched company name**.  
🔹 If no match is found, returns `"Unknown Company"`.  

---

## **7️⃣ Streamlit UI Setup**
```python
st.set_page_config(page_title="Stock Price Dashboard", layout="wide")
st.title("📈 Live Stock Price Dashboard")
```
🔹 Sets **page title & layout**.  
🔹 Creates a **header** for the dashboard.  

---

## **8️⃣ User Input for Stock Symbol**
```python
selected_symbol = st.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc):").strip().upper()
```
🔹 Creates an **input box** for the stock symbol.  
🔹 Ensures **uppercase formatting**.  

---

## **9️⃣ Dropdown for Time Interval Selection**
```python
intervals = ["1min", "5min", "15min", "30min", "60min"]
selected_interval = st.selectbox("Select time interval:", intervals, index=2)
```
🔹 Allows users to select a time interval for stock data.  
🔹 Default selection: `15min`.  

---

## **🔟 Fetching & Displaying Stock Data**
```python
if selected_symbol:
    company_name = fetch_company_name(selected_symbol)
    st.subheader(f"Stock Data for {selected_symbol} ({company_name})")
    df = fetch_stock_data(selected_symbol, selected_interval)
```
🔹 Calls **fetch_company_name()** to retrieve company details.  
🔹 Calls **fetch_stock_data()** to get stock prices.  
🔹 Displays **stock symbol & company name**.  

---

## **1️⃣1️⃣ Displaying Stock Data in a Table**
```python
if df is not None:
    st.dataframe(df.tail(7))
```
🔹 Shows the **latest 7 stock price entries**.  
🔹 Uses `st.dataframe()` for an **interactive table**.  

---

## **1️⃣2️⃣ Plotting Stock Price Trends**
```python
fig = px.line(df, x=df.index, y="Close",
              title=f"Stock Price Trend of {selected_symbol}",
              labels={"index": "Time", "Close": "Price in USD"})
st.plotly_chart(fig, use_container_width=True)
```
🔹 Uses **Plotly** to create an interactive **line chart**.  
🔹 Displays stock price movement over time.  

---

## **1️⃣3️⃣ Error Handling & Warnings**
```python
else:
    st.warning("⚠️ Invalid stock symbol! Please check and try again.")
```
🔹 Displays a warning message if the stock symbol is invalid.  

---

## **1️⃣4️⃣ Reminder to Enter a Stock Symbol**
```python
elif selected_symbol == "":
    st.info("🔍 Please enter a stock symbol to fetch data.")
```
🔹 If **no input is provided**, a reminder is shown.  

---
