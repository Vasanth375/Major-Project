# # import pandas as pd
# # import joblib

# # # Load the pre-trained model
# # joblib_file = "pretrained_dt_model_stress.pkl"
# # dt_model_loaded = joblib.load(joblib_file)

# # print("Model loaded successfully")

# # # Function to determine stress level based on rules
# # def determine_stress_rules(row):
# #     if row['heart_rate'] > 85 or row['steps'] < 5000 or row['sleep_hours'] < 6:
# #         return 'High'
# #     elif (row['heart_rate'] > 70 and row['heart_rate'] <= 85) or (row['steps'] >= 5000 and row['steps'] < 10000) or (row['sleep_hours'] >= 6 and row['sleep_hours'] < 7):
# #         return 'Medium'
# #     else:
# #         return 'Low'

# # # New data with heart rate, steps, calories, and hours of sleep
# # new_data = pd.DataFrame({
# #     'heart_rate': [94, 97, 53, 53, 71],
# #     'steps': [13522, 9500, 10819, 6485, 6289],
# #     'sleep_hours': [3.88, 7.6, 7.7, 6.4, 8.24],
# # })

# # # Apply rules-based stress level determination
# # new_data['stress_level_rules'] = new_data.apply(determine_stress_rules, axis=1)

# # # Define stress level categories
# # stress_levels = ["Low", "Medium", "High"]

# # # Make predictions on the new data using the model
# # predicted_stress = dt_model_loaded.predict(new_data[['heart_rate', 'steps', 'sleep_hours']])
# # predicted_probabilities = dt_model_loaded.predict_proba(new_data[['heart_rate', 'steps', 'sleep_hours']])

# # # Display the predictions
# # for i, prediction in enumerate(predicted_stress):
# #     # Get the predicted class probabilities from the model
# #     probabilities = predicted_probabilities[i]
    
# #     # Find the index of the maximum probability
# #     predicted_class_index = probabilities.argmax()
    
# #     # Display the predicted stress level from the model and rules-based determination
# #     predicted_stress_level = stress_levels[predicted_class_index]
# #     confidence = probabilities[predicted_class_index] * 100
    
# #     # Retrieve the stress level determined by rules
# #     rules_stress_level = new_data['stress_level_rules'][i]
    
# #     print(f"Data {i+1}: Predicted by Model: {predicted_stress_level} Stress ({confidence:.2f}% confidence)")
# #     print(f"           Determined by Rules: {rules_stress_level}")











# import pandas as pd
# import joblib

# # Load the pre-trained model
# joblib_file = "pretrained_dt_model_stress.pkl"
# dt_model_loaded = joblib.load(joblib_file)

# print("Model loaded successfully")

# # Function to determine stress level based on rules
# def determine_stress_rules(row):
#     if row['heart_rate'] > 85 or row['steps'] < 5000 or row['sleep_hours'] < 6:
#         return 'High'
#     elif (row['heart_rate'] > 70 and row['heart_rate'] <= 85) or (row['steps'] >= 5000 and row['steps'] < 10000) or (row['sleep_hours'] >= 6 and row['sleep_hours'] < 7):
#         return 'Medium'
#     else:
#         return 'Low'

# # New data with heart rate, steps, and hours of sleep
# new_data = pd.DataFrame({
#     'heart_rate': [94, 97, 53, 53, 71],
#     'steps': [13522, 9500, 10819, 6485, 6289],
#     'sleep_hours': [3.88, 7.6, 7.7, 6.4, 8.24],
# })

# # Apply rules-based stress level determination
# new_data['stress_level_rules'] = new_data.apply(determine_stress_rules, axis=1)

# # Define stress level categories
# stress_levels = ["Low", "Medium", "High"]

# # Make predictions on the new data using the model
# predicted_stress = dt_model_loaded.predict(new_data[['heart_rate', 'steps', 'sleep_hours']])
# predicted_probabilities = dt_model_loaded.predict_proba(new_data[['heart_rate', 'steps', 'sleep_hours']])

# # Display the predictions and accuracy
# correct_predictions = 0
# total_samples = len(new_data)

# for i, prediction in enumerate(predicted_stress):
#     # Get the predicted class probabilities from the model
#     probabilities = predicted_probabilities[i]
    
#     # Find the index of the maximum probability
#     predicted_class_index = probabilities.argmax()
    
#     # Display the predicted stress level from the model and rules-based determination
#     predicted_stress_level = stress_levels[predicted_class_index]
#     confidence = probabilities[predicted_class_index] * 100
    
#     # Retrieve the stress level determined by rules
#     rules_stress_level = new_data['stress_level_rules'][i]
    
#     print(f"Data {i+1}: Predicted by Model: {predicted_stress_level} Stress ({confidence:.2f}% confidence)")
#     print(f"           Determined by Rules: {rules_stress_level}")
    
#     # Check accuracy
#     if predicted_stress_level == rules_stress_level:
#         correct_predictions += 1

# # Calculate accuracy
# accuracy = (correct_predictions / total_samples) * 100
# print(f"\nAccuracy: {accuracy:.2f}%")












# import pandas as pd
# import joblib

# # Load the pre-trained model
# joblib_file = "pretrained_dt_model_stress.pkl"
# dt_model_loaded = joblib.load(joblib_file)

# print("Model loaded successfully")

# # Function to determine stress level based on rules
# def determine_stress_rules(row):
#     if row['heart_rate'] > 85 or row['steps'] < 5000 or row['sleep_hours'] < 6:
#         return 'High'
#     elif (row['heart_rate'] > 70 and row['heart_rate'] <= 85) or (row['steps'] >= 5000 and row['steps'] < 10000) or (row['sleep_hours'] >= 6 and row['sleep_hours'] < 7):
#         return 'Medium'
#     else:
#         return 'Low'

# # New data with heart rate, steps, and hours of sleep
# new_data = pd.DataFrame({
#     'heart_rate': [94, 97, 53, 53, 71],
#     'steps': [13522, 9500, 10819, 6485, 6289],
#     'sleep_hours': [3.88, 7.6, 7.7, 6.4, 8.24],
# })

# # Apply rules-based stress level determination
# new_data['stress_level_rules'] = new_data.apply(determine_stress_rules, axis=1)

# # Define stress level categories
# stress_levels = ["Low", "Medium", "High"]

# # Make predictions on the new data using the model
# predicted_stress = dt_model_loaded.predict(new_data[['heart_rate', 'steps', 'sleep_hours']])
# predicted_probabilities = dt_model_loaded.predict_proba(new_data[['heart_rate', 'steps', 'sleep_hours']])

# # Display the predictions and accuracy
# correct_predictions = 0
# total_samples = len(new_data)

# for i, prediction in enumerate(predicted_stress):
#     # Get the predicted class probabilities from the model
#     probabilities = predicted_probabilities[i]
    
#     # Find the index of the maximum probability
#     predicted_class_index = probabilities.argmax()
    
#     # Display the predicted stress level from the model and rules-based determination
#     predicted_stress_level = stress_levels[predicted_class_index]
#     confidence = probabilities[predicted_class_index] * 100
    
#     # Retrieve the stress level determined by rules
#     rules_stress_level = new_data['stress_level_rules'][i]
    
#     print(f"Data {i+1}: Predicted by Model: {predicted_stress_level} Stress ({confidence:.2f}% confidence)")
#     print(f"           Determined by Rules: {rules_stress_level}")
    
#     # Check accuracy
#     if predicted_stress_level == rules_stress_level:
#         correct_predictions += 1

# # Calculate accuracy
# accuracy = (correct_predictions / total_samples) * 100
# print(f"\nAccuracy: {accuracy:.2f}%")























import pandas as pd
import joblib

# Load the pre-trained model
joblib_file = "pretrained_dt_model_stress.pkl"
dt_model_loaded = joblib.load(joblib_file)

print("Model loaded successfully")

# Function to determine stress level based on rules
def determine_stress_rules(row):
    if row['heart_rate'] > 85 or row['steps'] < 5000 or row['sleep_hours'] < 6:
        return 'High'
    elif (row['heart_rate'] > 70 and row['heart_rate'] <= 85) or (row['steps'] >= 5000 and row['steps'] < 10000) or (row['sleep_hours'] >= 6 and row['sleep_hours'] < 7):
        return 'Medium'
    else:
        return 'Low'

# New data with heart rate, steps, and hours of sleep
new_data = pd.DataFrame({
    'heart_rate': [94, 97, 53, 53, 71],
    'steps': [13522, 9500, 10819, 6485, 6289],
    'sleep_hours': [3.88, 7.6, 7.7, 6.4, 8.24],
})

# Apply rules-based stress level determination
new_data['stress_level_rules'] = new_data.apply(determine_stress_rules, axis=1)

# Define stress level categories
stress_levels = ["Low", "Medium", "High"]

# Make predictions on the new data using the model
predicted_stress = dt_model_loaded.predict(new_data[['heart_rate', 'steps', 'sleep_hours']])
predicted_probabilities = dt_model_loaded.predict_proba(new_data[['heart_rate', 'steps', 'sleep_hours']])

# Display the results of rules-based stress level determination
print("Results of Rules-Based Stress Level Determination:")
for i in range(len(new_data)):
    rules_stress_level = new_data['stress_level_rules'][i]
    print(f"Data {i+1}: Determined Stress Level - {rules_stress_level}")

# Calculate accuracy of rules-based determination
correct_predictions = sum(new_data['stress_level_rules'][i] == predicted_stress[i] for i in range(len(new_data)))
accuracy = (correct_predictions / len(new_data)) * 100

print(f"\nAccuracy of Rules-Based Determination: {accuracy:.2f}%")
