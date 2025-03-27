"""
+ Objective:
- Each cell should be a square, same width and height. There should be no cutoffs
- I want to control the number of rows and columns 

In each case, you want the cell size to be fixed. You don't want stuff changing.
From there you can control the width and height of the canvas
"""





# Dimensions
COLS, ROWS  = 25, 25
CELL_SIZE = 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS*CELL_SIZE
CELL_WALL_WIDTH = 1
RANDOM_SEED = 10299302

# In seconds; The maximum i would set this is probably 0.15, anything higher would be annoying.
# Becareful not to set this to like > 5 seconds, because that would leave the program unresponsive.
DELAY = 0.05 

# Colors
YELLOW = (183, 211, 122)
BLACK = (0, 0, 0)
