import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load the engineered features data
df = pd.read_csv('C:/Users/Administrator/Desktop/EvenOdd/engineered_features.csv')

# Calculate additional features if they are not already in the DataFrame
if 'tick_diff' not in df.columns:
    df['tick_diff'] = df['tick'].diff()

if 'moving_avg' not in df.columns:
    df['moving_avg'] = df['tick'].rolling(window=5).mean()

# Drop any rows with NaN values that resulted from the diff() and rolling() operations
df.dropna(inplace=True)

# Define the target variable
df['target'] = df['last_digit'].apply(lambda x: 1 if x > 5 else 0)

# Define the new set of features, excluding 'time'
features = ['tick', 'last_digit', 'tick_diff', 'moving_avg']
X = df[features]
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Cross-validation
cross_val_scores = cross_val_score(model, X, y, cv=5)
print("Cross-validation scores:", cross_val_scores)
print("Mean Cross-validation score:", cross_val_scores.mean())
