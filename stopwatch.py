# template for "Stopwatch: The Game"
import simplegui
# define global variables
count = 0
attempt = 0
win = 0
point = "0/0"
is_running = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    if(t//10 < 60):
        if(t//100 == 0):
            output = "0:0" + str(float(t)/10)
        else:
            output = "0:" + str(float(t)/10)
    else:
        tt = t % 600
        if(tt//100 == 0):
            output = str(t//600) + ":0" + str(float(tt)/10)
        else:
            output = str(t//600) + ":" + str(float(tt)/10)
    return output   
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_watch():
    global is_running
    timer.start()
    is_running = True
def stop_watch():
    global attempt, win, point, is_running
    timer.stop()
    if is_running == True:
        if count % 10 == 0:
            attempt += 1
            win += 1
        else:
            attempt += 1
    point = str(win) + "/" + str(attempt)
    is_running = False
    return point
    
def reset():
    global count, attempt, win, point
    count = 0
    attempt = 0
    win = 0
    point = "0/0"

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(count), [100, 100], 36, "White")
    canvas.draw_text(point, [250, 30], 20, "Green")
    
# create frame
frame = simplegui.create_frame("stop_watch", 300, 200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("start", start_watch, 200)
frame.add_button("stop", stop_watch, 200)
frame.add_button("reset", reset, 200)
timer = simplegui.create_timer(100, tick)
# start frame
frame.start()

# Please remember to review the grading rubric
