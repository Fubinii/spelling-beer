import random
import math

default_wordlist = 'en_US_60_SB.txt'

# Loading the dictionary
def load_wordlist(default_wordlist):
    with open(default_wordlist) as dic:
        word_list = [w.strip() for w in dic if w.strip()]
    return word_list

def display_letters(letters, center_letter, score, total_score):
    letters = letters.replace(center_letter, '')
    # Honeycomb display for 7 letters
    if len(letters) == 7:
        letters = letters[:3] + center_letter + letters[3:]
        print(' ', letters[1].upper(), letters[2].upper(), '  |')
        print(letters[2].upper(), '('+letters[3].upper()+')', letters[4].upper(), '|', end=' ')
        print(f'Score: {score} / {total_score}') # To do: turn this into ranks
        print(' ', letters[5].upper(), letters[6].upper(), '  |')
    
    else:
        letters = center_letter + letters
        n = math.ceil(math.sqrt(len(letters)))
        for i, letter in enumerate(letters):
            if i%n == 0 and i != 0: 
                print()
                print('', end=' ')
            if letter != center_letter:
                print(letter.upper(), end=" ")
            else: 
                print('(' + letter.upper() + ')', end="")
            
        print()
        print(f'Score: {score} / {total_score}') # To do: turn this into ranks
        return None
    

def active_game(default_wordlist):
    use_honey = False # Default for displaying letters
    words = load_wordlist(default_wordlist)
    # Intro
    print("SPELLING BEE")
    print("------------")
    print("Current word list:", default_wordlist, "To change, type !wordlist <filename>")
    start = input("Type in letters to initialize game: ").lower()
    if start.startswith("!wordlist "):
        filename = start.split(" ", 1)[1]
        try: 
            words = load_wordlist(filename)
            start = input("Type in letters to initialize game: ").lower()
        except FileNotFoundError:
            print("File not found. Using default word list.")
            start = input("Type in letters to initialize game: ").lower()

    letters = ''.join(dict.fromkeys(start))
    if len(letters) == 7: use_honey = True
    print('Available letters:', end=" ")
    for letter in letters:
        print(letter.upper(), end=" ")
    print()

    # Center letter
    print("Chose a center letter:") 
    center_invalid = True
    while center_invalid:
        center_letter = input().lower()
        if center_letter not in letters:
            print("Center letter must be one of the letters you initialized.")
        else:
            center_invalid = False

    # Initialize word list
    valid_words = []
    pangrams = []
    for word in words:
        if len(word) >= 4 and center_letter in word and all(char in letters for char in word):
            valid_words.append(word)
            if all(char in word for char in letters): 
                pangrams.append(word)

    # Determine score
    total_score = 0 
    for word in valid_words:
        if len(word) == 4:
            total_score += 1
        else:
            total_score += len(word) 
            if word in pangrams: total_score += 7 # Bonus points for pangrams

    print('Total points achievable:', total_score, 'including', len(pangrams), 'pangrams.')
    print('Start by typing a word. (For a list of commands type !help)')
    # Game loop
    found_words = []
    score = 0
    while True:
        user_input = input().lower()

        #=== COMANDS ===
        if user_input.lower() == "!help":
            print("!count - Show the number of valid words remaining")
            print("!exit - Exit current game")
            print("!found - Show already found words")
            print("!hints - Show available hint commands")
            print("!pangrams - Show how many pangrams there are")
            print("!ranks - Show the points needed for each rank")
            print("!reveal, !end - Reveal all valid words (ends the game)")
            print("!shuffle - Shuffle the letters")
            
        elif user_input.lower() == "!count":
            print(f"You found {len(found_words)} out of {len(valid_words)} possible words.")

        elif user_input.lower() == "!exit":
            break

        elif user_input.lower() == "!found":
            print("Found words:")
            for word in found_words:
                if word in pangrams:
                    print(word.upper(), end=", ")
                else:
                    print(word, end=", ")
            print()

        # === HINT SECTION ===
        elif user_input.lower() == "!hints":
            print("!pangrams - Show how many pangrams there are. More hints will soon follow!")
        
        elif user_input.lower() == "!pangrams":
            print(f"There are {len(pangrams)} possible pangrams with these letters.")
        # ====================

        elif user_input.lower() == "!ranks": 
            print("Ranks will come in an upcoming version!")

        elif user_input.lower() == "!reveal" or user_input.lower() == "!end":
            print(f"Revealed at {score} / {total_score} points. Valid words were:")
            for word in valid_words:
                if word in found_words:
                    print('✓ ', word.upper())
                else:
                    print(word)
            break

        elif user_input.lower() == "!shuffle":
            l = list(letters)
            random.shuffle(l)
            letters = ''.join(l)

        # === REGULAR GAME ===
        else:
            if user_input in valid_words and user_input not in found_words:
                found_words.append(user_input)
                score += 1 if len(user_input) == 4 else len(user_input)
                if user_input in pangrams:
                    print("*** PANGRAM! *** Amazing!")
                    score += 7
                else:
                    print("Good!")
            elif user_input in found_words:
                print("Already found.")
            else:
                print("Not in word list.")
        
        display_letters(letters, center_letter, score, total_score)

        
while True:

    active_game(default_wordlist)

    print("New game? (y/n)")
    if input().lower() != 'y':
        break


