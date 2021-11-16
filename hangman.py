# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:
# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

from numpy import mat

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.") # IT'S OVER 9000!
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    return all(elem in letters_guessed for elem in secret_word)

def get_guessed_word(secret_word, letters_guessed):
    res = ''
    for letter in secret_word:
        if letter in letters_guessed:
            res += letter + ' '
        else:
            res += '_ '
    return res[:-1]

def get_available_letters(letters_guessed):
    res = ''
    for letter in string.ascii_lowercase:
      if letter not in letters_guessed:
        res += letter
    return res
    
def hangman(secret_word):
    guesses_left = 6
    attempts = 3
    letters_guessed = []
    vowels = ['a','e','i','o','u']
    print('\nHangman the game!!')
    print(f'Current word length is {len(secret_word)}')
    while not is_word_guessed(secret_word,letters_guessed) and guesses_left != 0:
        print('Progress:',get_guessed_word(secret_word,letters_guessed))
        print(f'You have {guesses_left} guesses left')
        print(f'Available letters are: {get_available_letters(letters_guessed)}')
        print('-'*30)
        print('\nChoose 1 letter from available ones')
        letter = input('Your choice: ').lower()
        while letter not in [*string.ascii_lowercase] or letter in letters_guessed:
            if guesses_left == 1:
                guesses_left -= 1
                break
            if letter in letters_guessed:
                print("You've already choosed this letter, try another one")
            elif attempts >= 1 and letter not in [*string.ascii_lowercase]:
                    attempts -= 1
                    print(f'\nIncorrect character, try again')
                    print('you have {0} more attempts to choose a correct one without losing a guess'.format(attempts if attempts in [1,2] else 'no'))
            else:
                if letter in vowels:
                    if guesses_left > 1:
                        guesses_left -= 2
                    else:
                        guesses_left = 0
                        break
                else:
                    guesses_left -= 1
                print("\nIncorrect character, try again")
                print(f"You have {guesses_left} guesses left")
            print('-'*30)
            letter = input('Your choice: ').lower()
        if guesses_left == 0:
            break
        else:
            if letter in secret_word:
                print('\nThe letter is in the word!')
            else:
                print("\nThe letter isn't in the word")
                guesses_left = guesses_left - 2 if letter in vowels else guesses_left - 1
            letters_guessed += letter
    if guesses_left == 0:
        print(f'You lost the game, the word was {secret_word}')
    else:
        print(f'Congrats! You won the game, the word was {secret_word}')
        print(f'Your final score is {(guesses_left)*len(set(secret_word))}')

def match_with_gaps(my_word, other_word):
    my_word = [elem for elem in my_word if not elem.isspace()]
    return len(other_word) == len(my_word) and all((my_word.count(char) == other_word.count(char)) for char in my_word if char != '_') and all(my_word[i] == other_word[i] or my_word[i] == "_" for i in range(len(my_word)))

# added second parameter to filter words without any already choosed but false letters
def show_possible_matches(my_word,letters_guessed):
    res = []
    for word in wordlist:
        if match_with_gaps(my_word,word) and all(char in [*get_available_letters(letters_guessed),*[char for char in my_word if char not in ["_"," "]]] for char in word):
            res.append(word)
    return res

def hangman_with_hints(secret_word):
    guesses_left = 6
    attempts = 3
    letters_guessed = []
    vowels = ['a','e','i','o','u']
    print('\nHangman the game!! (hints enabled)')
    print(f'Current word length is {len(secret_word)}')
    while not is_word_guessed(secret_word,letters_guessed) and guesses_left != 0:
        print('Progress:',get_guessed_word(secret_word,letters_guessed))
        print(f'You have {guesses_left} guesses left')
        print(f'Available letters are: {get_available_letters(letters_guessed)}')
        print('\nChoose 1 letter from available ones')
        print('-'*30)
        letter = input('Your choice: ').lower()
        while letter not in [*string.ascii_lowercase,'*'] or letter in letters_guessed:
            if guesses_left == 1:
                guesses_left -= 1
                break
            if letter in letters_guessed:
                print("You've already choosed this letter, try another one")
            elif attempts >= 1 and letter not in [*string.ascii_lowercase]:
                    attempts -= 1
                    print(f'\nIncorrect character, try again')
                    print('you have {0} more attempts to choose a correct one without losing a guess'.format(attempts if attempts in [1,2] else 'no'))
            else:
                guesses_left -= 1
                print("\nIncorrect character, try again")
                print(f"You have {guesses_left} guesses left")
            print('-'*30)
            letter = input('Your choice: ').lower()
        if guesses_left == 0:
            break
        else:
            if letter == '*':
                print('\nPossible words:\n',*show_possible_matches(get_guessed_word(secret_word,letters_guessed),letters_guessed),'\n')
            elif letter in secret_word:
                print('-'*30)
                print('The letter is in the word!')
                letters_guessed += letter
            else:
                print("The letter isn't in the word")
                guesses_left = guesses_left - 2 if letter in vowels else guesses_left - 1
                letters_guessed += letter
    if guesses_left == 0:
        print(f'You lost the game, the word was: {secret_word.upper()}')
    else:
        print(f'Congrats! You won the game, the word was: {secret_word.upper()}')
        print(f'Your final score is {(guesses_left)*len(set(secret_word))}')

if __name__ == "__main__":
    # pass
    print('-'*30)
    print('Choose the version of the game:')
    print('1 - classic hangman')
    print('2 - hangman with hints')
    secret_word = choose_word(wordlist)
    print('-'*30);hangman(secret_word) if int(input()) == 1 else print('-'*30);hangman_with_hints(secret_word)
    
