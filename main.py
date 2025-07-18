import pygame
import math
import time

from fontcontroller import FontController
from rendertext import RenderText

def main():
	pygame.display.init()
	
	screen_size = 400
	screen_midpoint = screen_size // 2
	screen = pygame.display.set_mode((screen_size,screen_size))
	orange = (245, 167, 66)

	lerp = lambda x,y,z: x + (y-x) * z

	font_controller = FontController()

	secondtext = RenderText(font_controller, orange, "black")
	secondtext.update_x(screen_midpoint)
	secondtext.update_y(screen_midpoint)

	# Make the size of the parts of the widget tangential to the window size
	wid_size = screen_size // 10
	smpoint = (screen_midpoint,screen_midpoint)
	startpoint = math.hypot(smpoint[0],smpoint[1])
	endpoint = math.hypot(smpoint[0] + wid_size,smpoint[1] + wid_size)
	orange_circle_rad = abs(startpoint - endpoint) * 0.6

	twopi = math.pi * 2
	fraction = 0.02
	start = math.pi / 2
	seconds = 10
	ctr = 0
	for i in range(seconds, -1, -1):
		# Draw the background and background circle
		screen.fill("black")
		pygame.draw.circle(screen, "white", smpoint, wid_size)

		# Render the 'slice of pi' that consumes ctr/seconds percent of the whole circle
		lp = lerp(start,start + twopi,ctr/seconds)
		# Use a granular fraction that can render contiguous lines from 0 to twopi * (ctr / seconds) radians
		j = start
		while j < lp:
			# Calculate the angle of the end point of the line being drawn
			endpoint_x = math.cos(j)
			endpoint_y = math.sin(j) * -1

			# Move the x,y points from the origin to screen space
			cx = endpoint_x * wid_size + screen_midpoint
			cy = endpoint_y * wid_size + screen_midpoint

			pygame.draw.line(screen, orange, smpoint, (cx, cy), 2)
			j += fraction

		# Render the circle covering up the 'slice of pi' orange circle
		# This gives the illusion of a curved bar/line filling up with orange over time
		# Radius os this circle is 60% of the radius of the 'slice of pi' orange circle
		pygame.draw.circle(screen, "black", smpoint, orange_circle_rad)

		# Render the seconds as a text box to the middle of the circle
		secondtext.update_text(str(0 if i < 0 else i))
		secondtext.draw(screen)

		# Draw/show the contents of the draw buffer
		pygame.display.flip()
		time.sleep(1)
		ctr += 1

	pygame.display.quit()

if __name__ == "__main__":
	main()
