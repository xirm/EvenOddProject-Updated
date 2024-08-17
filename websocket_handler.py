import websocket
import json
import time
import logging
from config import config

class WebSocketHandler:
    def __init__(self):
        self.url = config['websocket_url']
        self.api_key = config['api_key']
        self.volatilities = config['volatilities']
        self.ws = None

    def on_message(self, ws, message):
        data = json.loads(message)
        logging.info(f"Received message: {data}")
        # Handle real-time tick data here

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning("WebSocket closed, attempting to reconnect...")
        self.reconnect()

    def on_open(self, ws):
        logging.info("WebSocket connection established.")
        self.subscribe_to_ticks()

    def subscribe_to_ticks(self):
        for volatility in self.volatilities:
            subscription_request = {
                "ticks": volatility,
                "subscribe": 1
            }
            self.ws.send(json.dumps(subscription_request))

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def reconnect(self):
        time.sleep(5)
        logging.info("Reconnecting to WebSocket...")
        self.connect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    handler = WebSocketHandler()
    handler.connect()
