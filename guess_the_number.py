# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui
import math 

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global generated, count
    generated = 0
    count = 0

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global generated, count
    generated = random.randrange(100)
    count = int(math.log(100, 2)) + 1
    print "New Game. Range is from 0 to 100"
    print "Number of remaining guesses is " + str(count)
    print " "

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global generated, count
    generated = random.randrange(1000)
    count = int(math.log(1000, 2)) + 1 
    print "New Game. Range is from 0 to 1000"
    print "Number of remaining guesses is " + str(count)
    print " "
    
def input_guess(guess):
    # main game logic goes here	
    global generated, count 
    if int(guess) > generated and count > 0:
        count -= 1
        print "Guess was " + guess
        print "Number of remaining guesses is " + str(count)
        print "Higher"
        print " "
        
    elif int(guess) < generated and count > 0:
        count -= 1
        print "Guess was " + guess
        print "Number of remaining guesses is " + str(count)
        print "Lower"
        print " "
        
    elif int(guess) == generated and count > 0:
        print "Correct"
     
    else:
        print "You lose"
        new_game()

    
# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_input('Enter a guess', input_guess, 200)
frame.start

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
