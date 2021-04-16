class Paddle():
	def __init__(self, x, y, width, height):
	    self.x = x
	    self.y = y
	    self.width = width
	    self.height = height

	    # If the paddle is being dragged
	    self.drag = False