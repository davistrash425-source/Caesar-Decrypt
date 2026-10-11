def shift_char( char, num ):
    # only shift letters, and wrap around the alphabet so Z+1 -> A
    # (spaces/punctuation stay the same so they never turn into control characters)
    if char.isupper() and char.isascii():
        return chr( (ord(char) - ord('A') + num) % 26 + ord('A') )
    if char.islower() and char.isascii():
        return chr( (ord(char) - ord('a') + num) % 26 + ord('a') )
    return char

def encrypt( word,  num ):
    """Encrypts a certain string with the given key
    
    Args: 
        word: the string that the user would like to encrypt
        num: the key that the user would like to encrypt the string by

    Returns:
        encrypted_string: the input string shifted by the key

    """
    encrypted_string = ""
    for char in word:
        encrypted_string += shift_char( char, num )
    return ( encrypted_string )


def decrypt( word, num ):
    """Decrypts word with the given key

    Args:
        word: the string that is going to be decrypted
        num: key to decrypt with

    Returns:
        unencrypted_word: the word shifted back using the given key
    """
    unencrypted_word = ""
    for val in word:
        unencrypted_word += shift_char( val, -num )
    return unencrypted_word

def score( cypher ):

    # takes the cypher and puts it lower case
    cypher = cypher.lower()

    # reset the counts every call, otherwise they pile up across calls
    letters = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        letters[c] = 0

    # adds up all the amount of times each time each letter shows up in the cypher
    for letter in cypher:
        if letter in letters:
            letters[letter] += 1

    # find the frequency of each letter
    freq = findFrequencyPercent( letters )

    # compare the frequency of each letter then average the absolute value
    score = comp_freq(freq)
    return score

def comp_freq( freq ):
    # imports json and the file containing the data the program uses for "standard" english stats
    import json
    with open( "stats.json", "r", encoding="utf-8" ) as file:
        data = json.load(file)

    deviations = {}
    # for each letter, the program subtracts the target frequency by the actual frequency, absolute values it and puts it into an array
    for letter in freq:
        target_freq = data["frequency_percent"][letter]
        real_frequency = freq[letter]
        deviations[letter] = abs( target_freq - real_frequency )
    score = 0
    # the deviations are then added and divided by 26 to find the mean deviation
    for dev in deviations.values():
        score += dev
    return (score/26)


def findFrequencyPercent( letters ):
    total = 0
    frequencies = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequencies[c] = 0

    # all the letters are added up to find the total amount of letters are in the string
    for letter in letters:
        total += letters[letter]

    # If there are no letters, return the array with the zeros, otherwise the program will crash because of 0/0
    if total == 0:
        return frequencies

    # for each letter, it divides the amount of times the letter shows up by the total amount of letters to find the percentage
    for letter in letters:
        frequencies[letter] = ((letters[letter])/total)*100

    return frequencies

def rank_scores( cypher ):
    scores = {}

    # puts all the scores into a dict with the corresponding shift amount
    for shift in range(1,27):
        scores[shift] = score(decrypt(cypher, shift))

    # finds the the shift with the lowest score
    minimum = min( scores, key=scores.get )

    # formatting
    preview_width = 48

    print()
    print( f"{'':3}{'SHIFT':>5}  {'DEVIATION':>10}   MESSAGE" )
    print( "-" * (3 + 5 + 2 + 10 + 3 + preview_width) )

    for i in range (1, 27):
        # keep each preview on one line even if the message has line breaks/tabs
        message = " ".join( decrypt( cypher, i ).split() )
        if len(message) > preview_width:
            message = message[:preview_width - 3] + "..."

        marker = ">>" if i == minimum else ""
        print( f"{marker:<3}{i:>5}  {scores[i]:>9.3f}%   {message}" )

    print()
    print( f"Best match -- shift {minimum} ({scores[minimum]:.3f}% avg deviation):" )
    print()
    print( decrypt( cypher, minimum ) )
    print()

