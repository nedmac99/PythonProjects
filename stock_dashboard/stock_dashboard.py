'''
Date: The specific trading day for which the stock data is recorded.
Ticker: The unique symbol used to identify a company's stock on the exchange.
Open: The first price at which the stock traded after the market opened for the day.
High: The highest price the stock reached during the trading session.
Low: The lowest price the stock reached during the trading session.
Close: The final price at which the stock traded when the market closed, considered the standard measure of the day's value.
Volume: The total number of shares traded during the day, indicating market activity and liquidity.
'''

'''
Steps 0: What we're building 
- A compact market dashboard with: normalized price index, rolling volatility, moving averages, drawdowns, correlations, and monthly returns
- A metrics table (period return, annualized return, volatility, Sharpe≈, max drawdown) to summarize story

Steps 1: Data creation/loading
- Load in dataset for three tickers(AAPL, MSFT, SPY) using simple geometric Brownian motion. This guarantees the notebook runs anywhere (no internet needed)

Steps 2: Feature Engineering

'''