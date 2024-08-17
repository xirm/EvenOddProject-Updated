import json
from datetime import datetime, timedelta, timezone
import websocket
from config import config

def fetch_historical_data(volatility, start, end):
    url = config['websocket_url']
    headers = {
        "Authorization": f"Bearer {config['api_key']}"
    }
    
    all_messages = []

    def on_message(ws, message):
        data = json.loads(message)
        print("Received data:", data)
        all_messages.append(data)

        # Close the connection after receiving the data
        if 'history' in data:
            ws.close()

    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_message=on_message
    )
    
    request = {
        "ticks_history": volatility,
        "start": start,
        "end": end,
        "count": 100,  # Number of ticks to request
    }
    
    ws.on_open = lambda ws: ws.send(json.dumps(request))
    ws.run_forever()

    # Combine all received messages
    combined_data = {}
    for message in all_messages:
        if 'history' in message:
            if 'prices' in combined_data:
                combined_data['prices'].extend(message['history']['prices'])
                combined_data['times'].extend(message['history']['times'])
            else:
                combined_data = message['history']

    # Save the combined data to a file
    with open(f'{volatility}_data.json', 'w') as f:
        json.dump(combined_data, f)

# Convert datetime to Unix timestamp
end_time = int(datetime.now(timezone.utc).timestamp())
start_time = int((datetime.now(timezone.utc) - timedelta(hours=0.02)).timestamp())

for volatility in config['volatilities']:
    fetch_historical_data(volatility, start_time, end_time)
