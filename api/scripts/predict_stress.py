import pandas as pd
import joblib

# Load the pre-trained model
joblib_file = "pretrained_dt_model_stress.pkl"
dt_model_loaded = joblib.load(joblib_file)

print("Model loaded successfully")

# New data with only heart rate, steps, and hours of sleep
new_data = pd.DataFrame({
    'calories': [2000, 2500],  # Example values
    'heart_rate': [70, 90],    # Example values
    'steps': [5000, 7000],     # Example values
    'sleep_hours': [6, 5]      # Example values
})

# Make predictions on the new data
predicted_stress = dt_model_loaded.predict(new_data)
predicted_probabilities = dt_model_loaded.predict_proba(new_data)

# Display the predictions
for i, prediction in enumerate(predicted_stress):
    print(f"Data {i+1}: {'Stressed' if prediction == 1 else 'Not Stressed'} ({predicted_probabilities[i][1]*100:.2f}% confidence)")
