import pandas as pd

# Load the dataset
data = pd.read_csv("./stress_data.csv")

# Function to determine stress level
def determine_stress(row):
    if (row['heart_rate'] > 90 or row['steps'] < 3000 or row['sleep_hours'] < 5):
        return 'high'
    elif (row['heart_rate'] > 75 or row['steps'] < 7000 or row['sleep_hours'] < 7):
        return 'normal'
    else:
        return 'low'

# Apply the function to the dataset
data['stress_level'] = data.apply(determine_stress, axis=1)

# Save the new dataset with stress levels
data.to_csv('stress_data.csv', index=False)
print("Synthetic dataset with stress levels created and saved as 'synthetic_stress_data_with_levels.csv'.")
