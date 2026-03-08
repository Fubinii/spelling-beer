import random
import math
from time import sleep
from extra_code import load_words, create_wordlist, provide_start, word_score
from display import display_letters

default_words = 'en_US_60_SB.txt'

def active_game(default_words):
    use_honey = False # Default for displaying letters
    words = load_words(default_words)
    # Intro
    print("SPELLING BEE(R)")
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
            display_letters(letters, center_letter, 0, None, show_score=False, show_ranks=False)
            break
        else:
            letters = ''.join(dict.fromkeys(start))
            print('Available letters:', end=' ')
            for letter in letters:
                print(letter.upper(), end=' ')
            print()
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
    total_score = sum(word_score(word, pangrams) for word in valid_words)
    

    print('Total points achievable:', total_score, 'including', len(pangrams), 'pangrams.')

    ranks = [
        (math.floor(0.05*total_score), 'Moving Up'),
        (math.floor(0.08*total_score), 'Good'),
        (math.floor(0.15*total_score), 'Solid'),
        (math.floor(0.25*total_score), 'Nice'),
        (math.floor(0.4*total_score), 'Great'),
        (math.floor(0.5*total_score), 'Amazing'),
        (math.floor(0.7*total_score), 'Genius'),
        (total_score, 'Queen Bee')
    ]
    current_rank = 'Beginner'

    print('Start by typing a word. (For a list of commands type !help)')
    # Game loop
    found_words = set()
    score = 0

    # Creating Command dispatch
    def command_help():
        print("!exit - Exit current game")
        print("!found - Show already found words")
        print("!hints - Show available hint commands")
        print("!pangrams - Show how many pangrams there are")
        print("!ranks - Show the points needed for each rank")
        print("!reveal, !end - Reveal all valid words (ends the game)")
        print("!shuffle - Shuffle the letters")

        return None
    
    def command_exit():
        return 'break'
    
    def command_found(found_words, pangrams):
        print("Found words:")
        for word in sorted(found_words):
            if word in pangrams:
                print(word.upper(), end=", ")
            else:
                print(word, end=", ")
        print()
        return None
    
    def command_hints():
        print("!pangrams - Show how many pangrams there are. More hints will soon follow!")
        return None
    
    def command_pangrams(pangrams):
        print(f"There are {len(pangrams)} possible pangrams with these letters.")
        return None
    
    def command_ranks(ranks):
        for t, r in ranks:
            print(f"{r}: {t} points")
        return None
    
    def command_reveal(score, total_score, valid_words, found_words, pangrams):
        print(f"Revealed at {score} / {total_score} points. Valid words were:")
        for word in sorted(valid_words):
            if word in found_words and word in pangrams:
                print('✓ ', word.upper())
            elif word in found_words:
                print('✓ ', word)
            elif word in pangrams:
                print(word.upper())
            else:
                print(word)
        return 'break'
    
    def command_shuffle(letters):
        l = list(letters)
        random.shuffle(l)
        return ''.join(l)
    
    handle_command = {
        "!help": lambda: command_help(),
        "!exit": lambda: command_exit(),
        "!found": lambda: command_found(found_words, pangrams),
        "!hints": lambda: command_hints(),
        "!pangrams": lambda: command_pangrams(pangrams),
        "!ranks": lambda: command_ranks(ranks),
        "!reveal": lambda: command_reveal(score, total_score, valid_words, found_words, pangrams),
        "!end": lambda: command_reveal(score, total_score, valid_words, found_words, pangrams),
        "!shuffle": lambda: command_shuffle(letters)
    }
            
    while True:
        user_input = input().lower()

        command = handle_command.get(user_input)
        if command:
            result = command()
            if result == 'break':
                break
            elif user_input == "!shuffle":
                letters = result

        # === REGULAR GAME ===
        else:
            if user_input in valid_words and user_input not in found_words:
                found_words.add(user_input)
                score += word_score(user_input, pangrams)
                if user_input in pangrams:
                    print("*** PANGRAM! ***")
                else:
                    print("Good!")

                # Rank update    
                current_rank = next(
                (r for t, r in reversed(ranks) if score >= t), 'Beginner')

            elif user_input in found_words:
                print("Already found.")
            else:
                print("Not in word list.")
        
        sleep(0.5) 
        display_letters(letters, center_letter, score, current_rank) 

        
while True:

    active_game(default_words)

    print("New game? (y/n)")
    if input().lower() != 'y':
        break

