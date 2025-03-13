import streamlit as sl
from alpha_vantage.timeseries import TimeSeries
import pandas as p
import altair as alt

API_KEY="N8LB12BE4WMB81UK"

sl.title("Live Stock visualizer")

sym=sl.text_input("Enter Stock Symbol (e.g AAPL, TSLA, etc):")

if sym:
    try:
        ts = TimeSeries(key=API_KEY, output_format="pandas")
        data, meta_data = ts.get_intraday(symbol=sym, interval="30min", outputsize="compact")

        if data.empty:
            sl.error(f"No data available for {sym}. Please check the stock symbol or try a different one.")
        elif '4. close' not in data.columns:
            sl.error(f"No '4. close' data available for {sym}. API response may be incorrect.")
        else:
            data = data.sort_index()
            close_price = data['4. close']
            lat_price = close_price.iloc[-1]

            sl.write(f"**Latest Price of {sym} is:** ${lat_price:.2f}")

            # Reset index and properly format the Time column
            df = data.reset_index()
            df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['Time'] = p.to_datetime(df['Time'])  # Convert to datetime format
            df = df.sort_values(by='Time')  # Ensure proper chronological order
            
            # Display the table
            sl.dataframe(df) 

            # Create the chart
            chart = alt.Chart(df).mark_line(color='green').encode(
                x=alt.X('Time:T', title='Time'),
                y=alt.Y('Close:Q', title='Price in USD'),
                tooltip=['Time', 'Close']
            ).properties(
                title=f"Stock Price Trend of {sym}",
                width=700
            ).interactive()

            sl.altair_chart(chart, use_container_width=True)    

    except Exception as e:
        sl.error(f"An error occurred: {str(e)}")


