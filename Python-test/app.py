from flask import Flask, redirect, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session
import requests
import json
from datetime import datetime, timedelta
import os

# Disable OAuthlib's HTTPS requirement when running locally.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load credentials
with open('creds.json') as f:
    credentials = json.load(f)['web']

client_id = credentials['client_id']
client_secret = credentials['client_secret']
redirect_uri = credentials['redirect_uris'][0]

# OAuth2 setup
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
scope = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.heart_rate.read",
    "https://www.googleapis.com/auth/fitness.body.read",
    "https://www.googleapis.com/auth/fitness.sleep.read",
    "https://www.googleapis.com/auth/fitness.reproductive_health.read",
    "https://www.googleapis.com/auth/userinfo.profile",
]

API_KEY = 'AIzaSyA8EvmpNJttuxsJi6A8lgfooLIuL2divRI'  # Replace with your API key

data_values = [
    {'title': 'Calories', 'type': 'com.google.calories.expended'},
    {'title': 'Heart', 'type': 'com.google.heart_minutes'},
    {'title': 'Move', 'type': 'com.google.active_minutes'},
    {'title': 'Steps', 'type': 'com.google.step_count.delta'},
    {'title': 'Sleep', 'type': 'com.google.sleep.segment'},
]

base_obj = {'Calories': 0, 'Heart': 0, 'Move': 0, 'Steps': 0}

app = Flask(__name__)
app.secret_key = 'secretKey'


def get_aggregated_data_body(data_type, end_time):
    return {
        'aggregateBy': [{'dataTypeName': data_type}],
        'bucketByTime': {'durationMillis': 86400000},
        'endTimeMillis': end_time,
        'startTimeMillis': end_time - 7 * 86400000,
    }


def get_weekly_data(end_time, access_token):
    state = []
    promises = []

    for i in range(31):
        curr_time = datetime.utcfromtimestamp(end_time / 1000) - timedelta(days=i)
        state.append({**base_obj, 'Date': curr_time.isoformat()})

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    for element in data_values:
        body = get_aggregated_data_body(element['type'], end_time)
        response = requests.post(
            f'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate?key={API_KEY}',
            headers=headers,
            json=body,
        )

        if response.status_code == 200:
            data = response.json()
            for idx in range(7):
                if idx < len(data['bucket']) and data['bucket'][idx]['dataset'][0]['point']:
                    for point in data['bucket'][idx]['dataset'][0]['point']:
                        for val in point['value']:
                            extract = val.get('intVal') or round(val.get('fpVal', 0))
                            state[idx][element['title']] += extract
        else:
            print(f"Error fetching data: {response.status_code} {response.text}")

    return state

@app.route('/auth/google')
def auth_google():
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline')
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/auth/google/callback')
def auth_google_callback():
    google = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    session['oauth_token'] = google.token
    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'oauth_token' not in session:
        return redirect(url_for('auth_google'))

    google = OAuth2Session(client_id, token=session['oauth_token'])
    end_time = int(datetime.utcnow().timestamp() * 1000)

    try:
        data = get_weekly_data(end_time, session['oauth_token']['access_token'])
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching fitness data: {e}")
        return redirect(url_for('error'))


@app.route('/error')
def error():
    return "An error occurred", 500


if __name__ == '__main__':
    app.run(port=5000)