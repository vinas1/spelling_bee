import random
from gtts import gTTS
import os
import subprocess
import time
import pygetwindow as gw
import psutil
import sys

# Define vlc_process as a global variable
vlc_process = None

# Get the directory where the script is located
script_directory = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Define the path to the words.txt file in the same directory as the script or executable
word_file = os.path.join(script_directory, "words.txt")
print(f"(c) 2024 Spelling Bee, written by JD for CD.")
# Fallback to sys.executable directory for bundled executables
if not os.path.isfile(word_file) and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    word_file = os.path.join(os.path.dirname(sys.executable), "words.txt")

# Check if the words.txt file exists
if not os.path.isfile(word_file):
    print("Error: 'words.txt' file not found. Make sure the file is in the same directory as the script.")
    sys.exit(1)

def find_vlc_path():
    """Attempts to locate the VLC installation path on Windows systems."""
    common_install_locations = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    ]

    for location in common_install_locations:
        if os.path.exists(location):
            return location

    # If not found in common locations
    print("VLC Player not found in standard locations.")
    return None

# Example Usage
vlc_path = find_vlc_path()
if vlc_path:
    print("VLC Player found at: {}".format(vlc_path))
else:
    print("Please install VLC or ensure it's in your system's PATH.")


def speak(text):
    global vlc_process  # Declare vlc_process as a global variable

    tts = gTTS(text=text, lang='en')
    audio_file = os.path.abspath("word.mp3")
    tts.save(audio_file)

    vlc_path = find_vlc_path()
    if vlc_path:
        if vlc_process is not None:
            vlc_process.terminate()  # Terminate the previous process if it exists

        vlc_process = subprocess.Popen([vlc_path, audio_file])  # Start VLC
        time.sleep(2)  # Adjust this delay as needed

        # Now try removing the file:
        try:
            os.remove(audio_file)
        except OSError:
            #print("Warning: Could not remove {}".format(audio_file))
            print("...")
        # Close VLC window after a short delay
        close_vlc_window()

# ... (rest of the code remains the same)


def close_vlc_window():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'vlc.exe' in proc.info['name'].lower():
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                process.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                pass


def get_spelling(word):
    """Gets the user's spelling attempt"""
    max_attempts = 2
    remaining_attempts = max_attempts

    for attempt in range(max_attempts):
        # Introduce a delay before playing the word for the first time
        if attempt == 0:
            time.sleep(1.5)  # Adjust this delay as needed
            for _ in range(2):
                speak(word)
                time.sleep(1)  # Adjust this delay if needed
        else:
            speak(word)
            time.sleep(1.5)  # Adjust this delay if needed

        guess = input("Spell the word: ").lower()
        if guess == word:
            print("Correct!\n")
            return True

        remaining_attempts -= 1
        if remaining_attempts > 0:
            print(f"Incorrect. {remaining_attempts} {'attempts' if remaining_attempts > 1 else 'attempt'} remaining.")
        else:
            repeat_attempt = input("Incorrect. Do you want to try again? (yes/no): ").lower()
            if repeat_attempt != "yes":
                print(f"Sorry, you're out of retries. The correct spelling is: {word}\n")
                return False
            else:
                print(f"Sorry, you're out of retries. The correct spelling is: {word}\n")
                print("Let's try again.\n")
                remaining_attempts = max_attempts

    return False










def spelling_bee(word_file):
    """Plays the spelling bee game with words from a file"""
    score = 0
    with open(word_file, 'r') as file:
        word_list = [word.strip().lower() for word in file]

    random.shuffle(word_list)

    for word in word_list:
        if not get_spelling(word):
            score += 1
            print(f"Your current score: {score} wrong\n")

    print(f"\nGame Over! Your final score: {score} wrong out of {len(word_list)}")

    # Ensure that VLC process is terminated after the game is finished
    if vlc_process is not None:
        vlc_process.terminate()

if __name__ == "__main__":
    spelling_bee(word_file)
