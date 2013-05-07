# Simple Guess the Number game for Python 2.7
# This script can run under previous version of Python, but not with 3 and above
# I'd say this piece of code is copyrighted, but feel free to use it with mentioning my name ;)

from random import randrange
from math import log
import re

#defining global variables
guessed = 0
max_guesses = 0
secret_number = 0
current_range = 0
won = False

def reset_globals(range):
    """ Resets the defined globals for this game """
    global secret_number, max_guesses, guessed, won, current_range
    secret_number = generate_range(0,range)
    max_guesses = int(log(range,2))+1
    guessed = 0
    current_range = range
    won = False
    print "-"*50
    print "A new game started within the range [0,%d)"%range
    print "-"*50

def generate_range(low, high):
    return randrange(low, high)

def handle_game_over():
    """ Prints game over messages according if the player won or not
    then restarts the game"""
    print "-"*50
    print "The game is over."
    if won:
        print "You guessed my secret number %d correct in %d guesses"%(secret_number,guessed)
    else:
        print "You could not guess my secret number %d in %d guesses"%(secret_number,guessed)
    print "-"*50
    reset_globals(current_range)

def handle_guess(guess):
    global guessed, won
    guessed += 1
    
    print "Your guess #%d is: %d"%(guessed,guess) # String formatting
    
    if(guess < secret_number):
        print("My number is higher")
        print "You have %d guesses left\n"%(max_guesses-guessed)
    elif(guess > secret_number):
        print("My number is lower")
        print "You have %d guesses left\n"%(max_guesses-guessed)
    else:
        print "Correct, my number was " + str(secret_number)
        print "You needed %d guesses (and would have %d remaining)"%(guessed,max_guesses-guessed)
        won = True
        handle_game_over()
    
    if guessed == max_guesses and not won:
        won = False
        handle_game_over()

def evaluate_input(user_input):
    if "help" == user_input:
        help()
        return
    if "about" == user_input:
        about()
        return
    if re.compile("^new \d*$").match(user_input):
        game_range = int(re.sub("new ","",user_input))
        if game_range > 0:
            reset_globals(game_range)
            return
    if re.compile("^\d*$").match(user_input):
        handle_guess(int(user_input))
        return
    print "Please enter a valid option."
    help()
    

def play_game():
    """ this function has an endless loop to keep the game going """
    while(True):
        user_input = raw_input("Enter your guess --> ")
        if "exit" == user_input.lower().strip():
            return
        evaluate_input(user_input.lower().strip()) 

def help():
    """ Prints a help for this game """
    print "-"*50
    print "Enter your guess. The computer tells you if its number is lower, higher or same as yours."
    print "You will get the minimal set of guesses to get the right answer."
    print "Enter 'new <maximum>' to start a new game with the secret number between 0 and <maximum> exclusive."
    print "Enter 'exit' if you want to leave the game."
    print "Enter 'help' to display this help dialog."
    print "Enter 'about' to show some credits about this application."
    print "-"*50
    print

def about():
    """ Prints some credit information about this application """
    print "-"*50
    print "'Guess the Number'"
    print "A game by Gabor Laszlo Hajba (c)2013"
    print "The game was developed for Python version 2.7 and will not work with version >= 3"
    print '"Don\'t stand there gawping! Like you\'ve never seen the hand o\' God before!"'
    print "-"*50
    print

def main():
    """ This function contains the main logic for the game """
    about()
    help()
    reset_globals(100)
    play_game()

if __name__ == '__main__':
    main()
