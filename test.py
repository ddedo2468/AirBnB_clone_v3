#!/usr/bin/python3

import requests
import json

# API endpoint URL
url = "http://0.0.0.0:5000/api/v1/states"

# Sample state data
state_data = {
    "name": "New State",
    # Include other required fields if necessary
}

# Convert state data to JSON format
state_json = json.dumps(state_data)

# Set headers for the request
headers = {
    "Content-Type": "application/json",
}

# Make a POST request to create a new state
response = requests.post(url, data=state_json, headers=headers)

# Print the response status code and content
print("Response Status Code:", response.status_code)
print("Response Content:", response.text)
