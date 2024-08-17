import matplotlib.pyplot as plt

# Check class distribution
class_counts = y.value_counts()
print("\nClass distribution:")
print(class_counts)

# Plot class distribution
plt.figure(figsize=(10, 6))
class_counts.plot(kind='bar')
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution')
plt.show()
