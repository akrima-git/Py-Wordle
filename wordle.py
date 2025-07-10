import random

correct_chars_streak = []

def generate_word():
    with open("wordles.txt","r") as file:
        words = [line.strip() for line in file.readlines()]


    size = len(words)
    random_number = random.randint(0,size)
    ##print(random_number, words[random_number])
    return words[random_number], words


def validation(guess,word):
    correct_chars = ["⬜"] * 5
    for index1,char1 in enumerate(guess):
        for index2,char2 in enumerate(word):
            ##print(index1,char1,index2,char2)
            if char1 == char2:
                word = word.replace(char2,"*",1)
                if index1 == index2:
                    correct_chars[index1] = "🟩"
                else:
                    correct_chars[index1] = "🟧"

                break
    print(guess)
    print(word)
    correct_chars_streak.append("".join(correct_chars))
    for _ in correct_chars_streak:
        print(_)


    


def guessing_game():
    valid_guess = False
    guess_counter = 0
    selected_word, word_list = generate_word()
    ##print(selected_word)
    print("If you'd like to exit the game, please type 'QUIT'")
    while not valid_guess:
        guess = input("Enter a 5 character word: ")
        if guess.upper() == "QUIT":
            exit
        if len(guess) == 5 and guess in word_list:
            print("you guessed a valid word")
            guess_counter += 1
            if guess == selected_word:
                valid_guess = True
            validation(guess,selected_word)
        else:
            print("Enter a valid word")
        if guess_counter == 5:
            print("You lose dood")
            break
    play_again = input("Would you like to have another go? (Y/N) ")
    guessing_game() if play_again.upper() == "Y" else exit


guessing_game()
            
