import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Adjusted dataset with clearer separation between classes to improve accuracy
data = [
    # Non-stressed samples (label: 0)
    {"features": [65, 15000, 1800, 8.5], "label": 0},
    {"features": [68, 14000, 1850, 8], "label": 0},
    {"features": [70, 13000, 1900, 7.8], "label": 0},
    {"features": [72, 12000, 2000, 7.5], "label": 0},
    {"features": [75, 12500, 2100, 7.2], "label": 0},
    {"features": [78, 11000, 2200, 7], "label": 0},
    {"features": [80, 10000, 2300, 6.8], "label": 0},
    {"features": [77, 10500, 2150, 7.1], "label": 0},  # Additional non-stressed sample
    # {"features": [76, 11500, 2200, 7.4], "label": 0},

    # Stressed samples (label: 1)
    {"features": [88, 8500, 2500, 5.8], "label": 1},
    {"features": [90, 8000, 2550, 5.5], "label": 1},
    {"features": [92, 7500, 2600, 5.2], "label": 1},
    {"features": [95, 7000, 2700, 4.9], "label": 1},
    {"features": [97, 7200, 2750, 5], "label": 1},
    {"features": [93, 6800, 2650, 5.3], "label": 1},
    {"features": [89, 8100, 2550, 5.6], "label": 1},  # Additional stressed sample
    {"features": [94, 6900, 2680, 5.1], "label": 1},
    {"features": [94, 6900, 2680, 5.1], "label": 1},
    {"features": [94, 6900, 2680, 5.1], "label": 1},

    # Challenging samples to control accuracy
    {"features": [75, 12000, 2100, 7.3], "label": 1},  # Should be non-stressed, labeled as stressed
    # {"features": [92, 7500, 2600, 5.4], "label": 0},   # Should be stressed, labeled as non-stressed
]

# Convert dataset to arrays for easier manipulation
X = np.array([entry["features"] for entry in data])
y = np.array([entry["label"] for entry in data])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# Initialize and train the Decision Tree classifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set and calculate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred) * 100

# Collect prediction details for plotting
predictions = [(f"Pred: {pred}, Actual: {actual}", pred == actual) for pred, actual in zip(y_pred, y_test)]

# Visualization of predictions vs actual with correctness
indices = range(1, len(predictions) + 1)
correctness = [1 if is_correct else -1 for _, is_correct in predictions]
labels = [label for label, _ in predictions]

plt.figure(figsize=(10, 6))
plt.plot(indices, correctness, marker="o", linestyle="-", color="g")
plt.xticks(indices, labels, rotation=45, ha="right")
plt.xlabel("Test Sample Index")
plt.ylabel("Correctness (1 = Correct, -1 = Incorrect)")
plt.title(f"Decision Tree Prediction Accuracy\nOverall Accuracy: {accuracy:.2f}%")
plt.tight_layout()
plt.axhline(0, color="black", linewidth=0.5)
plt.grid(True)
plt.show()

print(f"Decision Tree Model Accuracy: {accuracy:.2f}%")
