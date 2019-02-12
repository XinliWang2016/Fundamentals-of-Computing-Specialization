# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global l3, state, text1_pos, text2_pos, equal, click 
    l1 = range(0, 8)
    l2 = range(0, 8)
    l3 = l1 + l2
    random.shuffle(l3)
    state = 0
    text1_pos = -1
    text2_pos = -1
    equal = {}
    click = 0
    label.set_text("Turns = " + str(click))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global text1_pos, text2_pos, state, equal, click
    
    if state == 0:
        state = 1
        text1_pos = list(pos)[0] // 50

    elif state == 1:
        state = 2
        text2_pos = list(pos)[0] // 50
        if(l3[text1_pos] == l3[text2_pos] and text1_pos != text2_pos):
            equal[text1_pos] = l3[text1_pos]
            equal[text2_pos] = l3[text2_pos]
        if (text2_pos not in equal.keys() and text1_pos != text2_pos):
            click += 1
            label.set_text("Turns = " + str(click))
    else:
        state = 1
        text1_pos = list(pos)[0] // 50
       
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global l3, text1_pos, text2_pos, equal
    for i in range(0, 16):
        canvas.draw_line([50 * (i + 1), 0], [50 * (i + 1), 100], 1, "White")
    if(equal != {}):
        for key, value in equal.items():
            canvas.draw_line([25 + 50 * key , 0], [25 + 50 * key, 100], 50, "Black")
            canvas.draw_text(str(value), [12 + 50 * key , 65], 50, "White")
    if state == 1:
        canvas.draw_line([25 + 50 * text1_pos, 0], [25 + 50 * text1_pos, 100], 50, "Black")
        canvas.draw_text(str(l3[text1_pos]), [12 + 50 * text1_pos , 65], 50, "White")
    elif state == 2:
        canvas.draw_line([25 + 50 * text1_pos, 0], [25 + 50 * text1_pos, 100], 50, "Black")
        canvas.draw_line([25 + 50 * text2_pos, 0], [25 + 50 * text2_pos, 100], 50, "Black")
        canvas.draw_text(str(l3[text1_pos]), [12 + 50 * text1_pos , 65], 50, "White")
        canvas.draw_text(str(l3[text2_pos]), [12 + 50 * text2_pos , 65], 50, "White")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background("Green")
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric