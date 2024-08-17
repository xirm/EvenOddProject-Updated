import pandas as pd

# Load the CSV file
file_path = 'C:/Users/Administrator/Desktop/EvenOdd/tick_data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataframe
print("First few rows of the CSV file:")
print(data.head())

# Display basic information about the dataframe
print("\nDataFrame Info:")
print(data.info())

# Display summary statistics
print("\nSummary Statistics:")
print(data.describe(include='all'))
