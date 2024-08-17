import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD

# Load the dataset
df = pd.read_csv('C:/Users/Administrator/Desktop/EvenOdd/engineered_features_updated.csv')

# Feature engineering
df['is_even'] = (df['last_digit'] % 2 == 0).astype(int)
df['is_odd'] = (df['last_digit'] % 2 != 0).astype(int)

# Add trend indicators or volatility metrics
df['rolling_avg_5'] = df['tick'].rolling(window=5).mean()
df['rolling_avg_10'] = df['tick'].rolling(window=10).mean()
df['volatility_5'] = df['tick'].rolling(window=5).std()
df['volatility_10'] = df['tick'].rolling(window=10).std()

# Add RSI (Relative Strength Index)
rsi = RSIIndicator(df['tick'], window=14)
df['rsi_14'] = rsi.rsi()

# Add Bollinger Bands
bollinger = BollingerBands(df['tick'], window=20, window_dev=2)
df['bollinger_hband'] = bollinger.bollinger_hband()
df['bollinger_lband'] = bollinger.bollinger_lband()
df['bollinger_mavg'] = bollinger.bollinger_mavg()

# Add MACD (Moving Average Convergence Divergence)
macd = MACD(df['tick'])
df['macd'] = macd.macd()
df['macd_signal'] = macd.macd_signal()
df['macd_diff'] = macd.macd_diff()

# Handle NaN values
df.dropna(inplace=True)

# Correct target labels
df['last_digit'] = df['last_digit'].round().astype(int).clip(lower=0, upper=9)

# Define features and target
features = ['tick', 'last_digit', 'tick_diff', 'moving_avg', 'is_even', 'is_odd',
            'rolling_avg_5', 'rolling_avg_10', 'volatility_5', 'volatility_10',
            'rsi_14', 'bollinger_hband', 'bollinger_lband', 'bollinger_mavg',
            'macd', 'macd_signal', 'macd_diff']
X = df[features]
y = df['last_digit']

# Filter out only Even and Odd classes
X = X[(y == 0) | (y == 1)]  # Assuming 0 is Even and 1 is Odd
y = y[(y == 0) | (y == 1)]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model and pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Perform grid search to find the best hyperparameters
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [None, 10, 20],
    'classifier__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

# Best model from grid search
best_pipeline = grid_search.best_estimator_

# Evaluate the model
y_pred = best_pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
y_prob = best_pipeline.predict_proba(X_test)[:, 1]  # Probabilities for the positive class
print(f"ROC AUC Score: {roc_auc_score(y_test, y_prob)}")

# Save the trained model
joblib.dump(best_pipeline, 'C:/Users/Administrator/Desktop/EvenOdd/random_forest_model_even_odd.pkl')

# Print feature importances
classifier = best_pipeline.named_steps['classifier']
if hasattr(classifier, 'feature_importances_'):
    feature_importances = classifier.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    print("\nFeature Importances:")
    print(importance_df)
else:
    print("Feature importances are not available for this model.")

# Permutation feature importance
results = permutation_importance(best_pipeline, X_test, y_test, scoring='accuracy')

importance_df = pd.DataFrame({
    'Feature': features,
    'Permutation Importance': results.importances_mean
}).sort_values(by='Permutation Importance', ascending=False)

print("\nPermutation Feature Importances:")
print(importance_df)
