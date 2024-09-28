import os
import random
import json
import logging
import spacy
import nltk
import numpy as np
import subprocess
import pyautogui
import requests
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Define a base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup paths for necessary files and folders
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'chatbot.log')

INTENTS_FILE = os.path.join(BASE_DIR, 'intents.json')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load intents
with open(INTENTS_FILE, 'r') as file:
    intents = json.load(file)

# Extract patterns and tags for training
patterns = []
tags = []
responses = {}

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokenized_pattern = ' '.join([lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(pattern)])
        patterns.append(tokenized_pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Vectorize patterns and train the model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns)
y = np.array(tags)

# Logistic Regression classifier
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Your OpenWeatherMap API key
API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key


def clean_text(text):
    doc = nlp(text)
    tokens = [lemmatizer.lemmatize(token.text.lower()) for token in doc]
    return ' '.join(tokens)


def predict_tag(text):
    cleaned_text = clean_text(text)
    text_vector = vectorizer.transform([cleaned_text])
    return model.predict(text_vector)[0]


def get_response(tag):
    return random.choice(responses[tag])


def execute_command(command):
    try:
        # Mapping of commands to actual applications
        command_map = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "chrome": ["start", "chrome"],
            "firefox": ["start", "firefox"],
            "media player": ["wmplayer"],
            "restart": ["shutdown", "/r", "/t", "0"],
            "shutdown": ["shutdown", "/s", "/t", "0"],
            "explorer": ["explorer"],
            # Add more applications as needed
        }

        # Normalize the command
        command = command.lower().strip()

        if command in command_map:
            subprocess.Popen(command_map[command])
            return f"Opened {command.capitalize()}."
        else:
            return "Command not recognized. Please try again."
    except Exception as e:
        logging.error(f"Error opening application: {str(e)}")
        return "Failed to open the application."


def automate_task(task):
    if task == "take a screenshot":
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(BASE_DIR, "screenshot.png"))
        return "Screenshot taken and saved."
    elif task == "open browser":
        # Open the default web browser
        subprocess.Popen(["start", "chrome"], shell=True)
        return "Opened the web browser."
    elif task == "volume up":
        # Increase the system volume (Windows)
        pyautogui.press('volumeup')
        return "Volume increased."
    elif task == "volume down":
        # Decrease the system volume (Windows)
        pyautogui.press('volumedown')
        return "Volume decreased."
    elif task == "mute":
        # Mute the system volume (Windows)
        pyautogui.press('volumemute')
        return "Volume muted."
    elif task == "open notepad":
        subprocess.Popen(["notepad.exe"])
        return "Opened Notepad."
    elif task == "type hello":
        # Type 'Hello' at the current cursor position
        pyautogui.write('Hello')
        return "Typed 'Hello'."
    elif task == "open google":
        # Open Google in the default web browser
        subprocess.Popen(["start", "chrome", "https://www.google.com"], shell=True)
        return "Opened Google."
    elif task == "shutdown":
        # Shutdown the computer
        subprocess.Popen(["shutdown", "/s", "/t", "1"])
        return "Shutting down the computer."
    elif task == "restart":
        # Restart the computer
        subprocess.Popen(["shutdown", "/r", "/t", "1"])
        return "Restarting the computer."
    else:
        return "Task not recognized."



def check_weather(city):
    """Check the weather for the given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "Could not retrieve weather information. Please check the city name."


def chatbot_response(user_input):
    try:
        tag = predict_tag(user_input)
        response = get_response(tag)

        # Check for special commands
        if "open google" in user_input.lower():
            response = execute_command("chrome")  # Open Google in Chrome
        elif "weather" in user_input.lower():
            city = input("Which city do you want to check the weather for? ")
            response = check_weather(city)  # Check weather for the specified city
        elif "open" in user_input.lower():
            app_name = user_input.lower().replace("open", "").strip()
            response = execute_command(app_name)  # Attempt to open the app
        elif "automate" in user_input.lower():
            task = user_input.lower().replace("automate", "").strip()
            response = automate_task(task)  # Attempt to automate the task

        logging.info(f"User Input: {user_input} | Predicted Tag: {tag} | Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return "Sorry, I didn't understand that. Can you please rephrase?"


# Main chat loop
def chat():
    print("\n\033[1;32mChatBot: Hello! How can I assist you today? (type 'quit' to exit)\033[0m")
    while True:
        user_input = input("\033[1;34mYou: \033[0m")
        if user_input.lower() == 'quit':
            print("\033[1;31mChatBot: Goodbye! Have a great day!\033[0m")
            break
        response = chatbot_response(user_input)
        print(f"\033[1;36mChatBot: {response}\033[0m")


if __name__ == '__main__':
    chat()
