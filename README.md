# 📈 Forex Crossover Detection Bot 🔔 (Telegram Alerts)

This bot fetches real-time Forex market data, analyzes it using technical indicators (5 EMA, 8 SMA, RSI), detects bullish crossovers, and sends alerts to Telegram automatically. Built with Python, using `yfinance` and `python-telegram-bot`.

---

## 🚀 Features

- 💸 Monitors major Forex pairs (EUR/USD, GBP/USD, USD/JPY, etc.)
- 📊 Calculates:
  - 5-Period Exponential Moving Average (5 EMA)
  - 8-Period Simple Moving Average (8 SMA)
  - 14-Period Relative Strength Index (RSI)
- 🔄 Detects latest bullish EMA crossovers
- 🕒 Updates every 15 minutes
- 📲 Sends alerts to a Telegram chat with TradingView chart link
- 🕐 Converts timestamps to IST (Indian Standard Time)
- ✅ Clean and structured asynchronous code with error handling

e.g
Latest crossover detected for EURUSD=X!
 Datetime          Adj Close       5EMA       8SMA       RSI Crossover Point
2025-04-22 15:15   1.0965          1.0962     1.0958     63.2 Crossover
TradingView Link: https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD


