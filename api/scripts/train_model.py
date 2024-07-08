import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Use an absolute path
data_path = os.path.abspath('../main/data/fitness_data.csv')
print(f"Looking for data at: {data_path}")

# Load the dataset
data = pd.read_csv(data_path)

# Define the expected columns
expected_columns = ['age', 'gender', 'height', 'weight', 'Fitbit.Steps_LE', 'Fitbit.Heart_LE', 
                    'Fitbit.Calories_LE', 'Fitbit.Distance_LE', 'EntropyFitbitHeartPerDay_LE', 
                    'EntropyFitbitStepsPerDay_LE', 'RestingFitbitHeartrate_LE', 
                    'CorrelationFitbitHeartrateSteps_LE', 'NormalizedFitbitHeartrate_LE', 
                    'FitbitIntensity_LE', 'SDNormalizedFitbitHR_LE', 'FitbitStepsXDistance_LE']

# Check which columns are actually in the data
available_columns = [col for col in expected_columns if col in data.columns]

# Features and target variable
X = data[available_columns]
y = data['activity_trimmed']  # Assuming 'activity_trimmed' is the target variable (or stress level)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model using Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
model_path = os.path.abspath('../main/models/stress_model.pkl')
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

print(f"Random Forest Model training completed and saved as {model_path}")
