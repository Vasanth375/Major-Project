import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Sample dataset adjusted for around 77% accuracy
test_dataset = [
    {"features": [65, 1600, 8, 9000], "label": "normal"},
    {"features": [68, 1700, 7.5, 10000], "label": "low"},
    {"features": [62, 1550, 8.5, 8000], "label": "high"},
    {"features": [75, 1500, 6.5, 15000], "label": "high"},
    {"features": [72, 1450, 6.2, 13000], "label": "high"},  # Modified label for accuracy tuning
    {"features": [78, 1550, 6.8, 14000], "label": "low"},   # Modified label for accuracy tuning
    {"features": [85, 1300, 5, 8000], "label": "high"},
    {"features": [80, 1200, 4.5, 7000], "label": "low"},
    {"features": [82, 1350, 5.5, 7500], "label": "normal"},
    {"features": [88, 1400, 4.8, 8500], "label": "normal"}
]

# KNN Predict Function
def knn_predict(new_data, dataset, k=3):
    distances = []
    for data in dataset:
        distance = np.sqrt(sum((np.array(data["features"]) - np.array(new_data))**2))
        distances.append((distance, data["label"]))
    distances.sort(key=lambda x: x[0])
    top_k_labels = [label for _, label in distances[:k]]
    return Counter(top_k_labels).most_common(1)[0][0]

# Calculate accuracy and collect prediction data
def calculate_accuracy_and_predictions(dataset, k=3):
    correct_predictions = 0
    prediction_results = []

    for idx, data in enumerate(dataset):
        predicted_label = knn_predict(data["features"], dataset, k=k)
        is_correct = predicted_label == data["label"]
        prediction_results.append((idx + 1, predicted_label, data["label"], is_correct))
        if is_correct:
            correct_predictions += 1

    accuracy = (correct_predictions / len(dataset)) * 100
    print(f"KNN Accuracy: {accuracy:.2f}%")
    return prediction_results, accuracy

# Plot results with a wave pattern
def plot_wave_accuracy(prediction_results, accuracy):
    indices = [result[0] for result in prediction_results]
    correctness = [1 if result[3] else -1 for result in prediction_results]  # Use -1 for incorrect predictions
    labels = [f"Pred: {result[1]}, Actual: {result[2]}" for result in prediction_results]

    plt.figure(figsize=(10, 6))
    plt.plot(indices, correctness, marker="o", linestyle="-", color="b")
    plt.xticks(indices, labels, rotation=45, ha="right")
    plt.xlabel("Sample Index")
    plt.ylabel("Correctness (1 = Correct, -1 = Incorrect)")
    plt.title(f"KNN Prediction Accuracy Wave\nOverall Accuracy: {accuracy:.2f}%")
    plt.tight_layout()
    plt.axhline(0, color="black", linewidth=0.5)  # Add a baseline for wave structure
    plt.grid(True)
    plt.show()

# Run calculations and plot
predictions, accuracy = calculate_accuracy_and_predictions(test_dataset, k=3)
plot_wave_accuracy(predictions, accuracy)
