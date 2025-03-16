📈 Real time Stock Market Monitoring

   A Streamlit based real time stock market monitoring powered by Alpha Vantage API.

   What is expected: 

✅ Fetches Real-time stock data from the user defined Stock Symbols.
✅ Stock market trend for the user defined stock symbol is visualized in an
    interactive manner using Plotly
✅ Optimized performance with cached API requests.

    Future features:
☑️ Integration of Gemini for forecasting of the stock market trend and investment
    recommendation based on stock market trend and predictions.
☑️ Dark/Light mode toggle for an improved UI experience.
☑️ Auto-Refresh option to allow the user to refresh the stock data at regular intervals.
☑️ A sidebar with extra options like company profile, market capital ,etc.

    What to look out for:
❌ Alpha Vantage (which is the API being implemented) limits free users to 5
    API calls, which means is the user exceeds the user limit, they get API limit
    errors.
❌ As of now, the app program doesn't handle timeout errors.
❌ The app may take a long time to output data. Especially for uncached stock
    symbols.
❌ Any other bugs please let me know 😁

🛠️ Installation and Set-up:
 1) Clone the repository:
      Navigate to the directory you wish to save the repository using "cd" command.

      In the terminal/git-bash enter:
        "git clone https://github.com/aakshpy/Real-time-Stock-Market-Monitoring.git" 
 2) Install required dependencies:
      run the command:
        "pip install -r requirements.txt"
 3) Run the application:
      run the command:
        "streamlit run RTSMM.py"

Thank you using my application!♥️ 