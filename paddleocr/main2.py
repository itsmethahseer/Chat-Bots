
import json

# Load the JSON file
with open('input.json', 'r') as file:
    data = json.load(file)

# Check the total number of JSON objects
total_objects = len(data)

print(f"Total number of JSON objects: {total_objects}")
