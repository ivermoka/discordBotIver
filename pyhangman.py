import random
from hangmanord import ord
import string


def get_valid_word(words):
    word = random.choice(words)
    while "-" in words or " " in words:
        word = random.choice(words)

    return word

def hangman():
    word = get_valid_word(ord)
    word_letters = set(word) # bokstavene i ordet
    alphabet = set(string.ascii_lowercase)
    used_letter = set() #hvilke ord som har blitt brukt
    
    lives = 10

    while len(word_letters) > 0 and lives > 0:
        print("Du har", lives, " liv igjen og du har brukt disse bokstavene: ", " ".join(used_letter))

        word_list= [letter if letter in used_letter else "-" for letter in word]
        print("Nåværende ord: ", " ".join(word_list))

        user_letter = input("Gjett en bokstav: ").lower() # få bruker til å legge inn bokstav
        if user_letter in alphabet - used_letter:
            used_letter.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)

            else:
                lives = lives - 1
                print("Bokstaven din er ikke i ordet.")
        elif user_letter in used_letter:
            print("Du har allerede brukt den bokstaven")
        else: 
            print("Ugyldig bokstav. Prøv igjen.")
    #fortsetter hvis antall ord igjen er større enn 0

    if lives == 0:
        print(f"Du døde, ordet var {word}. Bedre lykke neste gang.")
    else: 
        print(f"Du gjettet ordet {word}!")

hangman()