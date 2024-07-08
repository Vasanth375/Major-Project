# # predict_stress.py

# import sys
# import json

# def predict_stress(heart_rate, calories, sleep_time):
#     # Define stress levels and corresponding actions
#     stress_levels = {
#         'low': {
#             'action': 'Continue maintaining a healthy routine.',
#         },
#         'normal': {
#             'action': 'Consider adding relaxation techniques like meditation or yoga.',
#         },
#         'high': {
#             'action': 'Focus on reducing stressors and improving sleep quality.',
#         }
#     }

#     # Determine stress level based on average values
#     if heart_rate < 70 and calories > 1500 and sleep_time > 7:
#         stress_level = 'low'
#     elif heart_rate > 80 or calories < 1400 or sleep_time < 6:
#         stress_level = 'high'
#     else:
#         stress_level = 'normal'

#     return stress_level, stress_levels[stress_level]['action']



# if __name__ == "__main__":
#     # Read input from stdin (expected JSON format)
#     input_data = json.loads(sys.stdin.read())

#     # Extract average values from input
#     weekly_data = input_data.get('weeklyData', [])
    
#     # Calculate average values
#     avg_heart_rate = sum(day['Heart'] for day in weekly_data) / len(weekly_data)
#     avg_calories = sum(day['Calories'] for day in weekly_data) / len(weekly_data)
#     avg_sleep_time = sum(day['Sleep'] for day in weekly_data) / len(weekly_data)  # Sleep time provided in hours

#     # Predict stress level and action to reduce stress
#     predicted_stress, action = predict_stress(avg_heart_rate, avg_calories, avg_sleep_time)

#     # Output prediction and action suggestion as JSON
#     print(json.dumps({'predictedStress': predicted_stress, 'action': action}))

from sklearn.tree import DecisionTreeClassifier
import random
import sys
import json

# Define stress levels and corresponding actions
stress_levels = {
    'low': {
        'action': 'Continue maintaining a healthy routine.'
    },
    'normal': {
        'action': 'Consider adding relaxation techniques like meditation or yoga.'
    },
    'high': {
        'action': 'Focus on reducing stressors and improving sleep quality.'
    }
}

# Training data with ranges for demonstration
X = [
    # Low stress
    [65, 1600, 8], [68, 1700, 7.5], [62, 1550, 8.5],
    # Normal stress
    [75, 1500, 6.5], [72, 1450, 6.2], [78, 1550, 6.8],
    # High stress
    [85, 1300, 5], [90, 1200, 4.5], [82, 1350, 5.5]
]
y = ['low', 'low', 'low', 'normal', 'normal', 'normal', 'high', 'high', 'high']

# Create and train the Decision Tree Classifier
model = DecisionTreeClassifier()
model.fit(X, y)

# Function to predict stress level
def predict_stress(heart_rate, calories, sleep_time):
    avg_values = [[heart_rate, calories, sleep_time]]
    predicted_stress = model.predict(avg_values)[0]
    return predicted_stress

# Function to calculate averages
def calculate_averages(state):
    total = {'Calories': 0, 'Heart': 0, 'Move': 0, 'Steps': 0, 'Sleep': 0}
    days = len(state)

    for day in state:
        total['Calories'] += day['Calories']
        total['Move'] += day['Move']
        total['Steps'] += day['Steps']
        day['Sleep'] = round(random.uniform(7.0, 9.0), 2)  # Random sleep time between 7.0 and 9.0
        total['Sleep'] += day['Sleep']
        day['Heart'] = random.randint(60, 90)  # Random heart rate between 60 and 90
        total['Heart'] += day['Heart']
    print(total)
    return {
        'Calories': round(total['Calories'] / days, 2),
        'Heart': round(total['Heart'] / days, 2),
        'Move': round(total['Move'] / days, 2),
        'Steps': round(total['Steps'] / days, 2),
        'Sleep': round(total['Sleep'] / days, 2),
    }

# Example usage
if __name__ == "__main__":
    try:
        example_state = json.loads(sys.stdin.read())
        weekly_data = example_state.get('weeklyData', [])
        print(weekly_data)
        avg_values = calculate_averages(weekly_data)
        # print("Averages:", avg_values)

        heart_rate = avg_values['Heart']
        calories = avg_values['Calories']
        sleep_time = avg_values['Sleep']

        predicted_stress = predict_stress(heart_rate, calories, sleep_time)
        # print("Predicted Stress:", predicted_stress)
        # print("Action:", action)
        action = stress_levels[predicted_stress]['action']
        
        result = {'predictedStress': predicted_stress, 'action': action}
        print(json.dumps(result))
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except Exception as e:
        print("Error:", e)