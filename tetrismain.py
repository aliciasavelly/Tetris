from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
	''' Block class:
		Implement a block for a tetris piece
		Attributes: x - type: int
					y - type: int
		specify the position on the tetris board
		in terms of the square grid
	'''

	BLOCK_SIZE = 30
	OUTLINE_WIDTH = 3

	def __init__(self, pos, color):
		self.x = pos.x
		self.y = pos.y
		
		p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
				   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
		p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

		Rectangle.__init__(self, p1, p2)
		self.setWidth(Block.OUTLINE_WIDTH)
		self.setFill(color)

	def can_move(self, board, dx, dy):
		''' Parameters: dx - type: int
						dy - type: int

			Return value: type: bool
						
			checks if the block can move dx squares in the x direction
			and dy squares in the y direction
			Returns True if it can, and False otherwise
			HINT: use the can_move method on the Board object
		'''
		#YOUR CODE HERE
		# print "block can move?"
		return board.can_move(self.x + dx, self.y + dy)

	def move(self, dx, dy):
		''' Parameters: dx - type: int
						dy - type: int
						
			moves the block dx squares in the x direction
			and dy squares in the y direction
		'''

		self.x += dx
		self.y += dy

		Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
	''' Shape class:
		Base class for all the tetris shapes
		Attributes: blocks - type: list - the list of blocks making up the shape
					rotation_dir - type: int - the current rotation direction of the shape
					shift_rotation_dir - type: Boolean - whether or not the shape rotates
	'''

	def __init__(self, coords, color):
		self.blocks = []
		self.rotation_dir = 1
		### A boolean to indicate if a shape shifts rotation direction or not.
		### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
		self.shift_rotation_dir = False
		
		for pos in coords:
			self.blocks.append(Block(pos, color))



	def get_blocks(self):
		'''returns the list of blocks
		'''
		#YOUR CODE HERE
		return self.blocks

	def draw(self, win):
		''' Parameter: win - type: CanvasFrame

			Draws the shape:
			i.e. draws each block
		''' 
		for block in self.blocks:
			block.draw(win)

	def move(self, dx, dy):
		''' Parameters: dx - type: int
						dy - type: int

			moves the shape dx squares in the x direction
			and dy squares in the y direction, i.e.
			moves each of the blocks
		'''
		for block in self.blocks:
			block.move(dx, dy)

	def can_move(self, board, dx, dy):
		''' Parameters: dx - type: int
						dy - type: int

			Return value: type: bool
						
			checks if the shape can move dx squares in the x direction
			and dy squares in the y direction, i.e.
			check if each of the blocks can move
			Returns True if all of them can, and False otherwise
		   
		'''
		
		#YOUR CODE HERE
		# default implementation (MUST CHANGE)
		for block in self.blocks:
			if not block.can_move(board, dx, dy):
				return False
		return True

	
	def get_rotation_dir(self):
		''' Return value: type: int
		
			returns the current rotation direction
		'''
		return self.rotation_dir

	def get_rotate_positions(self, board):

		direction = self.get_rotation_dir()
		new_blocks = []
		temp_blocks = list(self.blocks)
		center_point = temp_blocks.pop(1)

		x = center_point.x
		y = center_point.y

		moving_grid = [Point(x, y), Point(x - 1, y - 1), Point(x, y - 1), Point(x + 1, y - 1), Point(x + 1, y), Point(x + 1, y + 1), Point(x, y + 1), Point(x - 1, y + 1), Point(x - 1, y)]

		for point in temp_blocks:
			for index in range(1, len(moving_grid)):
				newind = None
				if point.x == moving_grid[index].getX() and point.y == moving_grid[index].getY():
					if direction == -1:
						newind = index - 2
					else:
						newind = index + 2

				if newind == -1:
					newind = len(moving_grid) - 2
				elif newind == 0:
					newind = len(moving_grid) - 1
				elif newind == len(moving_grid):
					newind = 1
				elif newind == len(moving_grid) + 1:
					newind = 2


				if not newind == None:
					new_blocks.append(moving_grid[newind])
					break

		new_blocks.insert(1,moving_grid[0])

		return new_blocks

	def can_rotate(self, board):
		''' Parameters: board - type: Board object
			Return value: type : bool
			
			Checks if the shape can be rotated.
			
			1. Get the rotation direction using the get_rotation_dir method
			2. Compute the position of each block after rotation and check if
			the new position is valid
			3. If any of the blocks cannot be moved to their new position,
			return False
						
			otherwise all is good, return True
		'''
		
		#YOUR CODE HERE
		new_blocks = self.get_rotate_positions(board)
		# rotatedir = self.get_rotation_dir()
		# rotatedir = 1
		# print rotatedir
		# center = self.center_block
		for block in new_blocks:
			# block.x = center.x - rotatedir*center.y + rotatedir.block.y
			# block.y = center.y + rotatedir*center.x + rotatedir.block.x
			if not board.can_move(block.getX(), block.getY()):
				IS_OCCUPIED = False
				for est in self.blocks:
					if block.getX() == est.x and block.getY() == est.y:
						IS_OCCUPIED = True
				if not IS_OCCUPIED:
					return False
				# print center.x - rotatedir*center.y + rotatedir*block.y
				# print center.y + rotatedir*center.x + rotatedir*block.x
				# print "block can't rotate"
				# return False
		print "shape can rotate"
		return True



	def rotate(self, board):
		''' Parameters: board - type: Board object

			rotates the shape:
			1. Get the rotation direction using the get_rotation_dir method
			2. Compute the position of each block after rotation
			3. Move the block to the new position
			
		'''    

		####  YOUR CODE HERE #####
		rotated_blocks = self.get_rotate_positions(board)
		for index in range(0, len(rotated_blocks)):
			x = self.blocks[index].x
			y = self.blocks[index].y
			xnew = rotated_blocks[index].getX()
			ynew = rotated_blocks[index].getY()

			self.blocks[index].move(xnew - x, ynew - y)
		# rotatedir = self.get_rotation_dir()
		# center = self.center_block
		# if self.can_rotate(board):
		# 	for block in self.blocks:
		# 		block.move(center.x - rotatedir*center.y + rotatedir*block.y - block.x, center.y + rotatedir*center.x + rotatedir*block.x - block.y)
		# 		"block move"
				# block.draw(board)
		### This should be at the END of your rotate code. 
		### DO NOT touch it. Default behavior is that a piece will only shift

		### rotation direciton after a successful rotation. This ensures that 
		### pieces which switch rotations definitely remain within their 
		### accepted rotation positions.
		if self.shift_rotation_dir:
			self.rotation_dir *= -1

		

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x - 2, center.y),
				  Point(center.x - 1, center.y),
				  Point(center.x    , center.y),
				  Point(center.x + 1, center.y)]
		Shape.__init__(self, coords, 'blue')
		self.shift_rotation_dir = True
		self.center_block = self.blocks[2]

	def get_rotate_positions(self, board):
		#Overriding get_rotate positions because the I_shape doesn't work with the 9-grid scheme

		direction = self.get_rotation_dir() # -1 is counterclockwise, 1 is clockwise
		new_blocks = [] #will hold new blocks
		temp_blocks = list(self.blocks) #a temporary copy of self.blocks, excluding the center piece at index 1

		center_point = temp_blocks.pop(1)

		 #(x,y) is the center of revolution
		x = center_point.x
		y = center_point.y

		
		for point in temp_blocks:
			if point.y == y: #y is equal to the center
				dx = (point.x - x)*direction
				new_blocks.append(Point(x, y + dx))
			elif point.x == x: #x is equal to center
				dy = (point.y - y)*direction #accounts for clockwise or counterclockwise
				new_blocks.append(Point(x + dy, y))

		new_blocks.insert(1,Point(x,y))

		return new_blocks

class J_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x - 1, center.y),
				  Point(center.x    , center.y),
				  Point(center.x + 1, center.y),
				  Point(center.x + 1, center.y + 1)]
		Shape.__init__(self, coords, 'orange')        
		self.center_block = self.blocks[1]

class L_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x - 1, center.y),
				  Point(center.x    , center.y),
				  Point(center.x + 1, center.y),
				  Point(center.x - 1, center.y + 1)]
		Shape.__init__(self, coords, 'cyan')        
		self.center_block = self.blocks[1]


class O_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x    , center.y),
				  Point(center.x - 1, center.y),
				  Point(center.x   , center.y + 1),
				  Point(center.x - 1, center.y + 1)]
		Shape.__init__(self, coords, 'red')
		self.center_block = self.blocks[0]

	def rotate(self, board):
		# Override Shape's rotate method since O_Shape does not rotate
		return 

class S_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x    , center.y),
				  Point(center.x    , center.y + 1),
				  Point(center.x + 1, center.y),
				  Point(center.x - 1, center.y + 1)]
		Shape.__init__(self, coords, 'green')
		self.center_block = self.blocks[0]
		self.shift_rotation_dir = True
		self.rotation_dir = -1


class T_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x - 1, center.y),
				  Point(center.x    , center.y),
				  Point(center.x + 1, center.y),
				  Point(center.x    , center.y + 1)]
		Shape.__init__(self, coords, 'yellow')
		self.center_block = self.blocks[1]


class Z_shape(Shape):
	def __init__(self, center):
		coords = [Point(center.x - 1, center.y),
				  Point(center.x    , center.y), 
				  Point(center.x    , center.y + 1),
				  Point(center.x + 1, center.y + 1)]
		Shape.__init__(self, coords, 'magenta')
		self.center_block = self.blocks[1]
		self.shift_rotation_dir = True
		self.rotation_dir = -1      



############################################################
# BOARD CLASS
############################################################

class Board():
	''' Board class: it represents the Tetris board

		Attributes: width - type:int - width of the board in squares
					height - type:int - height of the board in squares
					canvas - type:CanvasFrame - where the pieces will be drawn
					grid - type:Dictionary - keeps track of the current state of
					the board; stores the blocks for a given position
	'''
	
	def __init__(self, win, width, height):
		self.width = width
		self.height = height

		# create a canvas to draw the tetris shapes on
		self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
										self.height * Block.BLOCK_SIZE)
		self.canvas.setBackground('light gray')

		# create an empty dictionary
		# currently we have no shapes on the board
		self.grid = {}

	def draw_shape(self, shape):
		''' Parameters: shape - type: Shape
			Return value: type: bool

			draws the shape on the board if there is space for it
			and returns True, otherwise it returns False
		'''
		if shape.can_move(self, 0, 0):
			shape.draw(self.canvas)
			return True
		return False

	def can_move(self, x, y):
		''' Parameters: x - type:int
						y - type:int
			Return value: type: bool

			1. check if it is ok to move to square x,y
			if the position is outside of the board boundaries, can't move there
			return False

			2. if there is already a block at that postion, can't move there
			return False

			3. otherwise return True
			
		'''
			
		#YOUR CODE HERE
		return (0 <= x < self.width) and (0 <= y < self.height) and (x, y) not in self.grid

	def add_shape(self, shape):
		''' Parameter: shape - type:Shape
			
			add a shape to the grid, i.e.
			add each block to the grid using its
			(x, y) coordinates as a dictionary key

			Hint: use the get_blocks method on Shape to
			get the list of blocks
			
		'''
		
		#YOUR CODE HERE
		shapeblocks = shape.get_blocks()
		for block in shapeblocks:
			self.grid[(block.x, block.y)] = block
		print self.grid


	def delete_row(self, y):
		''' Parameters: y - type:int

			remove all the blocks in row y
			to remove a block you must remove it from the grid
			and erase it from the screen.
			If you dont remember how to erase a graphics object
			from the screen, take a look at the Graphics Library
			handout
			
		'''
		
		#YOUR CODE HERE
		for x in range(0, self.width):
			if (x, y) in self.grid:
				self.grid[(x, y)].undraw()
				del self.grid[(x, y)]



	
	def is_row_complete(self, y):        
		''' Parameter: y - type: int
			Return value: type: bool

			for each block in row y
			check if there is a block in the grid (use the in operator) 
			if there is one square that is not occupied, return False
			otherwise return True
			
		'''
		
		#YOUR CODE HERE
		count = 0
		for block in self.grid:
			if block[1] == y:
				count += 1
		if count == 10:
			return True
		return False
	
	def move_down_rows(self, y_start):
		''' Parameters: y_start - type:int                        

			for each row from y_start to the top
				for each column
					check if there is a block in the grid
					if there is, remove it from the grid
					and move the block object down on the screen
					and then place it back in the grid in the new position

		'''
		# 18, 17, 16
		#YOUR CODE HERE
		# for x in range(0, self.width):
		# 	for y in reversed(range(0, y_start)):
		# 		movingblock = (x, y)
		# 		if movingblock in self.grid:
		# 			# self.grid[(x, y)].undraw()
		# 			movingblock = self.grid.pop((x, y))
		# 			movingblock.move(0, 1)
		# 			self.grid[(x, y + 1)] = movingblock
		# for k in range(0, y_start):
		# 	y = y_start - k
		# 	for x in range(0, self.width):
		# 		if self.grid.has_key((x,y)):
		# 			#print "(x,y) is", (x,y)
		# 			block = self.grid.pop((x,y)) #removed and saved
		# 			block.move(0, 1)
		# 			self.grid[(x,y+1)] = block

		for n in range(0, y_start):
			y = y_start - n
			for x in range(0, self.width):
				if self.grid.has_key((x, y)):
					popblock = self.grid.pop((x, y))
					popblock.move(0, 1)
					self.grid[(x, y + 1)] = popblock
	
	def remove_complete_rows(self):
		''' removes all the complete rows
			1. for each row, y, 
			2. check if the row is complete
				if it is,
					delete the row
					move all rows down starting at row y - 1

		'''
		
		#YOUR CODE HERE
		for y in range(0, self.height):
			if self.is_row_complete(y):
				self.delete_row(y)
				self.move_down_rows(y - 1)

	def game_over(self):
		''' display "Game Over !!!" message in the center of the board
			HINT: use the Text class from the graphics library
		'''
		
		#YOUR CODE HERE
		self.youlose = Text(Point(self.width * Block.BLOCK_SIZE / 2, self.height * Block.BLOCK_SIZE / 6), "Game over!")
		self.youlose.setFill("black")
		self.youlose.setSize(40)
		self.youlose.draw(self.canvas)
		


############################################################
# TETRIS CLASS
############################################################

class Tetris():
	''' Tetris class: Controls the game play
		Attributes:
			SHAPES - type: list (list of Shape classes)
			DIRECTION - type: dictionary - converts string direction to (dx, dy)
			BOARD_WIDTH - type:int - the width of the board
			BOARD_HEIGHT - type:int - the height of the board
			board - type:Board - the tetris board
			win - type:Window - the window for the tetris game
			delay - type:int - the speed in milliseconds for moving the shapes
			current_shapes - type: Shape - the current moving shape on the board
	'''
	
	SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
	DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1), "space": (0, 1)}
	BOARD_WIDTH = 10
	BOARD_HEIGHT = 20
	
	def __init__(self, win):
		self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
		self.win = win
		self.delay = 1000 #ms

		# sets up the keyboard events
		# when a key is called the method key_pressed will be called
		self.win.bind_all('<Key>', self.key_pressed)

		# set the current shape to a random new shape
		self.current_shape = self.create_new_shape()

		# Draw the current_shape on the board (take a look at the
		# draw_shape method in the Board class)
		####  YOUR CODE HERE ####
		self.board.draw_shape(self.current_shape)

		# For Step 9:  animate the shape!
		####  YOUR CODE HERE ####
		self.animate_shape()


	def create_new_shape(self):
		''' Return value: type: Shape
			
			Create a random new shape that is centered
			 at y = 0 and x = int(self.BOARD_WIDTH/2)
			return the shape
		'''
		
		#YOUR CODE HERE
		# SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
		randomshape = random.randint(0, len(self.SHAPES) - 1)
		return self.SHAPES[randomshape](Point(int(self.BOARD_WIDTH/2), 0))
	
	def animate_shape(self):
		''' animate the shape - move down at equal intervals
			specified by the delay attribute
		'''
		
		self.do_move('Down')
		self.win.after(self.delay, self.animate_shape)
	
	def do_move(self, direction):
		''' Parameters: direction - type: string
			Return value: type: bool

			Move the current shape in the direction specified by the parameter:
			First check if the shape can move. If it can, move it and return True
			Otherwise if the direction we tried to move was 'Down',
			1. add the current shape to the board
			2. remove the completed rows if any 
			3. create a new random shape and set current_shape attribute
			4. If the shape cannot be drawn on the board, display a
			   game over message

			return False

		'''
		
		#YOUR CODE HERE
		dx = self.DIRECTION[direction][0]
		dy = self.DIRECTION[direction][1]
		if self.current_shape.can_move(self.board, dx, dy):
			self.current_shape.move(dx, dy)
			return True
		elif direction == "Down":
			self.board.add_shape(self.current_shape)
			self.board.remove_complete_rows()
			self.current_shape = self.create_new_shape()
			# self.board.draw_shape(self.current_shape)
			# need to add here need to return something??
			if not self.board.draw_shape(self.current_shape):
				self.board.game_over()
			return False
		else:
			return False

		# i want this method to call the key_pressed method so basically it tests to see if it should move / can move and then it references the key_pressed method and moves it through that method and then sets its new current shape
		# need to figure out how to access string that says what it is


		# 	def move(self, dx, dy):
		# ''' Parameters: dx - type: int
		# 				dy - type: int

		# 	moves the shape dx squares in the x direction
		# 	and dy squares in the y direction, i.e.
		# 	moves each of the blocks
		# '''
		# for block in self.blocks:
		# 	block.move(dx, dy)
		

	def do_rotate(self):
		''' Checks if the current_shape can be rotated and
			rotates if it can
		'''
		
		#YOUR CODE HERE
		if self.current_shape.can_rotate(self.board):
			self.current_shape.rotate(self.board)
	
	def key_pressed(self, event):
		''' this function is called when a key is pressed on the keyboard
			it currenly just prints the value of the key

			Modify the function so that if the user presses the arrow keys
			'Left', 'Right' or 'Down', the current_shape will move in
			the appropriate direction

			if the user presses the space bar 'space', the shape will move
			down until it can no longer move and is added to the board

			if the user presses the 'Up' arrow key ,
				the shape should rotate.

		'''
			
		#YOUR CODE HERE
		key = event.keysym
		print key
		# if key == "Left":
		# 	self.current_shape.move(-1, 0)
		# if key == "Right":
		# 	self.current_shape.move(1, 0)
		if key == "Down" or key == "Right" or key == "Left" or key == "space":
			# print self.DIRECTION[key][0]
			# print type(self.DIRECTION[key][0])
			# print self.DIRECTION[key][1]
			self.do_move(key)
			# self.current_shape.move(-1, 0)
		if key == "Up":
			self.do_rotate()
		if key == "space":
			self.do_move(key)
			while self.current_shape.can_move(self.board, 0, 1):
				self.current_shape.move(0, 1)
			self.board.add_shape(self.current_shape)
		# if key == "space":
		# 	self.current_shape.move(0, )
		# add here. need to find a way to tell it to move directly above another block but not sure how yet. look into it

	   
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()