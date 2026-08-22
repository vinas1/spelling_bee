#2-20-2024
#Josh Davis
#https://www.linkedin.com/in/josh-davis101/
#This is a spelling bee program to help kids with spelling. 
#Keep a words.txt file in the root folder with one word per line.
#Validation testing completed in pyton 3.12

#import random
import os
#import time
#import psutil
import sys
import pyttsx3
#from gtts import gTTS
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) 

# Constants
WORD_FILE = "words.txt"


def load_words(word_file):
    """Loads words from the word file."""
    if not os.path.isfile(word_file):
        print(f"Error: Word file '{word_file}' not found.")
        sys.exit(1)

    try:
        with open(word_file, 'r') as file:
            return [word.strip().lower() for word in file]
    except (IOError, OSError) as e:
        print(f"Error reading word file: {e}")
        sys.exit(1)



def play_word(word, attempt_number=1, difficulty="normal", spell_out=False):
    """Speaks the word, optionally providing hints or spelling it out.

    Args:
        word: The word to be spoken.
        attempt_number: Current attempt number for the word.
        difficulty: The difficulty level (easy, normal, hard).
        spell_out: If True, spells the word letter-by-letter.
    """ 
    try:
        initial_rate = 140
        adjusted_rate = max(30, initial_rate - 60 * (attempt_number - 1))
        engine.setProperty('rate', adjusted_rate)

        if attempt_number > 1:
            if difficulty == "easy":
                # Always give a hint on every incorrect attempt
                engine.setProperty('rate', initial_rate)
                engine.say(f"Our word starts with the letter, {word[0]}... Listen carefully. Spell,")
                engine.runAndWait()
                engine.setProperty('rate', adjusted_rate) 
            elif difficulty == "normal":
                # Give a hint after two or more failed attempts
                if attempt_number >= 3:
                    engine.setProperty('rate', initial_rate)
                    engine.say(f"The word starts with the letter, {word[0]}... Listen carefully. Spell,")
                    engine.runAndWait()
                    engine.setProperty('rate', adjusted_rate) 
            elif difficulty == "hard":
                # No hints at all!
                pass 

        # Speak the word (either normally or spelling it out)
        if spell_out: 
            for letter in word:
                engine.say(letter)
                engine.runAndWait()
        else:
            engine.say(word) 
            engine.runAndWait()

        engine.setProperty('rate', initial_rate)  

    except Exception as e:
        print(f"Error playing audio: {e}")






def get_spelling_attempt(word, max_attempts=3):
    """Gets the user's spelling attempt with retries."""
    remaining_attempts = max_attempts
    for _ in range(max_attempts):
        for _ in range(2): 
            play_word(word, attempt_number=remaining_attempts) 
            time.sleep(0.75)  

        guess = input(f"Spell the word ({remaining_attempts} retries left): ").lower() 
        if guess == word:
            print("Correct!\n")
            return True
        else:
            remaining_attempts -= 1 
            print("Incorrect.\n")
            time.sleep(0.75)  
    return False


def spelling_bee_game():
    """Main spelling bee game function."""
    print(f"(c) 2024 Spelling Bee, written by JD for CD.")
    engine.say(f"Welcome to the Spelling Bee version 2... Let's begin, spell...")
    word_file = get_bundled_word_file()
    words = load_words(word_file)  # Load words here

    total_words = len(words)
    incorrect_answers = 0  # Track incorrect answers
    misspelled_words = []  # Initialize the list

    for word in words:
        attempt_number = 1  # Reset attempts for each word
        max_attempts = 3

        while attempt_number <= max_attempts:
            #print(f"Before calling play_word, attempt_number is: {attempt_number}") 
            play_word(word, attempt_number)  

            guess = input(f"Spell the word ({max_attempts - attempt_number + 1} retries left): ").lower() 
            if guess == word:
                print("\033[1;37mCorrect!\033[0m\n")  # Bold white text
                break  # Exit the attempt loop for this word
            else:
                print("\033[91mIncorrect.\033[0m\n")  # Red text
                attempt_number += 1  # Increment if the guess was wrong

        if not guess == word: 
            incorrect_answers += 1
            misspelled_words.append(word)
            engine.say(f"Listen to the correct spelling of the word, {word}...")
            play_word(word, spell_out=True)  # Spell out the word 
            print("\033[91m" + word + "\033[0m\n")  # Red text  
            engine.runAndWait()

        #print("End of word processing, rate is:", engine.getProperty('rate'))  # Debugging 

        # ...  (potential code here  to  prepare for the next word if needed) ... 

        #print("Before calling play_word for the next word, rate is:", engine.getProperty('rate'))  # Debugging
        percentage_correct = (1 - (incorrect_answers / total_words)) * 100 
        print(f"Your current score: {incorrect_answers} wrong ({percentage_correct:.1f}% correct)\n") 

    # Game Over with Encouragement (This needs to be outside the word processing loop)
    percentage_correct = (1 - (incorrect_answers / total_words)) * 100 
    print(f"Game Over! Your final score: {incorrect_answers} wrong ({percentage_correct:.1f}% correct)\n")
    engine.say(f"Game Over! Your final score: {incorrect_answers} wrong ({percentage_correct:.1f}% correct)")
    engine.runAndWait()  # Process the spoken output

    # Recap of Misspelled Words
    if misspelled_words:  
        print("\nYour Misspelled Words:")
        for word in misspelled_words:
            print("\033[91m" + word + "\033[0m\n")  # Red text
    else:
        print("\nYou got all the words right! Perfect game!")

    # Customize the encouragement based on performance
    if percentage_correct >= 90:
        print("Amazing work! You're a true spelling champion.")
        engine.say(f"Amazing work! You're a true spelling champion.")
        engine.runAndWait()  # Process the spoken output 
    elif percentage_correct >= 70:
        print("Great job! Keep practicing, and you'll be a spelling pro in no time.")
        engine.say(f"Great job! Keep practicing, and you'll be a spelling pro in no time.")
        engine.runAndWait()  # Process the spoken output 
    else:
        print("Don't get discouraged! Practice makes perfect.  Keep at it!")
        engine.say(f"Don't get discouraged! Practice makes perfect.  Keep at it!")
        engine.runAndWait()  # Process the spoken output 

    input("Press Enter to exit...")  # Pause at the end


 


def get_bundled_word_file():
    """Returns word file path relative to script or executable."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, WORD_FILE)

# Initialize the pyttsx3 engine
engine = pyttsx3.init() 

if __name__ == "__main__":
    spelling_bee_game() 
