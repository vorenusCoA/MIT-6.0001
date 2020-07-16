import random
import string

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
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for secretLetter in secret_word:
        found = False
        for guessedLetter in letters_guessed:
            if secretLetter == guessedLetter:
                found = True
                break
        if not found:
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ""
    for secretLetter in secret_word:
        found = False
        for guessedLetter in letters_guessed:
            if secretLetter == guessedLetter:
                guessed_word += secretLetter
                found = True
                break
        if not found:
            guessed_word += "_ "

    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    result = ""
    for letter in string.ascii_lowercase:
        found = False
        for guessedLetter in letters_guessed:
            if letter == guessedLetter:
                found = True
                break
        if not found:
            result += letter

    return result


def is_letter_in_word(letter, word):
    for char in word:
        if letter == char:
            return True
    return False


def calculate_score(numberOfGuesses, secret_word):
    letters_set = set(secret_word)
    return len(letters_set) * numberOfGuesses


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Welcome the user
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("You have 3 warnings left.")

    numberOfGuesses = 6
    numberOfWarnings = 3
    available_letters = string.ascii_lowercase
    letters_guessed = ""

    # Game loop
    won = False
    while numberOfGuesses > 0:    

        # Separate each guess
        print("------------")

        print("You have " + str(numberOfGuesses) + " guesses left.")
        print("Available letters: " + available_letters)

        # Promp the user for input a char (we assume the user inputs only 1 char)
        user_input = str.lower(input("Please guess a letter: "))

        # Validate input
        if not user_input.isalpha():
            numberOfWarnings -= 1
            print("Oops! That is not a valid letter.", end="")
            if numberOfWarnings >= 0:
                print(" You have " + str(numberOfWarnings) + " warnings left: ", end="")
            else:
                print(" You have no warnings left so you lose one guess:", end="")
                numberOfGuesses -= 1

            print(get_guessed_word(secret_word, letters_guessed))
            continue

        # At this point we know the user wrote a valid char

        # Check previous guesses
        if user_input in letters_guessed:
            numberOfWarnings -= 1
            print("Oops! You've already guessed that letter.", end="")
            if numberOfWarnings >= 0:
                print(" You have " + str(numberOfWarnings) + " warnings left: ", end="")
            else:
                print(" You don´t have more warnings so you lose a guess: ", end="")
                numberOfGuesses -= 1

            print(get_guessed_word(secret_word, letters_guessed))
            continue
                
        # Add the input to the guesses and take it from the available ones    
        letters_guessed += user_input
        available_letters = available_letters.replace(user_input, "")

        # Check if the letter is in the secret word        
        if is_letter_in_word(user_input, secret_word):
            print("Good guess: ", end="")
        else:
            if user_input in "aeiou":
                numberOfGuesses -= 2
            else:
                numberOfGuesses -= 1
            print("Oops! That letter is not in my word: ", end="")

        # Print the current state of the word
        print(get_guessed_word(secret_word, letters_guessed))

        if is_word_guessed(secret_word, letters_guessed):
            won = True
            break;

    print("------------")

    if won:
        print("Congratulations, you won!")
        score = calculate_score(numberOfGuesses, secret_word)
        print("Your total score for this game is: " + str(score))
    else:
        print("Sorry, you ran out of guesses. The word was " + secret_word)


if __name__ == "__main__":
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)
