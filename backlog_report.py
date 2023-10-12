import requests
import dotenv
import os
import json

dotenv.load_dotenv()

# Get the LIST_ID and API_KEY from the environment variables
API_KEY = os.getenv('API_KEY')
LIST_ID = os.getenv('LIST_ID')
SPACE_ID = os.getenv('SPACE_ID')
TEAM_ID = os.getenv('TEAM_ID')
STATUSES = os.getenv('STATUSES')
PRIORITY_DD = os.getenv('FIELD_PRIORITY_DD')
SQUAD_DD = os.getenv('FIELD_SQUAD_DD')

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

    # Iterate over the custom fields and print the options id, name, and orderindex for each field
    for custom_field in custom_fields:
        print(
            f'{custom_field["name"]} | ID: {custom_field["id"]}')
        print(f'  Custom field type: {custom_field["type"]}')

        if custom_field['type'] == 'drop_down':
            for option in custom_field['type_config']['options']:
                print(f'  Option ID: {option["id"]}')
                print(f'    Option Name: {option["name"]}')
                print(f'    Option Order Index: {option["orderindex"]}')
        elif custom_field['type'] == 'labels':
            for option in custom_field['type_config']['options']:
                print(f'  Label ID: {option["id"]}')
                print(f'    Label Name: {option["label"]}')
else:
    # Something went wrong
    print(f'Error: {response.status_code}')

print()

# Create a JSON object to represent the custom field filter
#
epd_prio_filter_p0 = {
    "field_id": PRIORITY_DD,
    "value": 0,
    "operator": "="
}

# Create a JSON object to represent the custom field filter
#
epd_prio_filter_p1 = {
    "field_id": PRIORITY_DD,
    "value": 1,
    "operator": "="
}

# Create a JSON object to represent the custom field filter
#
epd_prio_filter_other = {
    "field_id": PRIORITY_DD,
    "value": 1,
    "operator": ">"
}

# Create a JSON object to represent the custom field filter
#
epd_prio_filter_null = {
    "field_id": PRIORITY_DD,
    "operator": "IS NULL"
}

# Stringify the JSON object
json_string = json.dumps([epd_prio_filter_p0])
json_string_p1 = json.dumps([epd_prio_filter_p1])
json_string_other = json.dumps([epd_prio_filter_other])
json_string_null = json.dumps([epd_prio_filter_null])

# Make the GET request to the ClickUp API to get the filtered team tasks
filtered_team_tasks_response = requests.get(
    f'https://api.clickup.com/api/v2/team/{TEAM_ID}/task?space_ids[]={SPACE_ID}&statuses[]={STATUSES}&custom_fields={json_string}',
    headers=headers
)

filtered_team_tasks_response_p1 = requests.get(
    f'https://api.clickup.com/api/v2/team/{TEAM_ID}/task?space_ids[]={SPACE_ID}&statuses[]={STATUSES}&custom_fields={json_string_p1}',
    headers=headers
)

filtered_team_tasks_response_other = requests.get(
    f'https://api.clickup.com/api/v2/team/{TEAM_ID}/task?space_ids[]={SPACE_ID}&statuses[]={STATUSES}&custom_fields={json_string_other}',
    headers=headers
)

filtered_team_tasks_response_null = requests.get(
    f'https://api.clickup.com/api/v2/team/{TEAM_ID}/task?space_ids[]={SPACE_ID}&statuses[]={STATUSES}&custom_fields={json_string_null}',
    headers=headers
)


# If all of the requests were successful, then print the output
if filtered_team_tasks_response.status_code == 200 and filtered_team_tasks_response_p1.status_code == 200 and filtered_team_tasks_response_other.status_code == 200 and filtered_team_tasks_response_null.status_code == 200:
    filtered_team_tasks = filtered_team_tasks_response.json()['tasks']
    filtered_team_tasks_p1 = filtered_team_tasks_response_p1.json()['tasks']
    filtered_team_tasks_other = filtered_team_tasks_response_other.json()[
        'tasks']
    filtered_team_tasks_null = filtered_team_tasks_response_null.json()[
        'tasks']

    # Create an array to store the task IDs
    task_ids = []
    task_ids_p1 = []
    task_ids_other_set = set()

    # Iterate over the filtered team tasks and add the task IDs to the array
    for task in filtered_team_tasks:
        task_ids.append(task['id'])

    for task in filtered_team_tasks_p1:
        task_ids_p1.append(task['id'])

    for task in filtered_team_tasks_other:
        task_ids_other_set.add(task['id'])

    for task in filtered_team_tasks_null:
        task_ids_other_set.add(task['id'])

    task_ids_other = list(task_ids_other_set)

    # Print the array of task IDs and the length of the array
    print(f'P0 count: {len(task_ids)}; Task IDs: {task_ids}')
    print(f'P1 count: {len(task_ids_p1)}; Task IDs: {task_ids_p1}')
    print(f'Other count: {len(task_ids_other)}; Task IDs: {task_ids_other}')
