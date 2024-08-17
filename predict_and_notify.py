import pandas as pd
import joblib
import logging
import requests

# Pushover credentials
PUSHOVER_TOKEN = 'ak7q3ixmi7861opmhxheswejsetk58'
PUSHOVER_USER_KEY = 'uuobbyptujidgjvm2qgwsp4jw4dx1z'

# Configure logging
logging.basicConfig(filename='prediction_performance.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the model
model = joblib.load('C:/Users/Administrator/Desktop/EvenOdd/random_forest_model_corrected.pkl')

# Define the feature order and expected features
feature_order = ['tick', 'last_digit', 'tick_diff', 'moving_avg', 'is_even', 'is_odd', 'is_over_5', 'is_under_5']
expected_features = feature_order + ['rolling_avg_5', 'rolling_avg_10', 'volatility_5', 'volatility_10', 'rsi_14',
                                      'bollinger_hband', 'bollinger_lband', 'bollinger_mavg', 'macd', 'macd_signal', 'macd_diff']

# Define file paths for different markets
file_paths = {
    'R_10': 'C:/Users/Administrator/Desktop/EvenOdd/R_10_data_preprocessed.csv',
    'R_25': 'C:/Users/Administrator/Desktop/EvenOdd/R_25_data_preprocessed.csv',
    'R_50': 'C:/Users/Administrator/Desktop/EvenOdd/R_50_data_preprocessed.csv',
    'R_75': 'C:/Users/Administrator/Desktop/EvenOdd/R_75_data_preprocessed.csv',
    'R_100': 'C:/Users/Administrator/Desktop/EvenOdd/R_100_data_preprocessed.csv'
}

# Initialize counters for performance tracking
total_safe_predictions = {'Even': 0, 'Odd': 0}
correct_safe_predictions = {'Even': 0, 'Odd': 0}
incorrect_safe_predictions = {'Even': 0, 'Odd': 0}
total_not_safe_predictions = {'Even': 0, 'Odd': 0}
correct_not_safe_predictions = {'Even': 0, 'Odd': 0}
incorrect_not_safe_predictions = {'Even': 0, 'Odd': 0}

def send_pushover_notification(message):
    data = {
        'token': PUSHOVER_TOKEN,
        'user': PUSHOVER_USER_KEY,
        'message': message
    }
    response = requests.post('https://api.pushover.net/1/messages.json', data=data)
    if response.status_code == 200:
        logging.info("Pushover notification sent successfully.")
    else:
        logging.error("Failed to send Pushover notification.")

# Define the trading rule function
def evaluate_trading_strategy(df, prediction_col, min_safe_range=15, trade_type=None):
    global total_safe_predictions, correct_safe_predictions, incorrect_safe_predictions
    global total_not_safe_predictions, correct_not_safe_predictions, incorrect_not_safe_predictions

    if prediction_col not in df.columns:
        print(f"Error: The column {prediction_col} is missing in the DataFrame.")
        logging.error(f"Column {prediction_col} is missing in the DataFrame.")
        return

    predictions = df[prediction_col].tolist()
    last_digits = df['last_digit'].tolist()

    def generate_message(market, trade_type, safe_range, status):
        return f"Trade {trade_type} {market}. Next {safe_range} ticks are {status}."

    def check_rules(predictions, last_digits, min_safe_range, trade_type):
        global total_safe_predictions, correct_safe_predictions, incorrect_safe_predictions
        global total_not_safe_predictions, correct_not_safe_predictions, incorrect_not_safe_predictions

        for i in range(len(predictions) - min_safe_range):
            safe_range = min_safe_range
            while i + safe_range <= len(predictions):
                window_predictions = predictions[i:i+safe_range]
                window_last_digits = last_digits[i:i+safe_range]

                # Detailed output for the current window
                print(f"Window {i}: Predictions {window_predictions}")
                print(f"Window {i}: Last Digits {window_last_digits}")

                if trade_type == 'Even':
                    safe = check_consecutive(window_last_digits, [1, 3, 5, 7, 9], 2)  # Odd numbers
                elif trade_type == 'Odd':
                    safe = check_consecutive(window_last_digits, [0, 2, 4, 6, 8], 2)  # Even numbers
                else:
                    print("Trade type not recognized.")
                    continue

                status = "safe" if safe else "not safe"
                message = generate_message(market, trade_type, safe_range, status)

                # Print trade notification
                print(message)
                print(f"Trade Type: {trade_type}, Status: {status}, Safe: {safe}")
                logging.info(message)

                if status == "safe":
                    total_safe_predictions[trade_type] += 1
                    if safe:
                        correct_safe_predictions[trade_type] += 1
                    else:
                        incorrect_safe_predictions[trade_type] += 1
                else:
                    total_not_safe_predictions[trade_type] += 1
                    if safe:
                        incorrect_not_safe_predictions[trade_type] += 1
                    else:
                        correct_not_safe_predictions[trade_type] += 1

                if safe:
                    send_pushover_notification(message)
                    safe_range += 5  # Increase range by 5 ticks, adjust as needed
                else:
                    send_pushover_notification(f"Exit {trade_type} {market}. Unsafe conditions within next {safe_range} ticks.")
                    break

    if trade_type:
        check_rules(predictions, last_digits, min_safe_range, trade_type)
    else:
        print("Trade type not specified.")

def check_consecutive(sequence, values, max_consecutive):
    count = 0
    values = set(values)  # Allow for multiple values
    for v in sequence:
        if v in values:
            count += 1
            if count > max_consecutive:
                return False
        else:
            count = 0
    return True

def evaluate_and_notify(file_path, market):
    global total_safe_predictions, correct_safe_predictions, incorrect_safe_predictions
    global total_not_safe_predictions, correct_not_safe_predictions, incorrect_not_safe_predictions

    df = pd.read_csv(file_path)

    print(f"Columns in DataFrame for {file_path}: {df.columns.tolist()}")

    for feature in expected_features:
        if feature not in df.columns:
            df[feature] = 0

    df = df[expected_features]

    print(f"Columns in DataFrame (ordered) for {file_path}: {df.columns.tolist()}")
    print(f"Feature order used for prediction: {expected_features}")

    try:
        df['prediction'] = model.predict(df)
        print(df[['last_digit', 'prediction']].head(15))
        
        logging.info(f"Predictions made for {file_path} successfully.")
        logging.info(f"Sample predictions:\n{df[['last_digit', 'prediction']].head(15)}")
    except ValueError as e:
        logging.error(f"Error during prediction for {file_path}: {e}")
        print(f"Error during prediction for {file_path}: {e}")

    for trade_type in ['Even', 'Odd']:
        evaluate_trading_strategy(df, 'prediction', min_safe_range=20, trade_type=trade_type)

for market, file_path in file_paths.items():
    print(f"\nEvaluating {market} for file {file_path}")
    logging.info(f"Evaluating {market} for file {file_path}")
    evaluate_and_notify(file_path, market) 

percentages = {trade_type: (correct_safe_predictions[trade_type] / total_safe_predictions[trade_type] * 100) 
               if total_safe_predictions[trade_type] > 0 else 0
               for trade_type in total_safe_predictions}

sorted_trade_types = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

logging.info(f"\nSummary of safe to trade predictions:")
for trade_type in ['Even', 'Odd']:
    logging.info(f"{trade_type}: {total_safe_predictions[trade_type]} total, {correct_safe_predictions[trade_type]} correct, {incorrect_safe_predictions[trade_type]} incorrect, Accuracy: {percentages[trade_type]:.2f}%")
    logging.info(f"{trade_type}: {total_not_safe_predictions[trade_type]} total not safe, {correct_not_safe_predictions[trade_type]} correct not safe, {incorrect_not_safe_predictions[trade_type]} incorrect not safe")

print(f"\nSummary of safe to trade predictions:")
for trade_type in ['Even', 'Odd']:
    print(f"{trade_type}: {total_safe_predictions[trade_type]} total, {correct_safe_predictions[trade_type]} correct, {incorrect_safe_predictions[trade_type]} incorrect, Accuracy: {percentages[trade_type]:.2f}%")
    print(f"{trade_type}: {total_not_safe_predictions[trade_type]} total not safe, {correct_not_safe_predictions[trade_type]} correct not safe, {incorrect_not_safe_predictions[trade_type]} incorrect not safe")
