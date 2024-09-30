import requests
import re
import json
import speech_recognition as sr

def recognize_speech_from_microphone():
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input.
    with sr.Microphone() as source:
        print("Please say something...")

        # Adjust for ambient noise to improve recognition accuracy
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio
        audio = recognizer.listen(source)

        try:
            # Using Google Speech Recognition to recognize the speech
            text = recognizer.recognize_google(audio)
            print("You said: ", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return None

if __name__ == "__main__":
    # Call the function and assign the result to input_string
    input_string = recognize_speech_from_microphone()



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


    # Salesforce credentials
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    username = 'your_salesforce_username'
    password = 'your_salesforce_password_and_security_token'

    # Step 1: Get OAuth token
    token_url = 'https://login.salesforce.com/services/oauth2/token'
    payload = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }

    response = requests.post(token_url, data=payload)
    response_data = response.json()

    if 'access_token' in response_data:
        access_token = response_data['access_token']
        instance_url = response_data['instance_url']

        # Step 2: Create a new Account
        account_url = f"{instance_url}/services/data/v56.0/sobjects/Account/"
        account_payload = {
            json_data
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        create_account_response = requests.post(account_url, json=account_payload, headers=headers)

        if create_account_response.status_code == 201:
            print("Account created successfully:", create_account_response.json())
        else:
            print("Error creating account:", create_account_response.json())
    else:
        print("Error authenticating:", response_data)
