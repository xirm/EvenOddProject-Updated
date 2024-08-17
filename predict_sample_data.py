import pandas as pd
import joblib

# Load the model
model = joblib.load('C:\\Users\\Administrator\\Desktop\\EvenOdd\\random_forest_model.pkl')

# Sample data
sample_data = pd.DataFrame({
    'tick': [10, 20],
    'tick_diff': [2, 3],
    'moving_avg': [15, 25]
})

# Predict
sample_predictions = model.predict(sample_data)

# Print predictions
print("Sample Predictions:", sample_predictions)
