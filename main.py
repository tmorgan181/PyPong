# Trenton Morgan 2021
# PyPong

# Pygame module
import pygame as pg

# Game object classes
from paddle import Paddle
from ball import Ball

# Define the window size
win_width = 1000
win_height = 800

# Define paddle size
p_width = win_width/32
p_height = win_height/8

# Paddle offset from the right/left side
p_offset = 50

# Paddle starting positions (top left point)
rp_start = (win_width - (p_offset + p_width), (win_height/2 - p_height/2))
lp_start = ((p_offset + p_width), (win_height/2 - p_height/2))

# Define ball radius
b_radius = 25

# Ball starting position (center point)
b_start = (win_width/2, win_height/2)

# Ball starting velocity
b_vx = .5
b_vy = 0


# Initialize and begin the application
# return: none
def main():
    # Init pg constructor
    pg.init()

    # Create the window
    res = (win_width, win_height)
    window = pg.display.set_mode(res)

    print("Launching application.")

    # Launch the game window
    start_game(window)

# Draw the paddles on the window
# return: none
def draw_paddles(window, paddles):
	for paddle in paddles:
		pg.draw.rect(window, "white", (paddle.x, paddle.y, paddle.width, paddle.height))

# Draw the ball on the window
# return: none
def draw_ball(window, ball):
	pg.draw.circle(window, "white", (ball.x, ball.y), ball.radius)

# Determine whether the ball collides with either paddle
# return: True/False
def collides_paddle(ball, l_paddle, r_paddle):
	# Precalculate the ball's next x and y
	nx = ball.x + ball.vx
	ny = ball.y + ball.vy

	# If the ball is moving to the right
	if ball.vx > 0:
		# If the ball's next y position is in between the right paddle's height
		if ny + ball.radius > r_paddle.y and ny - ball.radius < r_paddle.y + r_paddle.height:
			# If the ball's next x is past the left edge of the right paddle
			if nx + ball.radius > r_paddle.x:
				# The objects are colliding
				return True

	# If the ball is moving to the left
	elif ball.vx < 0:
		# If the ball's next y position is in between the left paddle's height
		if ny + ball.radius > l_paddle.y and ny - ball.radius < l_paddle.y + l_paddle.height:
			# If the ball's next x is past the right edge of the left paddle
			if nx - ball.radius < l_paddle.x + l_paddle.width:
				# The objects are colliding
				return True

	# If we get here, the objects are not colliding
	return False

# Determine whether the ball bounces on the top or bottom of the screen
# def collides_screen(ball):

# Based on its velocity, change the ball's position for the current frame
# return: none
def update_ball_pos(ball):
	x_in_bounds = ball.x - ball.radius > 0 and ball.x + ball.radius < win_width
	y_in_bounds = ball.y - ball.radius > 0 and ball.y + ball.radius < win_height

	# If the ball is in bounds
	if (x_in_bounds and y_in_bounds):
		# Position += velocity
		ball.x += ball.vx
		ball.y += ball.vy
	else:
		# Out of bounds, so replace in center of screen
		ball.x = win_width/2
		ball.y = win_height/2

		# Reverse the x velocity
		ball.vx *= -1


# Check if the cursor is hovering over a paddle
# return: string; which paddle ("l"/"r"/"none") is being hovered
def mouse_on_paddle(l_paddle, r_paddle):
	mx = pg.mouse.get_pos()[0]
	my = pg.mouse.get_pos()[1]

	# Check the left paddle
	if mx > l_paddle.x and mx < l_paddle.x + l_paddle.width:
		if my > l_paddle.y and my < l_paddle.y + l_paddle.height:
			# The mouse is over the left paddle
			return "l"

	# Check the right paddle
	elif mx > r_paddle.x and mx < r_paddle.x + r_paddle.width:
		if my > r_paddle.y and my < r_paddle.y + r_paddle.height:
			# The mouse is over the right paddle
			return "r"

	# The mouse is not over a paddle
	return "none"

# Start playing the game
# return: none
def start_game(window):
	print("Starting the game!")

	# Create game objects with their starting values
	# Paddle(x, y, width, height)
	r_paddle = Paddle(rp_start[0], rp_start[1], p_width, p_height)
	l_paddle = Paddle(lp_start[0], lp_start[1], p_width, p_height)
	paddles = [r_paddle, l_paddle]

	# Ball(x, y, radius, vx, vy)
	ball = Ball(b_start[0], b_start[1], b_radius, b_vx, b_vy)

	### Game Loop ###
	running = True
	while running:
		# Reset the frame
		window.fill("black")

		# Check for events
		for event in pg.event.get():

			# Alt-F4 out
			if event.type == pg.QUIT:
				running = False
				break

			# Check if a paddle is being grabbed
			if event.type == pg.MOUSEBUTTONDOWN:
				# Left mouse button only
				if pg.mouse.get_pressed() == (1, 0, 0):
					which_paddle = mouse_on_paddle(l_paddle, r_paddle)
					if which_paddle == "l":
						# Set the left paddle's flag
						l_paddle.drag = True
					elif which_paddle == "r":
						# Set the right paddle's flag
						r_paddle.drag = True

		# Check for collisions with either paddle
		if collides_paddle(ball, l_paddle, r_paddle):
			# Reverse the x velocity
			ball.vx *= -1

		# Check for collisions on the top or bottom of the screen
		# if collides_screen(ball):


		# Get the mouse's y position
		my = pg.mouse.get_pos()[1]

		# If a paddle is being dragged, center it on the mouse's y coordinate
		if l_paddle.drag:
			l_paddle.y = my - l_paddle.height/2
		elif r_paddle.drag:
			r_paddle.y = my - r_paddle.height/2

		# Check if we should keep dragging
		if pg.mouse.get_pressed() != (1, 0, 0):
			# Mouse is not being pressed anymore
			l_paddle.drag = False
			r_paddle.drag = False

		# Update the ball's position
		update_ball_pos(ball)

		# Draw all game objects in the frame
		draw_paddles(window, paddles)
		draw_ball(window, ball)

		# Update the window with the new frame
		pg.display.update()

if __name__ == "__main__":
    main()