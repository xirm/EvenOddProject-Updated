import pandas as pd
import numpy as np
import joblib
import logging
import requests
from sklearn.preprocessing import StandardScaler
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the pre-trained model
model = joblib.load('random_forest_model.pkl')

# Define file paths
state_file = 'notification_state.txt'

# Function to read notification state
def read_notification_state():
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            state = file.read().strip()
            return state
    return 'None'

# Function to write notification state
def write_notification_state(state):
    with open(state_file, 'w') as file:
        file.write(state)

# Load historical data for prediction
data = pd.read_csv('preprocessed_tick_data.csv')

# Define target column
target_column = 'last_digit'

# Preprocess the data
X = data.drop(columns=[target_column, 'timestamp'])  # Adjust if necessary
y = data[target_column]

# Fit the scaler on the existing data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Load new tick data for prediction
new_data = pd.read_csv('preprocessed_tick_data.csv')  # Ensure this is the latest data

# Prepare the new data for prediction
X_new = new_data.drop(columns=[target_column, 'timestamp'])  # Adjust if necessary
X_new_scaled = scaler.transform(X_new)  # Scale new data

# Make predictions
y_pred = model.predict(X_new_scaled)

# Calculate percentages for "Over 4" and "Under 6"
over_4_percent = np.mean(y_pred >= 5)  # For "Over 4"
under_6_percent = np.mean(y_pred <= 5)  # For "Under 6"

# Get most and least appearing digits in the last 120 ticks
last_120_ticks = y.tail(120)
most_appearing = last_120_ticks.mode()[0]
least_appearing = last_120_ticks.value_counts().idxmin()

# Notification state
notification_state = read_notification_state()

# Notify if predictions meet certain criteria
if over_4_percent > 0.8:
    def send_pushover_notification(user_key, token, message):
        url = "https://api.pushover.net/1/messages.json"
        payload = {
            "token": token,
            "user": user_key,
            "message": message
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")

    # Send notification for Over 4
    send_pushover_notification(
        'uuobbyptujidgjvm2qgwsp4jw4dx1z',
        'ak7q3ixmi7861opmhxheswejsetk58',
        f"Trade Over 4: R_100. {over_4_percent*100:.2f}%. L {least_appearing}/M {most_appearing}."
    )

    # Update notification state
    write_notification_state('Over_4')

if under_6_percent > 0.8:
    # Send notification for Under 6
    send_pushover_notification(
        'uuobbyptujidgjvm2qgwsp4jw4dx1z',
        'ak7q3ixmi7861opmhxheswejsetk58',
        f"Trade Under 6: R_10. {under_6_percent*100:.2f}%. L {least_appearing}/M {most_appearing}."
    )

    # Update notification state
    write_notification_state('Under_6')

# Handle exit notifications
if notification_state == 'Over_4' and over_4_percent < 0.8:
    # Send exit notification for Over 4
    send_pushover_notification(
        'uuobbyptujidgjvm2qgwsp4jw4dx1z',
        'ak7q3ixmi7861opmhxheswejsetk58',
        f"Exit Trade Over 4: R_100. {over_4_percent*100:.2f}%. L {least_appearing}/M {most_appearing}."
    )
    # Reset state
    write_notification_state('None')

if notification_state == 'Under_6' and under_6_percent < 0.8:
    # Send exit notification for Under 6
    send_pushover_notification(
        'uuobbyptujidgjvm2qgwsp4jw4dx1z',
        'ak7q3ixmi7861opmhxheswejsetk58',
        f"Exit Trade Under 6: R_10. {under_6_percent*100:.2f}%. L {least_appearing}/M {most_appearing}."
    )
    # Reset state
    write_notification_state('None')

# Log prediction results
logging.info(f"R_10: Over 4: {over_4_percent*100:.2f}% – Under 6: {under_6_percent*100:.2f}% [L {least_appearing}/ M {most_appearing}] Last Digit: {y_pred[-1]}")
