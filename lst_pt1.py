import streamlit as sl
import yfinance as yf

sl.title("Live Stock visualizer")

sym=sl.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc): ")

if sym:
    stock=yf.Ticker(sym)
    stock_info=stock.history(period="1d")

    if not stock_info.empty:
        lat_price=stock_info["Close"].iloc[-1]
        sl.write(f"Latest Price of {sym} : ${lat_price:.2f}")
    else:
        st.error("No data available for the given Stock Symbol")
