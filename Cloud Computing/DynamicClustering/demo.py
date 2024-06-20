import requests
import json

from secret_config import BASE_URL

# Define the URL and headers
url = BASE_URL + "/perform_clustering"                   # via deployed endpoint
# url = "http://localhost:8080/perform_clustering"           # via localhost

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


# Read the content of demo_input.json file
with open('demo_input.json', 'r') as file:
    demo_input = json.load(file)
print(type(demo_input))
# Define the data to be sent in the POST request
data = {
    "dataframe": demo_input
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    response_json = response.json()
    
    # Print the response JSON
    print("Response JSON: \n", json.dumps(response_json, indent=4))
    # Save the response JSON to a file with pretty formatting
    with open('demo_results.json', 'w') as json_file:
        json.dump(response_json, json_file, indent=4)
else:
    print(f"Request failed with status code {response.status_code}")