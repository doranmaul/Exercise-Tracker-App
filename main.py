import requests
from datetime import datetime
import os

NUTRITIONIX_URL = "https://trackapi.nutritionix.com"
NUTRITIONIX_KEY = os.environ["NUTRITIONIX_KEY"]
NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]

SHEETY_URL = os.environ["SHEETY_URL"]
SHEETY_AUTH = os.environ["SHEETY_AUTH"]

auth_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_KEY,
    "Content-Type": "application/json"
}

exercises = input("Tell me which exercises you did: ")

parameters = {
    "query": exercises
}

exercise_endpoint = "/v2/natural/exercise"

response_nutritionix = requests.post(url=f"{NUTRITIONIX_URL}{exercise_endpoint}", json=parameters, headers=auth_headers)
response_nutritionix.raise_for_status()
data = response_nutritionix.json()

today = datetime.now()

date_formatted = today.strftime("%d/%m/%Y")
time_formatted = today.strftime("%H:%M:%S")
exercise = data["exercises"][0]["name"].title()
if data['exercises'][0]['duration_min'] > 60:
    minutes = round(data['exercises'][0]['duration_min'] % 60, 1)
    hours = round((data['exercises'][0]['duration_min'] - minutes) / 60, 1)
    if hours < 1.1:
        duration = f"{hours} hour and {minutes} minutes"
    else:
        duration = f"{hours} hours and {minutes} minutes"
else:
    duration = f"{round(data['exercises'][0]['duration_min'], 1)} minutes"
calories = round(data["exercises"][0]["nf_calories"], 1)

sheety_params = {
    "workout":
        {
            "date": date_formatted,
            "time": time_formatted,
            "exercise": exercise,
            "duration": duration,
            "calories": calories,
        }
}

sheety_header = {
    "Authorization": SHEETY_AUTH,
    "Content-Type": "application/json",
}

response_sheety = requests.post(url=SHEETY_URL, json=sheety_params, headers=sheety_header)
response_sheety.raise_for_status()

