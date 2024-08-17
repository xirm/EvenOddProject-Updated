import pandas as pd

# Load the preprocessed data
df = pd.read_csv('C:/Users/Administrator/Desktop/EvenOdd/preprocessed_tick_data.csv')

# Display the first few rows
print("First few rows of the preprocessed data:")
print(df.head())

# Display DataFrame information
print("\nDataFrame Info:")
print(df.info())

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe())
