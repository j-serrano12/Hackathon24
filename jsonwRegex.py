import re
import json

# Input string
input_string = 'Create an account with name jalapa phone number 655369988 number of employees 69'

# Regular expressions to extract data
name_match = re.search(r'name (\w+)', input_string)
phone_match = re.search(r'phone number (\d+)', input_string)
employees_match = re.search(r'number of employees (\d+)', input_string)

# Extracting values
name = name_match.group(1) if name_match else None
phone = phone_match.group(1) if phone_match else None
employees = employees_match.group(1) if employees_match else None

# Creating dictionary
data = {
    "name": name,
    "phone": phone,
    "employees": employees
}

# Convert to JSON
json_data = json.dumps(data, indent=4)

# Output the result
print(json_data)
