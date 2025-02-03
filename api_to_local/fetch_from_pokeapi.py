import requests
import json

# URL for the Ditto Pokemon data
url = 'https://pokeapi.co/api/v2/pokemon/ditto'

# Make the GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the JSON response data
    data = response.json()

    # Specify the file path to write the data to
    file_path = './ditto_data.json'

    # Write the JSON data to the local file system
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data has been successfully written to {file_path}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
