import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the preprocessed data
df = pd.read_csv('C:/Users/Administrator/Desktop/EvenOdd/preprocessed_tick_data.csv')

# Example of feature engineering: adding lagged features
df['last_digit_lag1'] = df['last_digit'].shift(1)
df['last_digit_lag2'] = df['last_digit'].shift(2)

# Drop rows with NaN values caused by shifting
df = df.dropna()

# Encode categorical variables
label_encoder = LabelEncoder()
df['volatility'] = label_encoder.fit_transform(df['volatility'])
df['trend'] = label_encoder.fit_transform(df['trend'])

# Feature scaling
scaler = StandardScaler()
features = ['tick', 'last_digit', 'volatility', 'trend', 'volatility_measure', 'last_digit_lag1', 'last_digit_lag2']
df[features] = scaler.fit_transform(df[features])

# Save the engineered features to a new CSV
df.to_csv('C:/Users/Administrator/Desktop/EvenOdd/engineered_features.csv', index=False)

print("Feature engineering complete. Data saved to: C:/Users/Administrator/Desktop/EvenOdd/engineered_features.csv")
