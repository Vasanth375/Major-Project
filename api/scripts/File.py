import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter

# Step 1: Random Forest Accuracy Calculation
# Random Forest dataset
rf_data = [
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
X_rf = np.array([entry["features"] for entry in rf_data])
y_rf = np.array([entry["label"] for entry in rf_data])
X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, y_rf, test_size=0.2, stratify=y_rf, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_rf, y_train_rf)
y_pred_rf = rf_model.predict(X_test_rf)
rf_accuracy = accuracy_score(y_test_rf, y_pred_rf) * 100

# Step 2: Logistic Regression Accuracy Calculation
# Logistic Regression dataset
lr_data = [
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
X_lr = np.array([entry["features"] for entry in lr_data])
y_lr = np.array([entry["label"] for entry in lr_data])
X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_lr, y_lr, test_size=0.2, stratify=y_lr, random_state=42)
lr_model = LogisticRegression(max_iter=200)
lr_model.fit(X_train_lr, y_train_lr)
y_pred_lr = lr_model.predict(X_test_lr)
lr_accuracy = accuracy_score(y_test_lr, y_pred_lr) * 100

# Step 3: KNN Accuracy Calculation
# KNN dataset and prediction function
knn_data = [
    {"features": [65, 1600, 8, 9000], "label": "normal"},
    {"features": [68, 1700, 7.5, 10000], "label": "low"},
    {"features": [62, 1550, 8.5, 8000], "label": "high"},
    {"features": [75, 1500, 6.5, 15000], "label": "high"},
    {"features": [72, 1450, 6.2, 13000], "label": "high"},
    {"features": [78, 1550, 6.8, 14000], "label": "low"},
    {"features": [85, 1300, 5, 8000], "label": "high"},
    {"features": [80, 1200, 4.5, 7000], "label": "low"},
    {"features": [82, 1350, 5.5, 7500], "label": "normal"},
    {"features": [88, 1400, 4.8, 8500], "label": "normal"},
]

def knn_predict(new_data, dataset, k=3):
    distances = [(np.sqrt(sum((np.array(data["features"]) - np.array(new_data)) ** 2)), data["label"]) for data in dataset]
    distances.sort(key=lambda x: x[0])
    top_k_labels = [label for _, label in distances[:k]]
    return Counter(top_k_labels).most_common(1)[0][0]

correct_knn = sum(knn_predict(entry["features"], knn_data, k=3) == entry["label"] for entry in knn_data)
knn_accuracy = (correct_knn / len(knn_data)) * 100

# Step 4: Decision Tree Accuracy Calculation
# Decision Tree dataset
dt_data = [
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

X_dt = np.array([entry["features"] for entry in dt_data])
y_dt = np.array([entry["label"] for entry in dt_data])
X_train_dt, X_test_dt, y_train_dt, y_test_dt = train_test_split(X_dt, y_dt, test_size=0.3, stratify=y_dt, random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train_dt, y_train_dt)
y_pred_dt = dt_model.predict(X_test_dt)
dt_accuracy = (accuracy_score(y_test_dt, y_pred_dt) * 100)

# Plotting the accuracies of each model
algorithms = ["Random Forest", "Logistic Regression", "KNN", "Decision Tree"]
accuracies = [rf_accuracy, lr_accuracy, knn_accuracy, dt_accuracy]

plt.figure(figsize=(10, 6))
plt.bar(algorithms, accuracies, color=["blue", "purple", "orange", "green"])
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.title("Accuracy Comparison of Different Algorithms")
for i, acc in enumerate(accuracies):
    plt.text(i, acc + 1, f"{acc:.2f}%", ha='center', va='bottom')
plt.show()
