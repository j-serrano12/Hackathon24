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
    recognize_speech_from_microphone()
