import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Sample dataset with features: [heart rate, steps, calories, sleeping hours]
# Label: 1 = Stressed, 0 = Not Stressed
data = [
    {"features": [78, 1000, 2000, 8], "label": 0},
    {"features": [96, 8000, 2500, 5], "label": 1},
    {"features": [85, 8500, 2200, 6.5], "label": 1},
    {"features": [105, 12500, 2500, 5.5], "label": 1},
    {"features": [80, 1200, 1950, 8.2], "label": 0},
    {"features": [100, 7000, 2600, 4.5], "label": 1},
    {"features": [87, 9000, 2150, 7], "label": 1},
    {"features": [110, 6500, 2800, 3.8], "label": 0},
    {"features": [78, 4000, 1800, 9], "label": 0},
    {"features": [115, 6000, 2900, 4], "label": 1},
]

# Convert dataset to arrays for easier manipulation
X = np.array([entry["features"] for entry in data])
y = np.array([entry["label"] for entry in data])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Initialize and train the Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set and calculate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred) * 100

# Visualize the accuracy with matplotlib
# X-axis represents feature names, and Y-axis shows some accuracy values for demonstration
feature_names = ["Heart Rate", "Steps", "Calories", "Sleep Hours"]
accuracy_values = [accuracy] * len(feature_names)  # Set the accuracy as the value for each feature

plt.figure(figsize=(8, 5))
plt.plot(feature_names, accuracy_values, marker='o', linestyle='-', color='b', label=f"Accuracy {accuracy} %")
plt.xlabel("Features")
plt.ylabel("Accuracy (%)")
plt.title("Random Forest Model Accuracy by Feature")
plt.legend()
plt.grid()
plt.show()

print(f"Model Accuracy: {accuracy:.2f}%")
