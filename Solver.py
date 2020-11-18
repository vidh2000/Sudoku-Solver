import numpy as np 



# Class not needed.. Functions only would satisfy
class Grid():

	# Possible sudokus you can use
	board4x4 = np.array([
		[2,1,0,0],
		[0,3,2,0],
		[0,0,0,4],
		[1,0,0,0]])

	board9x9 = np.array([  
		[5, 3, 0, 0, 7, 0, 0, 0, 0],
		[6, 0, 0, 1, 9, 5, 0, 0, 0],
		[0, 9, 8, 0, 0, 0, 0, 6, 0],
		[8, 0, 0, 0, 6, 0, 0, 0, 3],
		[4, 0, 0, 8, 0, 3, 0, 0, 1],
		[7, 0, 0, 0, 2, 0, 0, 0, 6],
		[0, 6, 0, 0, 0, 0, 2, 8, 0],
		[0, 0, 0, 4, 1, 9, 0, 0, 5],
		[0, 0, 0, 0, 8, 0, 0, 7, 9]])

	board16x16 = np.array([
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

	def __init__(self, board = board9x9, rows = 9, columns = 9):
		"""n-D matrix"""
		self.rows = rows
		self.columns = columns
		self.solved = False
		self.board = board
		
	def position(position):
		""" Returns index of each position in grid
			(position = (row, column))"""	
		y0 = position[0] -1
		x0 = position[1] -1
		return y0, x0

	### Functions checking if number is used ###

	def is_inRow(self, number, position):
		""" Checks if certain row already has the number inputed
			(number to check, (row, column))"""

		place = Grid.position(position)
		for x in range(0, self.columns):
	
			if self.board[place[0]][x] == number:
				return True #print(f"{number} already in column:", x+1)

	def is_inColumn(self, number, position):
		""" Checks if certain column already has the number inputed
			(number to check, (row, column)) """

		place = Grid.position(position)
		for y in range(0, self.columns):
			
			if self.board[y][place[1]] == number:
				return True #, print(f"{number} already in row:", y +1)

	def is_inSquare(self, number, position):
		""" Checks if certain square already has the number inputed
			(number to check, (row, column)) """

		place = Grid.position(position)
		for y in range(0, int(np.sqrt(self.rows))):
			for x in range(0, int(np.sqrt(self.columns))):

				if self.board[int(place[0]//  np.sqrt(self.rows)*  np.sqrt(self.rows) + y)][int(place[1]// np.sqrt(self.columns) * np.sqrt(self.columns) + x)] == number:
						return True #, print(f'{number} already in this square: in row {int(place[0]//  np.sqrt(self.rows)*  np.sqrt(self.rows) + y +1)} and column {int(place[1]// np.sqrt(self.columns) * np.sqrt(self.columns) + x +1)}') 



	def get_solution(self, number, position):
		""" Checks if number can be inputed
			(number to check, (row, column)) """
		
		# Checks the row
		in_row = Grid.is_inRow(self, number, position)
		# Checks the column
		in_column = Grid.is_inColumn(self, number, position)
		# Checks the square
		in_square = Grid.is_inSquare(self, number, position)
		
		if (in_row or in_column) or in_square:
			return False
		
		else:
			return True

	# Backtracking algorithm which solves the sudoku		
	def solve(self):

		# All positions
		for row in range(1, self.rows + 1):
			for column in range(1, self.columns + 1):

				# Input only when the place is 0
				if self.board[row-1][column-1] == 0:
					
					# Try all numbers
					for number in range(1, self.rows + 1):

						# Try getting a solution for the position
						get_solution = Grid.get_solution(self, number, (row, column))

						# Checks if solution exists
						if get_solution:
							
							# Inputs the solution (number)
							self.board[row-1][column-1] = number

							# Calls recursion and goes back from the beginning of the (row)	for loop
							Grid.solve(self)

							# If no solution is found
							self.board[row-1][column-1] = 0

					return
		
		print("Solved Sudoku:")
		print(np.matrix(self.board))

# sudoku4x4 = Grid(Grid.board4x4, 4, 4)
# print("Sudoku 4x4:")
# print(np.matrix(Grid.board4x4))
# sol4x4 = sudoku4x4.solve()

# sudoku9x9 = Grid(Grid.board9x9)
# print("Sudoku 9x9:")
# print(np.matrix(Grid.board9x9))
# sol9x9 = sudoku9x9.solve()

# sudoku16x16 = Grid(Grid.board16x16, 16, 16)
# print("Sudoku 16x16:")
# print(np.matrix(Grid.board16x16))
# sol16x16 = sudoku16x16.solve()

