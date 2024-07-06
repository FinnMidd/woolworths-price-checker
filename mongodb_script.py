import requests
import json
import os

key = os.environ.get('MONGO_KEY')

url = "https://ap-southeast-2.aws.data.mongodb-api.com/app/data-tbnmcev/endpoint/data/v1/action/find"

payload = json.dumps({
    "collection": "collection1",
    "database": "woolworths-price-checker",
    "dataSource": "Cluster0",
    "limit": 100  # Adjust this number as needed
})
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': key,
}

response = requests.request("POST", url, headers=headers, data=payload)

# Parse the JSON response
data = response.json()

# Save the data to a JSON file
with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to data.json")