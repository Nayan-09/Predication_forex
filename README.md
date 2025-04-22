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

