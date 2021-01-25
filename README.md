# sudoku
Sudoku game with a visualized solve process and a GUI to play with.

solve.py is the standalone solve algorithm
board.py is in charge of storing and operating on playing boards
square.py is just the class that represents 1 of 9 squares in a board
gui.py is the actualy code that allows a player to play the soduku game and interact with the board as well as observe the process of how a board is solved.

Below are the controls:
Click on a cell to select it
While selecting a cell, type a number to jot it down as note in that cell, it will show as a light green number
While selecting a cell with a number put in as a note, press Enter to check whether this number is the solution or not
While selecting a cell with a number put in as a note, press Delete to remove the note from the board
At any point, press Space Bar to watch the board get solved

If a note is entered into the board incorrectly, the player will receive a strike, 3 strikes will lose the game and terminate the program
