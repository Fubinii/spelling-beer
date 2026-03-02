import random
import math
from time import sleep
from extra_code import load_words, create_wordlist, provide_start

default_words = 'en_US_60_SB.txt'

def display_letters(letters, center_letter, score, total_score, current_rank, show_score=True, show_ranks=True):
    letters = letters.replace(center_letter, '')
    # Honeycomb display for 7 letters
    if len(letters)+1 == 7:
        letters = letters[:3] + center_letter + letters[3:]
        print(' ', letters[0].upper(), letters[1].upper(), '  |', end=' ')
        if show_ranks:
            print('Rank:', current_rank)
        else:
            print()
        print(letters[2].upper(), '('+letters[3].upper()+')', letters[4].upper(), '|', end=' ')
        if show_score: 
            print(f'Score: {score} / {total_score}') # To do: turn this into ranks
        else:
            print()
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
    

def active_game(default_words):
    use_honey = False # Default for displaying letters
    words = load_words(default_words)
    # Intro
    print("SPELLING BEE")
    print("------------")
    print("Current word list:", default_words, "To change, type !wordlist <filename>")
    
    while True:
        start = input("Type in letters to initialize game or use !generate: ").lower()
        if start.startswith("!wordlist "):
            filename = start.split(" ", 1)[1]
            try: 
                words = load_words(filename)
                print("Word list change successful!")
            except FileNotFoundError:
                print("File not found. Using default word list.")
        elif start == "!generate":
            letters, center_letter, valid_words, pangrams = provide_start(words)
            print('Available letters:')
            display_letters(letters, center_letter, 0, 0, None, show_score=False, show_ranks=False)
            break
        else:
            letters = ''.join(dict.fromkeys(start))
            print("Chose a center letter:") 
            center_invalid = True
            while center_invalid:
                center_letter = input().lower()
                if center_letter not in letters:
                    print("Center letter must be one of the letters you initialized.")
                else:
                    center_invalid = False
            break
    
    valid_words, pangrams = create_wordlist(letters, center_letter, words)

    # Determine score
    total_score = 0 
    for word in valid_words:
        if len(word) == 4:
            total_score += 1
        else:
            total_score += len(word) 
            if word in pangrams: total_score += 7 # Bonus points for pangrams

    print('Total points achievable:', total_score, 'including', len(pangrams), 'pangrams.')
    ranks = {
        math.floor(0.02*total_score): 'Good Start',
        math.floor(0.08*total_score): 'Good',
        math.floor(0.15*total_score): 'Solid',
        math.floor(0.25*total_score): 'Nice',
        math.floor(0.4*total_score): 'Great',
        math.floor(0.5*total_score): 'Amazing',
        math.floor(0.7*total_score): 'Genius',
        total_score: 'Queen Bee'
    }
    current_rank = 'Beginner'

    print('Start by typing a word. (For a list of commands type !help)')
    # Game loop
    found_words = []
    score = 0
    while True:
        user_input = input().lower()

        #=== COMANDS ===
        if user_input == "!help":
            print("!exit - Exit current game")
            print("!found - Show already found words")
            print("!hints - Show available hint commands")
            print("!pangrams - Show how many pangrams there are")
            print("!ranks - Show the points needed for each rank")
            print("!reveal, !end - Reveal all valid words (ends the game)")
            print("!shuffle - Shuffle the letters")
            
        elif user_input == "!exit":
            break

        elif user_input == "!found":
            print("Found words:")
            for word in sorted(found_words):
                if word in pangrams:
                    print(word.upper(), end=", ")
                else:
                    print(word, end=", ")
            print()

        # === HINT SECTION ===
        elif user_input == "!hints":
            print("!pangrams - Show how many pangrams there are. More hints will soon follow!")
        
        elif user_input == "!pangrams":
            print(f"There are {len(pangrams)} possible pangrams with these letters.")
        # ====================

        elif user_input == "!ranks": 
            print("Ranks will come in an upcoming version!")

        elif user_input == "!reveal" or user_input == "!end":
            print(f"Revealed at {score} / {total_score} points. Valid words were:")
            for word in valid_words:
                if word in found_words and word in pangrams:
                    print('✓ ', word.upper())
                elif word in found_words:
                    print('✓ ', word)
                elif word in pangrams:
                    print(word.upper())
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
                    print("*** PANGRAM! ***")
                    score += 7

                else:
                    print("Good!")

                # Rank update    
                for t, r in ranks.items():
                    if score >=  t:
                        current_rank = r
                    elif score < t:
                        break

            elif user_input in found_words:
                print("Already found.")
            else:
                print("Not in word list.")
        
        sleep(0.5) 
        display_letters(letters, center_letter, score, total_score, current_rank) 

        
while True:

    active_game(default_words)

    print("New game? (y/n)")
    if input().lower() != 'y':
        break


