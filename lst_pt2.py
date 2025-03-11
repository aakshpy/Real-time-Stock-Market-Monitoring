import streamlit as sl
from alpha_vantage.timeseries import TimeSeries
import pandas as p
import matplotlib.pyplot as plt

API_KEY="N8LB12BE4WMB81UK"

sl.title("Live Stock visualizer")

sym=sl.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc):")

if sym:
    try:
        ts = TimeSeries(key=API_KEY, output_format="pandas")
        data, meta_data = ts.get_intraday(symbol=sym, interval="5min", outputsize="compact")

        if data.empty:
            sl.error(f"No data available for {sym}. Please check the stock symbol or try a different one.")
        elif '4. close' not in data.columns:
            sl.error(f"No '4. close' data available for {sym}. API response may be incorrect.")
        else:
            data = data.sort_index()
            close_price = data['4. close']
            lat_price = close_price.iloc[-1]

            sl.write(f"**Latest Price of {sym} is:** ${lat_price:.2f}")

            fig, ax = plt.subplots()
            ax.plot(close_price.index, close_price, label="Stock Price", color="green")
            ax.set_title(f"Stock Price Trend of {sym}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Price in USD")
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            ax.grid(True)

            sl.pyplot(fig)

            sl.write("Stock Price Data")
            sl.dataframe(data.head())

    except Exception as e:
        sl.error(f"An error occurred: {str(e)}")

