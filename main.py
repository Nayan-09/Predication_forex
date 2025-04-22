import yfinance as yf
import pandas as pd
import pytz
import time
import asyncio
import signal
import sys
from telegram import Bot
from telegram.error import TelegramError

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Variable to store the last sent data for each forex pair
last_sent_data = {}

# Function to send messages to Telegram (asynchronous)
async def send_to_telegram(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}")

# Function to fetch historical forex data
def fetch_historical_forex_data(ticker, interval):
    try:
        print(f"Fetching historical data for {ticker} with interval {interval}...")
        data = yf.download(ticker, interval=interval, period="1d")  # Fetch 1-day data with the given interval
        if data.empty:
            print(f"No data found for {ticker} ({interval}).")
            return None
        data.reset_index(inplace=True)  # Ensure 'Datetime' is a column
        return data
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return None

# Function to calculate indicators (5 EMA, 8 SMA, RSI)
def calculate_indicators(data):
    data["5EMA"] = data["Adj Close"].ewm(span=5, adjust=False).mean()
    data["8SMA"] = data["Adj Close"].rolling(window=8).mean()
    delta = data["Adj Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    return data

# Function to find the latest crossover (and check RSI condition)
def find_latest_crossover(data):
    # Calculate the crossover condition
    data["Crossover"] = (data["5EMA"] > data["8SMA"]) & (data["5EMA"].shift(1) <= data["8SMA"].shift(1))
    data["Crossover Point"] = data["Crossover"].apply(lambda x: "Crossover" if x else "No Crossover")
    
    # Filter for the most recent crossover
    latest_crossover = data[data["Crossover"]]
    if not latest_crossover.empty:
        latest_crossover = latest_crossover.tail(1)  # Get the last crossover point
        return latest_crossover[["Datetime", "Adj Close", "5EMA", "8SMA", "RSI", "Crossover Point"]]
    return None

# Function to convert Datetime column to IST
def convert_to_ist(data):
    ist = pytz.timezone('Asia/Kolkata')  # IST timezone
    if 'Datetime' in data.columns:
        data['Datetime'] = data['Datetime'].apply(lambda x: x.tz_localize(pytz.utc).astimezone(ist) if x.tzinfo is None else x.astimezone(ist))
    return data

# Function to generate TradingView link for a given forex pair
def generate_tradingview_link(ticker):
    symbol = ticker.split("=")[0]  # Remove the =X part to get the actual symbol
    tradingview_link = f"https://www.tradingview.com/chart/?symbol=OANDA%3A{symbol}&interval=15"
    return tradingview_link

# Function to process forex pair for historical data
async def process_forex_pair_historical(ticker, interval):
    data = fetch_historical_forex_data(ticker, interval)
    if data is None:
        return

    data = calculate_indicators(data)
    data = convert_to_ist(data)  # Convert Datetime to IST
    
    latest_crossover = find_latest_crossover(data)

    # If a crossover was found, send the message
    if latest_crossover is not None:
        current_state = latest_crossover.to_string(index=False)
    else:
        current_state = "No crossover"

    # Check if the state has changed since the last time
    if last_sent_data.get(ticker) != current_state:
        if current_state != "No crossover":
            message = f"Latest crossover detected for {ticker}!\n{current_state}\nTradingView Link: {generate_tradingview_link(ticker)}"
        else:
            message = f"No crossover for {ticker} at this time.\nTradingView Link: {generate_tradingview_link(ticker)}"
        
        await send_to_telegram(message)

        # Update the last_sent_data dictionary with the current state
        last_sent_data[ticker] = current_state

# Function to check historical crossovers for a list of forex pairs
async def check_forex_crossovers(forex_pairs, interval="15m"):  # Changed interval to 15 minutes
    for pair in forex_pairs:
        await process_forex_pair_historical(pair, interval)

# Function to handle the program termination and send alert
def handle_exit_signal(signal, frame):
    print("Program is being stopped or interrupted.")
    asyncio.run(send_to_telegram("Program stopped or interrupted! Connection lost."))
    sys.exit(0)

# Main execution with continuous running (asynchronous)
async def main():
    forex_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X", "AUDUSD=X", "NZDUSD=X", "USDCAD=X"]
    
    # Handling termination signals (e.g., SIGINT for Ctrl+C)
    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)
    
    while True:  # Infinite loop to keep the program running
        await check_forex_crossovers(forex_pairs, interval="15m")  # Check historical data for crossovers
        print("Sleeping for 15 minutes...\n")
        await asyncio.sleep(900)  # Sleep for 15 minutes (900 seconds)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
