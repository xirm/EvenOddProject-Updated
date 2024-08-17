import logging
import requests

def send_notification(message):
    try:
        # Use the provided Pushover token and user key
        token = "ak7q3ixmi7861opmhxheswejsetk58"
        user = "uuobbyptujidgjvm2qgwsp4jw4dx1z"

        if token and user:
            response = requests.post("https://api.pushover.net/1/messages.json", data={
                "token": token,
                "user": user,
                "message": message
            })

            if response.status_code == 200:
                logging.info(f"Notification sent successfully: {message}")
            else:
                logging.error(f"Failed to send notification. Status code: {response.status_code}")
        else:
            logging.error("Pushover token or user not provided")

    except Exception as e:
        logging.error(f"Exception while sending notification: {e}")
