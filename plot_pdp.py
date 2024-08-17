from sklearn.inspection import partial_dependence
import matplotlib.pyplot as plt
import joblib
import pandas as pd

# Load the model and training data
model = joblib.load('C:/Users/Administrator/Desktop/EvenOdd/random_forest_model.pkl')
df = pd.read_csv('C:/Users/Administrator/Desktop/EvenOdd/engineered_features_updated.csv')

# Define features used in training
features = ['tick', 'tick_diff', 'moving_avg']

# Plot partial dependence
fig, ax = plt.subplots(figsize=(10, 6))
for feature in features:
    pdp = partial_dependence(model, df[features], features=[feature], kind='average')
    ax.plot(pdp['values'][0], pdp['average'][0], label=feature)

ax.set_xlabel('Feature Value')
ax.set_ylabel('Partial Dependence')
ax.legend()
plt.title('Partial Dependence Plots')
plt.show()
