


import os

from linguistic import getPOS
import random

foundGame = False

greetings = [ "hi", "hello", "hey", "yo", "greetings" ]
greetings_responses = [ "Hi there." , "Greetings human.", "Hello there.", "Hey." ]
balance = [ "balance", "money", "amount" , "bank", "account"]
game = [ "bored", "game", "play", "challenge" ]
yes = [ "yes", "yep", "yeah", "yea", "ya"]
no = ["no", "nah", "nope", "nopes"]
helpfunc = [ "help" ]
bye = ["bye", "goodbye", "goodnight", "adios", "cya", "byebye"]
thanks = ["thanks", "thank"]


# Generates a bot response from a user message
def generateReply(message):
    pos = getPOS(message)
    # If error occurred getting POS
    if not pos:
            return "I am not functioning at the moment. I'll be back soon!"

    # If user greeted
    if pos[0][0].lower() in greetings:
            return random.choice(greetings_responses)

    for e in pos:
        if e[0].lower() in bye:
            return "Bye! See you soon!"

    for e in pos:
        if e[0].lower() in thanks:
            return "You're welcome!"

    for e in pos:
        if e[0].lower() in helpfunc:
            return "You can ask about your bank balance. If you're bored, we can play a game. For technical support you can sclick on the contact button below."

    for e in pos:
        if e[0].lower() in balance:
            return "You will be redirected for signature verification."

    for e in pos:
        if e[0].lower() in game:
            return "Let's play a game. You be the fighter plane, I be the evil bots. You will be redirected to an external window. Proceed?"

    for e in pos:
        if e[0].lower() in yes:
            os.system("python invaders.py")
            return "Hope you enjoyed your game! Up for anything else?"    

    for e in pos:
        if e[0].lower() in no:
            return "Cool, some other time!"

    return "Well, how may I help you?"