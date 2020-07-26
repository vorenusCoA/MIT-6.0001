# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>

import math
import random
import string


VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

# Keep track for substitution and repetition
substitutionMade = False
repetitionMade = False


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # The sum of each individual letter
    lettersPoints = 0
    wordLower = word.lower()
    for letter in wordLower:
        lettersPoints += SCRABBLE_LETTER_VALUES[letter]

    multiplier = 7 * len(wordLower) - 3 * (n - len(wordLower))
    if multiplier < 1:
        multiplier = 1

    return lettersPoints * multiplier


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    # The user gets one wildCard allways
    hand['*'] = 1
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    word_lower = word.lower()
    for letter in word_lower:
        if letter in new_hand and new_hand[letter] > 0:
            new_hand[letter] -= 1

    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower()
    if '*' in word_lower:
        # If the word contains the wildcard '*' we should check for 5 possibilities
        # If at least one is correct we return True
        found = False
        for vowel in VOWELS:
            possible_word = word_lower.replace('*', vowel)
            new_hand = hand.copy()
            new_hand[vowel] = new_hand.get(vowel, 0) + 1
            if is_valid_word_helper(possible_word, new_hand, word_list):
                found = True
                break

        return found

    else:
        return is_valid_word_helper(word_lower, hand, word_list)


def is_valid_word_helper(word_lower, hand, word_list):
    # Check if the word is composed of letters in the hand
    word_lower_dict = get_frequency_dict(word_lower)
    for key, value in word_lower_dict.items():
        if (key not in hand or hand[key] < value):
            return False

    # Check if the word is in our list
    found = False
    for wordDB in word_list:
        if wordDB == word_lower:
            found = True
            break

    return found


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for value in hand.values():
        length += value
    return length


def play_hand(hand, word_list, is_a_replay):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      is_a_replay : indicates if the hand is a replay or not
      returns: the total score for the hand
      
    """
    # Keep track of the total score
    totalScore = 0

    numberOfIterations = 0    

    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:

        numberOfIterations += 1        

        # Display the hand
        print("Current hand: ", end="")
        display_hand(hand)
        
        global substitutionMade

        # Ask the user to change a letter (only one time each game)
        if not substitutionMade and numberOfIterations == 1 and not is_a_replay:
            substitute = input("Would you like to substitute a letter? (y/n) ")
            if substitute == "y":
                substitutionMade = True
                letterToReplace = input("Which letter would you like to replace: ")
                # Replace letter
                hand = substitute_hand(hand, letterToReplace)

            # New line
            print()
            # Display the hand
            print("Current hand: ", end="")
            display_hand(hand)

        # Ask user for input
        userInput = input("Enter word, or \"!!\" to indicate that you are finished: ")

        # If the input is two exclamation points:
        if userInput == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(userInput, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                pointsEarned = get_word_score(userInput, calculate_handlen(hand))
                totalScore += pointsEarned
                print("\"" + userInput + "\" earned " + str(pointsEarned) + " points.", end="")
                print("Total: " + str(totalScore) + " points")

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")

            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, userInput)
            # Break line
            print()

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) == 0:
        print("Ran out of letters. ")

    print("Total score for this hand: " + str(totalScore) + " points")

    # Return the total score as result of function
    return totalScore


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # Check if the given letter is in the hand
    # If not, return the hand without changes
    if letter not in hand:
        return hand

    # Choose new letter
    while True:
        # The new letter should be different from user's choice,
        # and should not be any of the letters already in the hand
        new_letter = random.choice(VOWELS + CONSONANTS)
        if new_letter != letter and new_letter not in hand:
            break

    # Copy de hand
    new_hand = hand.copy()
    # Remove old letter and get its number
    qLetters = new_hand.pop(letter)
    # Replace given letter
    new_hand[new_letter] = qLetters

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # Keep track of the total score
    totalScore = 0

    # Asks the user to input the total number of hands
    numberOfHands = int(input("Enter total number of hands: "))

    while numberOfHands > 0:

        # Deal hand
        hand = deal_hand(HAND_SIZE)
        # Play hand and keep score
        handScore = play_hand(hand, word_list, False)

        print("----------")

        global repetitionMade
        # 1 time in the game the user can repeat the hand
        if not repetitionMade:
            repeatHand = input("Would you like to replay the hand? (y/n) ")
            if repeatHand == "y":
                repetitionMade = True
                # Replay the hand
                newScore = play_hand(hand, word_list, True)
                print("----------")
                # The score is the max between the 2 hands played
                handScore = max(handScore, newScore)

        totalScore += handScore
        numberOfHands -= 1

    # Game Over
    print("Total score over all hands: " + str(totalScore))

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
