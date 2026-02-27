import random

def provide_start(words):
    found_letters = False

    while not found_letters:
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        letters = []

        v1 = random.choice(vowels)
        vowels.replace(v1,'')
        letters.append(v1)

        v2 = random.choice(vowels)
        vowels.replace(v2, '')
        letters.append(v2)

        vc = random.choice(vowels+consonants)
        if vc in consonants: consonants.replace(vc, '')

        letters.append(vc)

        for i in range(4):
            c = random.choice(consonants)
            consonants.replace(c,'')
            letters.append(c)

        if 'q' in letters and not 'u' in letters: 
            qu_check = False
        else:
            qu_check = True
        
        center_letter = random.choice(letters)

        if qu_check:
            valid_words = []
            pangrams = []
            for word in words:
                if len(word) >= 4 and center_letter in word and all(char in letters for char in word):
                    valid_words.append(word)
                    if all(char in word for char in letters): 
                        pangrams.append(word)
            
            if len(pangrams) != 0: found_letters = True
    random.shuffle(letters)
    letters_string = ''.join(letters)

    return letters_string, center_letter, valid_words, pangrams

# Testing section
# def load_wordlist(default_wordlist):
#     with open(default_wordlist) as dic:
#         words = [w.strip() for w in dic if w.strip()]
#     return words

# letters, center_letter, _, pangrams = provide_start(load_wordlist('en_US_60_SB.txt'))   

# print(letters, 'with cl', center_letter, pangrams)



