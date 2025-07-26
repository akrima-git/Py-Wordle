import random
import sys

# ANSI color codes
GREEN_BG = "\033[42m"      # Green background for correct position
YELLOW_BG = "\033[43m"     # Yellow background for wrong position
GRAY_BG = "\033[100m"      # Light gray background for unused letters
BLACK_BG = "\033[40m"      # Black background for incorrect letters
BLACK_FG = "\033[30m"      # Black text
WHITE_FG = "\033[97m"      # White text (for black background)
RESET = "\033[0m"

# Keyboard layout
KEYBOARD = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

correct_chars_streak = []  # Stores the feedback (🟩, 🟧, ⬜)
guesses = []  # Stores the actual guessed words
letter_states = {}  # Tracks the state of each letter (gray, yellow, green)

def colorize_letter(letter, bg_color):
    # Use white text for black background, black text for other backgrounds
    fg_color = WHITE_FG if bg_color == BLACK_BG else BLACK_FG
    return f"{bg_color}{fg_color} {letter.upper()} {RESET}"

def display_keyboard():
    print("\nKeyboard:")
    # First row width determines the center point
    max_row_len = len(KEYBOARD[0])  # Length of first row (QWERTYUIOP)
    
    for row in KEYBOARD:
        colored_row = []
        for letter in row:
            if letter in letter_states:
                colored_row.append(colorize_letter(letter, letter_states[letter]))
            else:
                colored_row.append(colorize_letter(letter, GRAY_BG))
        
        # Calculate padding based on the number of letters, not the string length
        spaces_needed = (max_row_len - len(row)) * 2  # Each letter takes 4 spaces with colors
        padding = " " * spaces_needed
        print(padding + " ".join(colored_row))

def generate_word():
    with open("wordles.txt","r") as file:
        words = [line.strip() for line in file.readlines()]

    size = len(words)
    random_number = random.randint(0, size - 1)  # Fix off-by-one error
    return words[random_number], words


def validation(guess, word):
    feedback = []
    word_chars = list(word)
    display_chars = []
    current_guess_states = {}  # Track states for current guess
    
    # First pass: check for correct positions (green)
    for i, (guess_char, word_char) in enumerate(zip(guess, word)):
        if guess_char == word_char:
            feedback.append("🟩")
            display_chars.append(colorize_letter(guess_char, GREEN_BG))
            word_chars[i] = "*"
            current_guess_states[guess_char.upper()] = GREEN_BG
        else:
            feedback.append("⬜")
            display_chars.append(None)
    
    # Second pass: check for correct letters in wrong positions (yellow)
    for i, guess_char in enumerate(guess):
        if display_chars[i] is not None:  # Skip already marked green
            continue
        found_yellow = False
        for j, word_char in enumerate(word_chars):
            if guess_char == word_char:
                feedback[i] = "🟧"
                display_chars[i] = colorize_letter(guess_char, YELLOW_BG)
                word_chars[j] = "*"
                if guess_char.upper() not in current_guess_states:  # Don't override green
                    current_guess_states[guess_char.upper()] = YELLOW_BG
                found_yellow = True
                break
        if not found_yellow:
            display_chars[i] = colorize_letter(guess_char, BLACK_BG)
            if guess_char.upper() not in current_guess_states:  # Don't override green or yellow
                current_guess_states[guess_char.upper()] = BLACK_BG
    
    # Update global letter states (only upgrade, never downgrade)
    for letter, state in current_guess_states.items():
        if letter not in letter_states or state == GREEN_BG or (state == YELLOW_BG and letter_states[letter] == GRAY_BG):
            letter_states[letter] = state
    
    result = "".join(feedback)
    correct_chars_streak.append(result)
    guesses.append(guess)  # Store the current guess
    
    # Print the current guess with colored backgrounds
    print("\nGuess:", " ".join(display_chars))
    
    # Print guess history with consistent colors
    print("\nGuess history:")
    for past_guess, history in zip(guesses, correct_chars_streak):
        colored_word = []
        for past_char, feedback_char in zip(past_guess, history):
            if feedback_char == "🟩":
                colored_word.append(colorize_letter(past_char, GREEN_BG))
            elif feedback_char == "🟧":
                colored_word.append(colorize_letter(past_char, YELLOW_BG))
            else:
                colored_word.append(colorize_letter(past_char, BLACK_BG))  # Always use black for incorrect letters
        print(" ".join(colored_word))
    
    # Display keyboard with updated letter states
    display_keyboard()


    


def guessing_game():
    MAX_ATTEMPTS = 6  # Standard Wordle has 6 attempts
    selected_word, word_list = generate_word()
    guess_counter = 0
    
    # Clear previous game's data
    correct_chars_streak.clear()
    guesses.clear()
    letter_states.clear()
    
    print("\nWelcome to Wordle!")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the 5-letter word.")
    print(f"{GREEN_BG}{BLACK_FG} A {RESET} = Correct letter in correct position")
    print(f"{YELLOW_BG}{BLACK_FG} A {RESET} = Correct letter in wrong position")
    print(f"{GRAY_BG}{BLACK_FG} A {RESET} = Letter not in word")
    print("Type 'QUIT' to exit the game\n")

    while guess_counter < MAX_ATTEMPTS:
        remaining = MAX_ATTEMPTS - guess_counter
        guess = input(f"\nEnter a 5-letter word ({remaining} attempts remaining): ").lower()
        
        if guess.upper() == "QUIT":
            print("Thanks for playing!")
            sys.exit()
            
        if len(guess) != 5:
            print("Error: Please enter a 5-letter word")
            continue
            
        if guess not in word_list:
            print("Error: Word not in word list")
            continue
        
        guess_counter += 1
        validation(guess, selected_word)
        
        if guess == selected_word:
            print(f"\nCongratulations! You won in {guess_counter} attempts!")
            break
            
    if guess != selected_word:
        print(f"\nGame Over! The word was: {selected_word}")
    
    while True:
        play_again = input("\nWould you like to play again? (Y/N): ")
        if play_again.upper() in ['Y', 'N']:
            break
        print("Please enter 'Y' or 'N'")
    
    if play_again.upper() == 'Y':
        guessing_game()
    else:
        print("Thanks for playing!")
        sys.exit()


guessing_game()
            
