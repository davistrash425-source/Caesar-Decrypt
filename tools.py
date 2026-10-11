import json

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
    unencrypted_word = ""
    for val in word:
        unencrypted_word += shift_char( val, -num )
    return unencrypted_word

def brute_force( word ):
    for i in range(26):
        print( str(i + 1 ) + ": " + decrypt( word, i + 1 ) )

with open( "stats.json", "r", encoding="utf-8" ) as file:
    data = json.load(file)

def score( cypher ):
    cypher = cypher.lower()

    # reset the counts every call, otherwise they pile up across calls
    letters = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        letters[c] = 0

    for letter in cypher:
        if letter in letters:
            letters[letter] += 1

    # find the frequency of each letter
    freq = findFrequencyPercent( letters )

    # compare the frequency of each letter then average the absolute value
    score = comp_freq(freq)
    return score

def comp_freq( freq ):
    deviations = {}
    for letter in freq:
        target_freq = data["frequency_percent"][letter]
        real_frequency = freq[letter]
        deviations[letter] = abs( target_freq - real_frequency )
    score = 0
    for dev in deviations.values():
        score += dev
    return (score/26)


def findFrequencyPercent( letters ):
    total = 0
    frequencies = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequencies[c] = 0

    for letter in letters:
        total += letters[letter]

    if total == 0:
        return frequencies

    for letter in letters:
        frequencies[letter] = ((letters[letter])/total)*100

    return frequencies

def rank_scores( cypher ):
    scores = {}

    for shift in range(1,27):
        scores[shift] = score(decrypt(cypher, shift))

    minimum = min( scores, key=scores.get )

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

