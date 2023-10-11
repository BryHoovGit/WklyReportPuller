import requests
import dotenv
import os

dotenv.load_dotenv()

# Get the LIST_ID and API_KEY from the environment variables
API_KEY = os.getenv('API_KEY')
LIST_ID = os.getenv('LIST_ID')
SPACE_ID = os.getenv('SPACE_ID')
TEAM_ID = os.getenv('TEAM_ID')
STATUSES = os.getenv('STATUSES')

# Create a reusable headers object
headers = {
    'Authorization': f'{API_KEY}'
}

# Make the GET request to the ClickUp API to get the custom fields for a specific List
response = requests.get(
    f'https://api.clickup.com/api/v2/list/{LIST_ID}/field',
    headers=headers
)

# Check the response status code
if response.status_code == 200:
    # Success! Get the custom fields from the response
    custom_fields = response.json()['fields']

    # Print the custom fields to the console
    for custom_field in custom_fields:
        print(
            f'{custom_field["name"]} ({custom_field["type"]}) {custom_field["id"]}')

    # Make the GET request to the ClickUp API to get the filtered team tasks
    filtered_team_tasks_response = requests.get(
        f'https://api.clickup.com/api/v2/team/{TEAM_ID}/task?space_ids[]={SPACE_ID}&statuses[]={STATUSES}',
        headers=headers
    )

# Check the response status code
if filtered_team_tasks_response.status_code == 200:
    # Success! Get the filtered team tasks from the response
    filtered_team_tasks = filtered_team_tasks_response.json()['tasks']

    # Create an array to store the task IDs
    task_ids = []

    # Iterate over the filtered team tasks and add the task IDs to the array
    for task in filtered_team_tasks:
        task_ids.append(task['id'])

    # Print the array of task IDs and the length of the array
    print(f'Match count: {len(task_ids)}; Task IDs: {task_ids}')
else:
    # Something went wrong
    print(f'Error: {filtered_team_tasks_response.status_code}')
