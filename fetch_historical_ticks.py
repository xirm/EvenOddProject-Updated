import websocket
import json
import pandas as pd
from datetime import datetime, timedelta
import config

def get_unix_time(dt):
    return int(dt.timestamp())

def fetch_historical_data(volatility, start_time, end_time):
    ws = websocket.WebSocket()
    ws.connect(config.config['websocket_url'])
    
    auth_request = {
        "authorize": config.config['api_key']
    }
    ws.send(json.dumps(auth_request))
    
    request = {
        "ticks_history": volatility,
        "start": get_unix_time(start_time),
        "end": get_unix_time(end_time),
        "count": 1000,
        "style": "ticks"
    }
    ws.send(json.dumps(request))
    
    response = ws.recv()
    ws.close()
    return response

# Define time range
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)

# Fetch data for each volatility
for volatility in config.config['volatilities']:
    response = fetch_historical_data(volatility, start_time, end_time)
    with open(f'{volatility}_data.json', 'w') as file:
        file.write(response)
