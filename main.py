from tools import ( encrypt, decrypt, rank_scores )

# user receives its option and return and integer between 1-4 corresponding to its choice
choice = int(input ( "\noptions:\n  1. encrypt\n  2. decrypt(w/ key)\n  3. decrypt(w/o key)\n" ))

match ( choice ):
    # Encrypt - User enters a string and an integer, the program then returns a string the shifted the user's input by the number they entered
    case 1:
        user_text = input( "Enter text: " )
        user_key = int(input( "Enter number: " ))
        print (encrypt( user_text, user_key ))

    # Decrypt - The user enters a cypher string they would like to decrypt, the program shifts the text back according to the entered key
    case 2:
        user_cypher = input( "Enter cypher: " )
        user_key = int(input( "Enter number: " ))
        print ( decrypt( user_cypher, user_key ) )

    # Real Decryption - all the user enters is the cypher
    case 3:
        user_cypher = input( "Enter cypher: " )
        rank_scores( user_cypher )

    # Error - If the user enters anything but an integer (1-3), they receive the following error
    case _:
        print ( "error: invalid input" )

