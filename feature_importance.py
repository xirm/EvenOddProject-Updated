import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Load the preprocessed data
data = pd.read_csv('preprocessed_tick_data.csv')

# Define your features (X) and target (y)
X = data.drop(['target_column'], axis=1)  # Replace 'target_column' with your actual target column
y = data['target_column']

# Train your model
model = RandomForestClassifier()  # Replace with your model if different
model.fit(X, y)

# Feature importance
importances = model.feature_importances_
feature_names = X.columns

# Create a DataFrame for feature importances
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(10, 8))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importances')
plt.show()

print(importance_df)
