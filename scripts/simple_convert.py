#!/usr/bin/env python3

import json
from collections import defaultdict

# Define the groups and their variables
VARIABLE_GROUPS = {
    'Django Configuration': ['DJANGO_SECRET_KEY'],
    'Database Settings': ['AZURE_SQL_DB_NAME', 'AZURE_SQL_DB_USER', 'AZURE_SQL_DB_PASSWORD', 
                         'AZURE_SQL_DB_HOST', 'AZURE_SQL_DB_PORT'],
    'Storage Settings': ['AZURE_ACCOUNT_NAME', 'AZURE_ACCOUNT_KEY', 'AZURE_CONTAINER']
}

# Create reverse mapping for easy lookup
VAR_TO_GROUP = {
    var: group for group, vars in VARIABLE_GROUPS.items() for var in vars
}

def get_group_comment(group_name):
    return {
        "name": f"# {group_name}",
        "value": "----------------------------",
        "slotSetting": False
    }

# Read the .env file
env_vars = defaultdict(list)
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            try:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip("'").strip('"')
                
                # Find the group for this variable
                group = VAR_TO_GROUP.get(key, 'Other Settings')
                
                env_vars[group].append({
                    "name": key,
                    "value": value,
                    "slotSetting": False
                })
                print(f"Processed: {key} (Group: {group})")
            except ValueError:
                print(f"Skipping invalid line: {line}")

# Organize the final output
final_list = []
for group in ['Django Configuration', 'Database Settings', 'Storage Settings', 'Other Settings']:
    if env_vars[group]:
        if final_list:  # Add a blank line between groups
            final_list.append({
                "name": "",
                "value": "",
                "slotSetting": False
            })
        final_list.append(get_group_comment(group))
        final_list.extend(env_vars[group])

# Write to JSON
with open('env_config.json', 'w') as f:
    json.dump(final_list, f, indent=2)
    print("\nJSON data written to env_config.json with grouped variables")
