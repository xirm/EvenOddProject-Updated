import asyncio
import websockets
import json
from datetime import datetime
from collections import Counter
import requests
import logging
import csv
import os

# Configuration
config = {
    "api_key": "DKJDby0RQlQy1iN",
    "api_url": "https://api.deriv.com",
    "websocket_url": "wss://ws.binaryws.com/websockets/v3?app_id=1089",
    "volatilities": ["R_10", "R_25", "R_50", "R_75", "R_100"],
    "data_file": "tick_data.csv"  # File to save tick data
}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to save tick data to a CSV file
def save_to_csv(data, file_name):
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if file does not exist
        if not file_exists:
            writer.writerow(['timestamp', 'tick', 'last_digit', 'volatility', 'trend', 'volatility_measure'])
        
        writer.writerow(data)

# Function to create the ticks history request
def create_ticks_history_request(symbol, count):
    return {
        "ticks_history": symbol,
        "adjust_start_time": 1,
        "count": count,
        "end": "latest",
        "start": 1,
        "style": "ticks"
    }

def extract_last_digit(quote):
    try:
        return int(str(quote).split('.')[-1][-1])
    except (ValueError, IndexError):
        logging.error(f"Error extracting last digit from quote: {quote}")
        return -1

def calculate_trend(ticks):
    return sum([ticks[i] - ticks[i - 1] for i in range(1, len(ticks))])

def calculate_volatility(ticks):
    if len(ticks) < 2:
        return 0
    return max(ticks) - min(ticks)

async def fetch_data(url, request_data):
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps(request_data))
        response = await websocket.recv()
        data = json.loads(response)
        if 'error' in data:
            logging.error(f"Error: {data['error']['message']}")
        return data

async def analyze_and_save(symbol):
    tick_requests = [
        create_ticks_history_request(symbol, 60),
        create_ticks_history_request(symbol, 300),
        create_ticks_history_request(symbol, 1800)
    ]
    
    for request in tick_requests:
        data = await fetch_data(config['websocket_url'], request)
        if 'history' in data:
            quotes = data['history']['prices']
            ticks = [extract_last_digit(q) for q in quotes]
            
            most_common, least_common = calculate_most_least_digits(ticks)
            trend = calculate_trend(ticks)
            volatility = calculate_volatility(ticks)
            
            timestamp = datetime.now().isoformat()
            for tick in ticks:
                save_to_csv(
                    [timestamp, tick, extract_last_digit(tick), symbol, 
                     'uptrend' if trend > 0 else 'downtrend' if trend < 0 else 'neutral', 
                     volatility],
                    config['data_file']
                )

            logging.info(f"Data saved for {symbol} with {len(ticks)} records.")

def calculate_most_least_digits(digits):
    digit_count = Counter(digits)
    most_common = digit_count.most_common(1)[0][0] if digit_count else -1
    least_common = digit_count.most_common()[-1][0] if digit_count else -1
    return most_common, least_common

async def main():
    symbols = config['volatilities']
    tasks = [analyze_and_save(symbol) for symbol in symbols]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
