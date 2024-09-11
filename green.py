import speech_recognition as sr
import webbrowser
import pyttsx3
from openai import OpenAI
from langdetect import detect
import os
import vlc

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize VLC player
player = vlc.MediaPlayer()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process AI commands using OpenAI API
def aiprocess(command, lang):
    client = OpenAI(api_key="YOUR_API_KEY")

    messages = [
        {"role": "system", "content": f"You are communicating in {lang} language."},
        {"role": "user", "content": command}
    ]

    completion = client.Completion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return completion.choices[0].message['content']

# Function to perform YouTube search using YouTube Data API
def youtube_search(query):
    api_key = "AIzaSyBwEN6OizZAubeFBx-kTF2886ZermC24-Q"
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=1,
        type="video"
    )
    response = request.execute()
    return response['items'][0]['id']['videoId']

# Function to detect language
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"  # Default to English if language detection fails

# Function to play a YouTube video
def play_youtube_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    webbrowser.open(url)

# Function to stop the song (requires VLC media player)
def stop_song():
    player.stop()

# Function to adjust volume
def adjust_volume(direction):
    current_volume = player.audio_get_volume()
    if direction == "increase":
        player.audio_set_volume(min(current_volume + 10, 100))
    elif direction == "decrease":
        player.audio_set_volume(max(current_volume - 10, 0))

# Function to process user commands
def processcommand(command):
    lang = detect_language(command)

    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in command.lower():
        webbrowser.open("https://instagram.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
        query = command.lower().split(" ", 1)[1]
        video_id = youtube_search(query)
        play_youtube_video(video_id)
    elif "stop" in command.lower():
        stop_song()
    elif "increase volume" in command.lower():
        adjust_volume("increase")
    elif "decrease volume" in command.lower():
        adjust_volume("decrease")
    else:
        output = aiprocess(command, lang)
        speak(output)

if __name__ == "__main__":
    speak("Initializing dx86...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language='hi-IN')  # Recognize in Hindi
            print("Command:", command)

            if "dx86" in command.lower():
                speak("Haan")  # Respond in Hindi

            processcommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
