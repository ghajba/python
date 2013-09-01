# Game of Life from John Conway
# http://en.wikipedia.org/wiki/Conway's_Game_of_Life
# Created by GHajba
# http://hahamo.wordpress.com

import simplegui
import random
import math

def draw_rect(self, point, width, height, line_width, line_color, fill_color=None):
    point_list = [(point[0], point[1]), (point[0]+width, point[1]), (point[0]+width, point[1]+height), (point[0], point[1]+height)]
    self.draw_polygon(point_list, line_width, line_color, fill_color)
simplegui.Canvas.draw_rect = draw_rect

lines = 60
size = lines**2
grid = [0]*(size)

WIDTH = 10

def init():
    global timer, grid
    timer.stop()
    timer = simplegui.create_timer(500, advance)
    grid = [0]*(size)

def start():
    global timer
    timer.start()

def pause():
    global timer
    timer.stop()
    
def get_neighbours(cell):
    row = cell//lines
    column = cell%lines
    
    if row == 0: # first line
        if column == 0: # first cell
            return grid[cell+1] + grid[lines] + grid[lines+1]
        if column == size-1: # last cell
            return grid[cell-1] + grid[cell+lines] + grid[cell+lines-1]
        return grid[cell-1] + grid[cell+1] + grid[cell+lines] + grid[cell+lines-1] + grid[cell+lines+1]
    if row == lines-1: # last line
        if column == 0: # first cell
            return grid[cell+1] + grid[cell-lines] + grid[cell-lines+1]
        if column == lines-1: # last cell
            return grid[cell-1] + grid[cell-lines] + grid[cell-lines-1]
        return grid[cell-1] + grid[cell+1] + grid[cell-lines] + grid[cell-lines-1] + grid[cell-lines+1]
    if column == 0: # first column
        return grid[cell+1] + grid[cell+lines] + grid[cell+lines+1] + grid[cell-lines] + grid[cell-lines+1]
    if column == lines-1: # last coulumn
        return grid[cell-1] + grid[cell+lines] + grid[cell+lines-1] + grid[cell-lines] + grid[cell-lines-1]
    # else
    return grid[cell-1] + grid[cell+1] + grid[cell+lines] + grid[cell+lines-1] + grid[cell+lines+1] + grid[cell-lines] + grid[cell-lines-1] + grid[cell-lines+1]

def advance():
    """ This method advances the game of life """
    global grid
    new_grid = [0]*(size)
    for i in range(size):
        nb = get_neighbours(i)
        if (grid[i] and nb < 2) or (grid[i] and nb > 3):
            new_grid[i] = 0
        elif nb == 3:
            new_grid[i] = 1
        else:
            new_grid[i] = grid[i]
            
    grid = new_grid
    
def mouse_handler(pos):
    if timer.is_running(): return
    row = (pos[1]-(WIDTH+5))//WIDTH
    cell = ((pos[0]-5)//WIDTH)+row*lines
    if cell < 0 or cell >= size-1: return
    if grid[cell] == 1: grid[cell] = 0
    else: grid[cell] = 1
    
# Handler to draw on canvas
def draw(canvas):
    for i in range(lines+1):
        canvas.draw_line((5+i*WIDTH, WIDTH+5), (5+i*WIDTH, WIDTH+5+lines*WIDTH), 0.2, "Black")
        canvas.draw_line((5, WIDTH+5+i*WIDTH), (5+lines*WIDTH, WIDTH+5+i*WIDTH), 0.2, "Black")
    for i in range(size):
        if grid[i]:
            canvas.draw_rect((5+(i%lines)*WIDTH,WIDTH+5+(i//lines)*WIDTH),WIDTH,WIDTH,1,"Black","Black")
    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Conway's Game of Life", 800, 650)
frame.set_canvas_background("White")
frame.add_button("Start", start)
frame.add_button("Stop", pause)
frame.add_button("Reset", init)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(500, advance)

# Start the frame animation
init()
frame.start()