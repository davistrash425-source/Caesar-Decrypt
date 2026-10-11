import json
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "RandomText.txt"
text = ""
letters = {
    "a": 0,
    "b": 0,
    "c": 0,
    "d": 0,
    "e": 0,
    "f": 0,
    "g": 0,
    "h": 0,
    "i": 0,
    "j": 0,
    "k": 0,
    "l": 0,
    "m": 0,
    "n": 0,
    "o": 0,
    "p": 0,
    "q": 0,
    "r": 0,
    "s": 0,
    "t": 0,
    "u": 0,
    "v": 0,
    "w": 0,
    "x": 0,
    "y": 0,
    "z": 0,
}


with open ( filename, "r", encoding="utf-8" ) as file:
    for line in file:
        text += line.replace(" ","")

text = text.lower()
print ( text )

for letter in text:
    if letter in letters:
        letters[letter] += 1

with open ( "results.txt", "a", encoding="utf-8" ) as file:
    file.write ( json.dumps({"file": filename, "counts": letters}) + "\n" )
