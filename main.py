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
b_vx = .25
b_vy = 0


# Initialize and begin the application
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
def draw_paddles(window, paddles):
	for paddle in paddles:
		pg.draw.rect(window, "white", (paddle.x, paddle.y, paddle.width, paddle.height))

# Draw the ball on the window
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
		if ny - ball.radius > r_paddle.y and ny + ball.radius < r_paddle.y + r_paddle.height:
			# If the ball's next x is past the left edge of the right paddle
			if nx + ball.radius > r_paddle.x:
				# The objects are colliding
				return True

	# If the ball is moving to the left
	elif ball.vx < 0:
		# If the ball's next y position is in between the left paddle's height
		if ny - ball.radius > l_paddle.y and ny + ball.radius < l_paddle.y + l_paddle.height:
			# If the ball's next x is past the right edge of the left paddle
			if nx - ball.radius < l_paddle.x + l_paddle.width:
				# The objects are colliding
				return True

	# If we get here, the objects are not colliding
	return False

# Determine whether the ball bounces on the top or bottom of the screen
# def collides_screen(ball):



# Start playing the game
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

		# Store the current mouse coordinates
		mouse = pg.mouse.get_pos()

		# Check for events
		for event in pg.event.get():

			if event.type == pg.QUIT:
				running = False
				break

		# Check for collisions with either paddle
		if collides_paddle(ball, l_paddle, r_paddle):
			ball.vx *= -1

		# Check for collisions on the top or bottom of the screen
		# if collides_screen(ball):


		# Update the ball's position and velocity
		x_in_bounds = ball.x - ball.radius > 0 and ball.x + ball.radius < win_width
		y_in_bounds = ball.y - ball.radius > 0 and ball.y + ball.radius < win_height
		if (x_in_bounds and y_in_bounds):
			ball.x += ball.vx
			ball.y += ball.vy

		# Draw all game objects in the frame
		draw_paddles(window, paddles)
		draw_ball(window, ball)

		# Update the window with the new frame
		pg.display.update()

if __name__ == "__main__":
    main()