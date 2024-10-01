import requests
import re
import json
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

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

def activate_recognition():
    # Call the function and assign the result to input_string
    input_string = recognize_speech_from_microphone()

    if input_string:
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
            "Name": name,
            "Phone": phone,
            "NumberOfEmployees": int(employees) if employees else None
        }

        # Convert to JSON
        json_data = json.dumps(data, indent=4)

        # Output the result
        print(json_data)
        messagebox.showinfo("Recognition Result", f"Data: {json_data}")

        # Salesforce credentials (You should ideally not hardcode credentials)
        # Salesforce credentials
        client_id = '3MVG90biqdLHqqMTbYjPlAYYzVwasrNt_nB9ZmrUsD.xTeGok_7wHFfSVcy8Cz55GL6KEcHpXeqhch1ldLLKf'
        client_secret = '7F2FD63C4A72A4EDA0A7D44DD8366EA1AA7C844F1301737744C31E42B38A1040'
        username = 'test-jwdcxme9mpl9@example.com'
        password = '3f$slnutDrkneT6B1otzkT4xjhfMM6ntXOXyn'

        # Step 1: Get OAuth token
        token_url = 'https://fun-data-4626-dev-ed.scratch.my.salesforce.com/services/oauth2/token'
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
            account_payload = data

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            create_account_response = requests.post(account_url, json=account_payload, headers=headers)

            if create_account_response.status_code == 201:
                print("Account created successfully:", create_account_response.json())
                messagebox.showinfo("Success", "Account created successfully!")
            else:
                print("Error creating account:", create_account_response.json())
                messagebox.showerror("Error", "Error creating account!")
        else:
            print("Error authenticating:", response_data)
            messagebox.showerror("Error", "Authentication failed!")
    else:
        messagebox.showerror("Error", "Speech recognition failed. Try again!")

# Create the UI window
root = tk.Tk()
root.title("Speech Recognition")
root.geometry("300x200")

# Create the button and bind it to the activate_recognition function
button = tk.Button(root, text="Start Recognition", command=activate_recognition)
button.pack(pady=50)

# Start the Tkinter event loop
root.mainloop()
