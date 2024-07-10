import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Number of samples
num_samples = 1000

# Generate synthetic data
data = pd.DataFrame({
    'calories': np.random.randint(1500, 3500, num_samples),
    'heart_rate': np.random.randint(60, 100, num_samples),
    'steps': np.random.randint(1000, 20000, num_samples),
    'sleep_hours': np.random.uniform(4, 10, num_samples)
})

# Save the dataset
data.to_csv('./stress_data.csv', index=False)
print("Synthetic dataset created and saved as 'synthetic_data_without_stress.csv'.")
