######################################################################
# Implementing a spelling bee game, inspired by the that appears in the New York Times. 
# The purpose of the game is to find as many possible words from 
# a display of 7 letters, where each word must meet the following criteria:
#   1. it must consist of four or more letters; and
#   2. it must contain the central letter of the display.
# So, for example, if the display looks like:
#    T Y
#   B I L
#    M A
# where I is the "central letter," the words "limit" and "tail" are
# legal, but "balmy," "bit," and "iltbma" are not.

from random import choice, randint, sample

######################################################################
# fingerprint(W) takes a word, W, and returns a fingerprint of W
# consisting of an ordered set of the unique character constituents of
# the word. 
def fingerprint(W):
    return(''.join(sorted(set(W))))


######################################################################
# score(W) takes a word, W, and returns how many points the word is
# worth. The scoring rules here are straightforward:
#   1. four letter words are worth 1 point;
#   2. each additional letter adds 1 point up to a max of 9; and
#   3. pangrams (use all 7 letters in display) are worth 10 points.
# So, for example:
#      A L
#     O B Y
#      N E
#   >>> score('ball')
#   1
#   >>> score('balloon')
#   4
#   >>> score('baloney')
#   10     # Pangram!
#
def score(W):
    score = 0                            #Starts off counter with 0
    if len(fingerprint(W))==7:           #Fingerprint function removes duplicates, so 7 distinct characters make a panagram!
        score += 10                      #Since it's a panagram, it adds 10 points to the score
        print("You're on fire! +10")
    elif 4<=len(W)<=12:                  #Length of the word is 4 characters or greater, can be equal to 12 or greater 
        score +=(len(W)-3)
        print("You got it! +", len(W)-3 )
    elif len(W)>12:
        score += 9
        print("Awesome! +9")
    return score                         #Score is returned to be used later for the total running score in the round(D,S) function
######################################################################
# jumble(S, i) takes a string, S, having exactly 7 characters and an
# integer index i where 0<=i<len(S). The string describes a puzzle,
# while i represents the index of S corresponding to the "central"
# character in the puzzle. This function doesn't return anything, but
# rather prints out a randomized representation of the puzzle, with
# S[i] at the center and the remaining characters randomly arrayed
# around S[i]. So, for example:
#    >>> jumble('abelnoy', 1)
#     A L
#    O B Y
#     N E
#    >>> jumble('abelnoy', 1)
#     N Y
#    L B A
#     E O
#
def jumble(S, i):
    S = S.upper()           #String is converted to uppercase 
    M = S[i]                #M is synonymous with the central character in the string
    L = list(S)             #Casting the string as a list allows us to use list operations like indexing and slicing
    L.remove(M)              
    N=sample("".join(L),6)  #Takes a sample from the letters of the usable string
    print("",N[0],N[1])
    print(N[2],M,N[3])
    print("",N[4],N[5])

######################################################################
# readwords(filename) takes the name of a file containing a dictionary
# of English words and returns two values, a dictionary of legal words
# (those having 4 or more characters and fingerprints of 7 or fewer
# characters), with fingerprints as keys and values consisting of sets
# of words with that fingerprint, as well as a list, consisting of all
# of the unique keys of the dictionary having exactly 7 characters (in
# no particular order).
#
def readwords(filename):
    infile = open('words.txt', 'r')
    W = infile.read().split()
    fileSize = []                      #Total number of words read will be stored in this list
    wordsList = []                     #Total number of usable words will be stored in this list
    dictionary = {}                    #The dictionary will be built in this
    for x in W:
        fileSize.append(x)
        if len(x) >= 4 and len(fingerprint(x)) <= 7:
            wordsList.append(x)
    for y in wordsList:
        dictionary[fingerprint(y)] = set()            #All the dictionary keys will be stored in wordsList, turning them into fingerprints here
    for z in wordsList:
        dictionary[fingerprint(z)].add(z)
    uniqueList = [i for i in list(dictionary.keys()) if len(fingerprint(i)) == 7]
    
    print(len(fileSize), "words read:", len(wordsList), "usable;", len(dictionary),"unique fingerprints.")
    print("Welcome to Spelling Bee!")    
    return (dictionary, uniqueList)


######################################################################
# round(D, S) takes two arguments, corresponding to the values
# returned by readwords(), randomly selects a puzzle seed from the
# list S and a central letter from within S. It then shows the puzzle
# and enters a loop where the user can:
#    1. enter a new word for scoring;
#    2. enter / to rescramble and reprint the puzzle;
#    3. enter + for a new puzzle; or
#    4. enter . to end the game.
# When a word is entered, it is checked for length (must be longer
# than 4 characters and its fingerprint must be contained within the
# puzzle seed). The word is then checked against D, and if found, is
# scored and added to the list of words.

def round(D,S):
    Puzzle = choice(S)                #Puzzle is a random puzzle with exactly 7 letters
    i = randint(0,6)                  #"i" randomly generates an integer from 0 to 6 to be the central character
    jumble(Puzzle,i)                  #Calls the jumble function to display a randomized seed
    M = Puzzle[i]                     #M is the central character of the puzzle seed that was randomized
    Z = [x for x in (D.keys()) if set(x)&set(Puzzle)==set(x)]         #Z is a list of all the fingerprints that are in "Puzzle"
    newDictionary=dict((k,D[k]) for k in Z)                           #Creates a smaller dictionary with items that are particularly legal for the current puzzle
    Y = [x for x in newDictionary.values()]                           #Y is a list of all values from newDictionary
    usablewords = set().union(*Y)                                     #A list of all the words that are legal for the current puzzle seed
    totalpoints = []                                                  #Creates a list that collects the user's running total of the score for each round
    guessedwords = []                               #"guessedwords" is assigned an empty list that collects the running total of legal words that the user inputs
    print("Input words, or: '/' = scramble; ':' = show; '+' = new puzzle; '.' = quit") 
    while True:
        x=input("sb>")                                     #Prompts the user to enter things
        if x == ":":
            print("{} words found so far:".format(len(guessedwords)))
            for z in guessedwords:
                print (z)                                  #Prints all the words that were collected in the guessedwords list (words that the user has inputted)  
        elif x == "+":
            print ("You have found {} of {} possible words: you scored {} points!".format(len(guessedwords),len(usablewords),sum(totalpoints)))               
            round(D,S)                                     #Recursively calls the round(D,S) to start a new puzzle
        elif x == "/":
            jumble(Puzzle,i)                               #Scrambles the current puzzle seed, while maintaining the same central character
        elif x == ".":
            print ("You have found {} of {} possible words: you scored {} point(s)!".format(len(guessedwords),len(usablewords),sum(totalpoints)))
            print("Thank you for playing Spelling Bee!")
            exit()                                                          #Ends the round
        else: 
            if len(x)<4:                                                    #Checks and ensures that no words less than 4 characters can be entered
                print("Word is not long enough: must be at least 4 characters!")
            elif set(x) & set(Puzzle) != set(x):                            #Checks and makes sure that all the correct letters are being used
                print("Illegal letter used, Try again!")
            elif set(x) & set(Puzzle) == set(x) and x not in usablewords:   #Checks the dictionary for the legal values and sees if it recognizes the word or not
                print("Unrecognized word. Try again!")            
            else:
                if M not in fingerprint(x):
                    print("Word must include:", (M.upper()))                #Prints a statement that states that the(capitalized) central character is missing
                else:
                    totalpoints.append(score(x))                            #Running total score of all the words that have been guessed, gets appended into list
                    usablewords.remove(x)                                   #Removes from usablewords so that the same word cannot be entered twice
                    guessedwords.append(x)                                  #Every word guessed gets put into the list of guessedwords
######################################################################
# play(filename='words.txt') takes a single optional argument filename
# (defaults to 'words.txt') that gives the name of the file containing
# the dictionary of legal words. After invoking readwords(), it
# repeatedly invokes round() until it obtains a False, indicating the
# game is over.
def play(filename='words.txt'):
    while True:
        D,S = readwords(filename)                    #Sets D and S (the dictionary and list) to words.txt, invokes readwords
        round(D,S)                                   #Invokes round(D,S)
if input() == ".":
     exit()                                   #Allows the rounds to stop looping, and actually ends the game
    

