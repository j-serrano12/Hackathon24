import requests
import re
import json
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import PhotoImage
from ttkbootstrap import Style

def recognize_speech_from_microphone():
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input.
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="blue")
        root.update()

        # Adjust for ambient noise to improve recognition accuracy
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio
        audio = recognizer.listen(source)

    try:
        # Using Google Speech Recognition to recognize the speech
        text = recognizer.recognize_google(audio)
        status_label.config(text="Processing...", fg="green")
        root.update()
        return text
    except sr.UnknownValueError:
        status_label.config(text="Could not understand audio.", fg="red")
        root.update()
        return None
    except sr.RequestError:
        status_label.config(text="Speech recognition service error.", fg="red")
        root.update()
        return None
    
def activate_recognition():
    # Call the function and assign the result to input_string
    input_string = recognize_speech_from_microphone()

    if input_string:
        # Regular expressions to extract data
        name_match = re.search(r'name (\w+)', input_string, re.IGNORECASE)
        phone_match = re.search(r'phone number (\d+)', input_string, re.IGNORECASE)
        employees_match = re.search(r'number of employees (\d+)', input_string, re.IGNORECASE)

        # Extracting values
        name = name_match.group(1) if name_match else "N/A"
        phone = phone_match.group(1) if phone_match else None
        employees = employees_match.group(1) if employees_match else None

        # Creating dictionary
        data = {
            "Name": name,
            "Phone": phone,
            "NumberOfEmployees": int(employees)
        }

        # Convert to JSON
        json_data = json.dumps(data, indent=4)

        # Output the result
        print(json_data)
        # Salesforce credentials (Consider using environment variables for security)
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

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
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
                    status_label.config(text="Account created successfully!", fg="green")
                else:
                    print("Error creating account:", create_account_response.json())
                    messagebox.showerror("Error", f"Error creating account: {create_account_response.json()}")
            else:
                print("Error authenticating:", response_data)
                messagebox.showerror("Error", f"Authentication failed: {response_data}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            messagebox.showerror("Error", f"Request failed: {e}")
    else:
        messagebox.showerror("Error", "Speech recognition failed. Try again!")
        status_label.config(text="Ready", fg="black")

# Create the UI window
root = tk.Tk()
root.title("Speech Recognition App")
root.geometry("590x660")
root.configure(bg="#91cff2")  # Light blue background

#load the image 
image = PhotoImage(file='bg-ornament-vertical-einstein.png')
image_label = tk.Label(root, image=image, bg="#91cff2")
image_label.pack(pady=20)


# Define fonts
title_font = font.Font(family="Open_Sans", size=36, weight="bold")
button_font = font.Font(family="Open_Sans", size=12)
status_font = font.Font(family="Open_Sans", size=14, slant="italic")

# Create a frame for the title
title_frame = tk.Frame(root,bd=0,bg='#91cff2')
title_frame.pack(pady=0)
title_label = tk.Label(title_frame, text="Jumini voice assistant", bg='#91cff2',font=title_font, fg="#333333")
title_label.pack()

# Create a frame for the button
button_frame = tk.Frame(root, bg="#91cff2")
button_frame.pack(pady=30)

# Create the button with enhanced styling
button = tk.Button(
    button_frame, 
    text="Click and Say something", 
    command=activate_recognition, 
    bg="#2c7524", 
    fg="white", 
    font=button_font,
    activebackground="#45a049",
    padx=20,
    pady=10,
    borderwidth=0,
    relief="flat"
)
button.pack()

# Create a status label
status_label = tk.Label(root, text="Ready", font=status_font,bg='#91cff2',fg="#333333")
status_label.pack(pady=20)

#style = Style(theme='darkly')

# Add a footer
footer_frame = tk.Frame(root, bg="#f0f0f0")
footer_frame.pack(side="bottom", fill="x", pady=10)

footer_label = tk.Label(footer_frame, text="© 2024 Jumini X Hackathon", font=("Helvetica", 8), bg="#f0f0f0", fg="#888888")
footer_label.pack()

# Start the Tkinter event loop
root.mainloop()
