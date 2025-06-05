from os import startfile
import webbrowser
import speech_recognition as sr
import win32com.client
from openai import OpenAI
from confict import apikey


def ai(prompt):
    client = OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=apikey
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    ans = response.choices[0].message.content
    print(ans)
    return ans


# Initialize the Windows voice engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speak intro
speaker.Speak("Hi, I am Jarvis, built by Sai Pawan , How can I help you")

# Function to take voice input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis: Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Jarvis: Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
        except sr.UnknownValueError:
            print("Jarvis: Sorry, I didn't catch that.")
            speaker.Speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Jarvis: Network error.")
            speaker.Speak("There is a network issue.")
            return ""

        return query

# Continuous voice interaction loop
while True:
    spoken_text = takecommand()

    if "stop" in spoken_text.lower():
        speaker.Speak("Okay, stopping now. Goodbye! Pawan")
        break

    # Check for site opening commands
    sites = [["youtube", "https://youtube.com"], ["wikipedia", "https://www.wikipedia.com"]]
    for site in sites:
        if f"open {site[0]} jarvis" in spoken_text.lower():
            speaker.Speak(f"Opening {site[0]} for you sir")
            webbrowser.open(site[1])
            break  # to avoid saying the spoken_text again

    # Check for music play command
    if "play music" in spoken_text.lower():
        music_path = r"C:\Users\saipa\Downloads\vinee-heights-126947.mp3"
        speaker.Speak("Playing your music now.")
        startfile(music_path)

    if "using AI ".lower() in spoken_text.lower():
        ans = ai(prompt=spoken_text)
        speaker.Speak(ans)


    # Speak the recognized command back (optional)
    #speaker.Speak(spoken_text)
