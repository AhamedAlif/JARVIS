import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import requests
from bs4 import BeautifulSoup
import pyjokes
import nmap
import pyautogui
from twilio.rest import Client
import openai

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Twilio configuration
twilio_sid = "your_twilio_sid"
twilio_auth_token = "your_twilio_auth_token"
twilio_phone_number = "your_twilio_phone_number"
recipient_phone_number = "recipient_phone_number"

# Initialize the Twilio client
client = Client(twilio_sid, twilio_auth_token)

# OpenAI GPT-3.5 API configuration
openai.api_key = "your_openai_api_key"

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis, your intelligent assistant and chatbot. How can I assist you today?")

# Function to listen to user's voice command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-US")
        print("User said:", query)
    except Exception as e:
        print("Sorry, I could not understand. Please try again.")
        return ""
    return query

# Function to send email
def send_email(receiver, subject, body):
    # Configure your email settings here
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver, message)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the email.")

# Function to fetch news headlines
def get_news_headlines():
    try:
        url = "https://news.google.com/rss"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:5]  # Fetching the first 5 news headlines
        headlines = [item.title.get_text() for item in items]
        return headlines
    except Exception as e:
        print(e)
        return []

# Function to fetch a random joke
def get_joke():
    return pyjokes.get_joke()

# Function to perform port scanning
def scan_ports(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments="-p-")
    open_ports = []
    for port in nm[target].all_tcp():
        if nm[target].tcp(port)["state"] == "open":
            open_ports.append(port)
    if open_ports:
        speak(f"The following ports are open on {target}:")
        for port in open_ports:
            speak(str(port))
    else:
        speak(f"No open ports found on {target}.")

# Function to take a screenshot
def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(screenshot_name)
    speak("Screenshot taken successfully!")

# Function to send a voice message
def send_voice_message(text):
    try:
        message = client.messages.create(
            body=text,
            from_=twilio_phone_number,
            to=recipient_phone_number,
            media_url=["https://your-audio-file-url"]
        )
        print("Voice message sent successfully!")
        speak("Voice message sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the voice message.")

# Function to generate a response using GPT-3.5 model
def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(e)
        return "Sorry, I am currently unable to generate a response."

# Function to perform actions based on user's command
def process_command(command):
    command = command.lower()
    if "wikipedia" in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia:")
        speak(results)
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
    elif "play music" in command:
        music_dir = "C:/Music"  # Replace with your music directory
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, random.choice(songs)))
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "send email" in command:
        speak("To whom do you want to send the email?")
        receiver = listen().lower()
        speak("What is the subject of the email?")
        subject = listen()
        speak("What should be the body of the email?")
        body = listen()
        send_email(receiver, subject, body)
    elif "news" in command:
        speak("Fetching the latest news headlines...")
        headlines = get_news_headlines()
        if headlines:
            speak("Here are the top news headlines:")
            for headline in headlines:
                speak(headline)
        else:
            speak("Sorry, I was unable to fetch the news headlines.")
    elif "joke" in command:
        joke = get_joke()
        speak("Here's a joke for you:")
        speak(joke)
    elif "scan ports" in command:
        speak("Please provide the target IP address or hostname.")
        target = listen().lower()
        scan_ports(target)
    elif "screenshot" in command:
        take_screenshot()
    elif "send voice message" in command:
        speak("What message would you like to send?")
        text = listen()
        send_voice_message(text)
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        gpt_prompt = f"You said: '{command}'"
        gpt_response = generate_response(gpt_prompt)
        speak(gpt_response)

# Main program loop
if __name__ == "__main__":
    greet()
    while True:
        command = listen()
        process_command(command)
