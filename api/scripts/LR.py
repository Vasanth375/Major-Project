import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dataset with features: [heart rate, steps, calories, sleeping hours]
# Label: 1 = Stressed, 0 = Not Stressed
data = [
    {"features": [78, 12000, 2000, 8], "label": 0},
    {"features": [96, 8000, 2500, 5], "label": 0},
    {"features": [85, 8500, 2200, 6.5], "label": 0},
    {"features": [105, 7500, 2500, 5.5], "label": 1},
    {"features": [80, 12500, 1950, 8.2], "label": 1},
    {"features": [100, 7000, 2600, 4.5], "label": 1},
    {"features": [87, 9000, 2150, 7], "label": 1},
    {"features": [110, 6500, 2800, 3.8], "label": 1},
    {"features": [78, 14000, 1800, 9], "label": 1},
    {"features": [115, 6000, 2900, 4], "label": 1},
]

# Convert dataset to DataFrame for easier manipulation
X = np.array([entry["features"] for entry in data])
y = np.array([entry["label"] for entry in data])

# Split data into training and testing sets using stratify to balance the classes in test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred) * 100

# Plotting accuracy
plt.figure(figsize=(6, 4))
plt.bar(["Test Accuracy 50%"], [accuracy], color="purple")
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.title("Logistic Regression Model Accuracy on Test Data")
plt.show()

# # Plot Feature Importance (Logistic Regression Coefficients)
# feature_names = ["Heart Rate", "Steps", "Calories", "Sleeping Hours"]
# coef = model.coef_[0]  # Logistic Regression coefficients for each feature

# plt.figure(figsize=(8, 5))
# plt.barh(feature_names, coef, color="teal")
# plt.xlabel("Coefficient Value")
# plt.title("Feature Importance in Stress Prediction")
# plt.show()
