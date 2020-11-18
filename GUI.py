import pygame
import datetime
import time
from Solver import  *
from pygame.locals import *


# Solver contains a Grid class where all functions are in and where 4x4, 9x9, 16x16 boards are in as Grid.board...

# Create the sudoku; format = (boardNxN, N, N)
#sudoku = Grid(Grid.board4x4, 4, 4)
sudoku = Grid()
#sudoku = Grid(Grid.board16x16, 16, 16)

# Initiate pygame
pygame.init()


class GUI(object):
	""" Creates the user interface. You have to input which Grid.boardNxN you want to solve)"""

	def __init__(self, board, rows, columns):

		self.board = board
		self.rows = rows
		self.columns = columns

		# Squares
		self.width = 50
		self.color = (0,0,0)

		# Grid of squares to input numbers in
		self.lattice =  []
		for row in range(self.rows):
			self.lattice.append([])
			for column in range(self.columns):
				self.lattice[row].append((self.width/2 + column * self.width, self.width/2 + row * self.width, self.width, self.width))		# (x,y,width,height)
				
		# Window
		self.screen_width = self.width * (self.columns +1)
		self.screen_height = self.width * (self.rows +1)
		self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
	

	# Creates the lattice of square objects
	def matrix(self):
		for row in range(self.rows):
			for column in range(self.columns):
				pygame.draw.rect(self.win, self.color, self.lattice[row][column], 2)

	# Draw initial numbers from the sudoku
	def drawNumber(self):

		numberFont = pygame.font.SysFont('Papyrus', 40, True)
		
		for row in range(self.rows):
			for column in range(self.columns):
				if self.board[row][column] != 0:
					if self.rows == 16:
						numberFont = pygame.font.SysFont('Papyrus', 25, True)
						numberText = numberFont.render(str(self.board[row][column]), 1, (0,0,0))
						self.win.blit(numberText, (self.lattice[row][column][0] + 12, self.lattice[row][column][1] + 2))
					else:
						numberText = numberFont.render(str(self.board[row][column]), 1, (0,0,0))
						self.win.blit(numberText, (self.lattice[row][column][0] + 12, self.lattice[row][column][1] - 7))
	# Resets the grid
	def reset(self):
		if len(self.board) == 4:
			self.board = np.array([
									[2,1,0,0],
									[0,3,2,0],
									[0,0,0,4],
									[1,0,0,0]])
		if len(self.board) == 9:
			self.board = np.array([  
									[5, 3, 0, 0, 7, 0, 0, 0, 0],
									[6, 0, 0, 1, 9, 5, 0, 0, 0],
									[0, 9, 8, 0, 0, 0, 0, 6, 0],
									[8, 0, 0, 0, 6, 0, 0, 0, 3],
									[4, 0, 0, 8, 0, 3, 0, 0, 1],
									[7, 0, 0, 0, 2, 0, 0, 0, 6],
									[0, 6, 0, 0, 0, 0, 2, 8, 0],
									[0, 0, 0, 4, 1, 9, 0, 0, 5],
									[0, 0, 0, 0, 8, 0, 0, 7, 9]])
		if len(self.board) == 16:
			self.board = np.array([
									[0, 11, 9, 0, 0, 16, 13, 4, 0, 0, 14, 0, 10, 6, 15, 0],
									[4, 12, 15, 0, 3, 6, 0, 11, 0, 5, 0, 1, 16, 7, 14, 2],
									[1, 0, 6, 0, 15, 2, 0, 0, 11, 9, 10, 0, 0, 0, 8, 0],
									[0, 13, 0, 0, 0, 1, 0, 0, 4, 6, 0, 15, 0, 0, 0, 0],
									[0, 0, 0, 0, 0, 0, 15, 0, 8, 1, 5, 3, 0, 4, 11, 7],
									[6, 0, 1, 0, 0, 12, 8, 0, 9, 0, 0, 2, 0, 0, 3, 0],
									[14, 0, 4, 13, 6, 0, 0, 3, 0, 12, 7, 10, 8, 0, 2, 0],
									[3, 8, 0, 0, 4, 7, 2, 0, 6, 0, 0, 0, 0, 12, 16, 5],
									[13, 0, 0, 16, 0, 8, 14, 10, 3, 4, 15, 0, 12, 5, 1, 11],
									[0, 0, 0, 6, 2, 0, 0, 1, 10, 0 , 11, 0, 15, 3, 0, 9],
									[7, 0, 0, 12, 0, 4, 0, 15, 5, 0, 9, 14, 0, 0, 0, 0],
									[10, 0, 0, 8, 0, 0, 11, 0, 0, 0, 1, 12, 4, 0, 13, 16],
									[0, 0, 0, 0, 0, 0, 7, 0, 15, 2, 0, 0, 0, 0, 12, 3],
									[0, 0, 7, 0, 0, 10, 6, 0, 1, 8, 0, 13, 11, 0, 9, 14],
									[8, 6, 5, 0, 0, 3, 0, 0, 14, 0, 0, 9, 0, 0, 0, 0],
									[0, 16, 0, 2, 0, 0, 0, 14, 0, 10, 0, 0, 0, 0, 0, 0]])
		redrawScreen()

	# Insert the number into the square if it fits
	def insertNumber(self):
		
		mx, my = pygame.mouse.get_pos()

		# Enable inputting numbers
		for row in range(len(self.lattice)):
			for column in range(len(self.lattice[row])):

				# Position check
				if mx > self.lattice[row][column][0] and mx < self.lattice[row][column][0] + self.lattice[row][column][2]:
					if my > self.lattice[row][column][1] and my < self.lattice[row][column][1] + self.lattice[row][column][3]:

						# Show location
						print("Row", row+1, "and column ", column+1)
						# Mark as the square you're manipulating
						pygame.draw.rect(self.win, (255,0,0), self.lattice[row][column])
						redrawScreen()

						# Clear the queue to wait for the input
						pygame.event.clear()

						inserting = True
						while inserting:
							# Wait for the input
							event = pygame.event.wait()
							if event.type == pygame.QUIT:
								pygame.quit()

							keys =  [48+1,48+2,48+3,48+4,48+5,48+6,48+7,48+8,48+9] #Key 1 K_1 is K_1 = 49 and so on...
							if event.type == KEYDOWN:

								for key in keys:
									if event.key == key:
										number = key - 48
										get_solution = Grid.get_solution(self, number, (row+1, column+1))
										if get_solution:
											
											# Insert the number
											self.board[row][column] = number
											print(number, "inserted in row ", row+1, "and column", column+1)
											# Reset the square
											pygame.draw.rect(self.win, self.color, self.lattice[row][column], 2)
											# Draws the updated sudoku
											redrawScreen()
											inserting = False
											# Clear the queue to wait for the input
											pygame.event.clear()
										else:
											print("Wrong!", number, "doesn't fit in row ", row+1, "and column", column+1)		#if Grid.get_solution(number, (row+1, column+1)): #row, column are indices here						
											# Reset the square
											pygame.draw.rect(self.win, self.color, self.lattice[row][column], 2)
											inserting = False
											# Clear the queue to wait for the input
											pygame.event.clear()
						
		#print(self.lattice)
	def solve(self):

		# All positions
		for row in range(1, self.rows + 1):
			for column in range(1, self.columns + 1):

				# Input only when the place is 0
				if self.board[row-1][column-1] == 0:
					
					# Try all numbers
					for number in range(1, self.rows + 1):

						# Pauses to see the process
						#time.sleep(0.00001)
	
						# Try getting a solution for the position
						get_solution = Grid.get_solution(self, number, (row, column))

						# Checks if solution exists
						if get_solution:
							
							# Inputs the solution (number)
							self.board[row-1][column-1] = number
							
							# Count number of tries that numbers have been inputted
							# global i
							# i += 1
							# if i % 100 == 0:
							# 	print(i)

							# Draws the updated sudoku						# SLOWER BUT shows algorithm working
							redrawScreen()

							# Calls recursion and goes back from the beginning of the (row)	for loop
							GUI.solve()

							# If no solution is found
							self.board[row-1][column-1] = 0

					return

		# Draws the updated sudoku											# faster and doesn't show the process
		redrawScreen()
		# Solved - stop program
		pygame.event.clear()
		while True:
			# Wait for the input
		    event = pygame.event.wait()
		    if event.type == pygame.QUIT:
		    	pygame.quit()


# Display time of playing
def timer():
	time_f = datetime.datetime.now()
	delta = time_f - time_i
	timePlaying = str(delta).split(".")[0]
	# Create font
	timerFont = pygame.font.SysFont('Papyrus', 20, True)
	# Display text
	timerText = timerFont.render(timePlaying, 1, (0,0,0))
	GUI.win.blit(timerText, (GUI.screen_width - GUI.width/2 - timerText.get_width(), GUI.screen_height - GUI.width/2 -4))

# Update screen
def redrawScreen():
	GUI.win.fill((255,255,255))

	# Draw the matrix
	GUI.matrix()

	# Draw numbers
	GUI.drawNumber()

	# Timer
	timer()
	
	# Update the display
	pygame.display.update()



# Declare which board do you want to play (4x4, 9x9, 16x16)
GUI = GUI(sudoku.board, sudoku.rows, sudoku.columns)


		########################		########################		########################		########################		########################

# Main loop
run = True
fps = 60
clock = pygame.time.Clock()
time_i = datetime.datetime.now()

# Count how many numbers have been inputed (optional under GUI.solve())
i = 0

while run:
	clock.tick(fps)
	
	# i += 1
	# print(i)
	
	# If i click on keys it sends a command that the key was/is pressed
	keys = pygame.key.get_pressed()
	
	# Enables closing the window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		# Insert the number into the sudoku
		if event.type == pygame.MOUSEBUTTONDOWN:
			GUI.insertNumber()

	# Reset the board
	if keys[pygame.K_ESCAPE]:
		GUI.reset()

	# Solve using a backtracking algorithm
	if keys[pygame.K_SPACE]:
		GUI.reset()
		GUI.solve()
		
	

	# If solved; exit


	# Redraw the window	
	redrawScreen()



