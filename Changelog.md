# ChangeLog

## Version Alpha 1 (Initial Prototype - `lst_pt1.py`)
- Implemented basic **stock data retrieval** using `yfinance`.
- Allowed users to enter a stock symbol and fetch the latest price.
- Displayed stock price but **lacked visualization and error handling**.

---

## Version Alpha 2 (Prototype V2 - `lst_pt2.py`)
- **Switched API** from `yfinance` to `Alpha Vantage`.
- Introduced **intraday stock data fetching** with a 5-minute interval.
- **Added Matplotlib visualization** to display stock price trends.
- Implemented **error handling** for invalid stock symbols.
- Displayed stock price trends in a **line chart**.
- **Known Issues:** UI layout was basic, and chart design needed improvement.

---

## Version Alpha 3 (Prototype V3 - `lst_pt3.py`)
- Changed **time interval from 5 minutes to 30 minutes** for better visualization.
- Replaced Matplotlib with **Altair for interactive charts**.
- Improved **data table layout** for better readability.
- **Known Issues:** The app still lacked **caching and UI enhancements**.

---

## Version 1.0 (**Project Streamlit**) (RTSMM - `RTSMM.py`)
- **Implemented caching (`st.cache_data`)** to optimize API calls.
- Integrated **Plotly for smoother and more interactive visualizations**.
- Added a **company name fetch feature** to display stock details.
- Improved **error handling** with meaningful warnings and feedback. 
- Fixed **bugs related to missing stock data and API failures**.
- **Future Plan:** Integrate **Gemini API for AI-based stock forecasting**.

---

## Version 1.1 (RTSMM V2 - `RTSMM_V2.py`)
- Integrated **Gemini to provide stock predictions and investment recommendations.**
- Improved **error handling.**
- UI Enhancements.