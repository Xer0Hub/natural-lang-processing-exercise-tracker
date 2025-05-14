"""This application was intended for Sheety to Excel integration. It allows you to input workout / health data and in turn it will auto populate an Excel sheet
you designate to the script."""

#-------IMPORTS-------#
import requests
import datetime
import json

#-------CONSTANTS-------#
#AUTHENTICATION
API_KEY = "YOUR API KEY"
AP_ID = "YOUR AP ID"
TOKEN = "YOUR TOKEN"

#USER
GENDER = ""
WEIGHT_KG = 0
HEIGHT_CM = 0
AGE = 0

#PROJECT
USERNAME = "YOUR USERNAME"
PROJECT_NAME = "YOUR PROJECT NAME"
SHEET_NAME = "YOUR SHEET NAME"

#-------API END POINTS-------#
#Nutritionix end point
nutritionix_endpoint = "https://trackapi.nutritionix.com"
#Natural Language for Nutrients
nlp_nutrients = "v2/natural/nutrients"
#Instant Endpoint
autocomplete = "v2/search/instant"
#Search-Item Endpoint w/ UPC scan interpreter
scanner = "v2/search/item"
#Parse requests like "30 minutes yoga" and calculate the calories burned.
nlp_exercise_calories = "v2/natural/exercise"

#POST TO SHEET
sheet_endpoint = "YOUR SHEET ENDPOINT"

#-------DICTIONARIES-------#
headers = {
    "x-app-id": AP_ID,
    "x-app-key": API_KEY
}

#QUESTION ASKED USER
daily_question = input("What exercise(s) did you do today?: ")

parameters = {
    "query": daily_question,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

#-------SEARCH QUERY MADE TO SERVER-------#
query_data = requests.post(url=f"{nutritionix_endpoint}/{nlp_exercise_calories}" , json= parameters, headers=headers)
query_response = query_data.json()
print(query_response)

#-------POST QUERY MADE TO SERVER-------#
#VARIABLES
exercise = query_response["exercises"][0]["user_input"].title()
print(exercise)
duration = query_response["exercises"][0]['duration_min']
calories = query_response["exercises"][0]['nf_calories']

date_time_today = datetime.datetime.today()
#TODO might throw an error later if the date isn't reversed.
date_today = date_time_today.date()
print(date_today)
formatted_date = date_today.strftime("%d/%m/%Y")
print(formatted_date)

time_today = date_time_today.time().strftime("%X")
print(time_today)

sheet_inputs = {
    "workout": {
        "date": formatted_date,
        "time": time_today,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

headers = {
    "Authorization": "Bearer YOUR TOKEN"
}

json_payload = json.dumps(sheet_inputs)

sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)

#-------GET QUERY MADE TO SERVER-------#

print(sheet_response.text)