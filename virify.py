import pandas as pd
import joblib

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Load the new data
data_file = 'preprocessed_tick_data.csv'  # Adjust if needed

try:
    data = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"File not found: {data_file}")
    exit(1)

# Print available columns for debugging
print("Columns in new data:", data.columns)

# Select the features used during training
required_features = ['tick', 'tick_diff', 'moving_avg']
missing_features = [feature for feature in required_features if feature not in data.columns]

if missing_features:
    raise KeyError(f"Missing features: {', '.join(missing_features)}")

# Prepare data for prediction
X_new = data[required_features]

# Make predictions
predictions = model.predict(X_new)

# Output predictions
print(predictions)
