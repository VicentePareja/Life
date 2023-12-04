import pygame
import math
import random
from parameters import *
pygame.init()


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

FONT = pygame.font.SysFont("comicsans", 16)

class Particule:

	G = G
	TIMESTEP = TIMESTEP

	def __init__(self, x, y, radius = 5, color = RED, mass=1):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.x_vel = 0
		self.y_vel = 0
		self.SCALE = SCALE

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
		pygame.draw.circle(win, self.color, (x, y), self.radius)
	
	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = distance_x ** 2 + distance_y ** 2

		force = self.G * self.mass * other.mass / distance
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		
		total_fx = total_fy = 0
		
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP
		
        if self.y > HEIGHT / 2 or self.y < -HEIGHT / 2:
            self.y_vel *= -1
				
        if self.x > WIDTH / 2 or self.x < -WIDTH / 2:
            self.x_vel *= -1

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP


def create_particules(number):
	
    particules = []
	
    for _ in range(number):
		
        x = random.randint(-WIDTH / 2, WIDTH / 2)
        y = random.randint(-HEIGHT / 2, HEIGHT / 2)
        mass = random.randint(1, 4)
        particules.append(Particule(x, y, mass=mass))
		
    return particules

def print_position(particules):
	for particule in particules:
            print(particule.x, particule.y)

def main():
	run = True
	clock = pygame.time.Clock()

	particules = create_particules(3)
	

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for particule in particules:
			particule.update_position(particules)
			particule.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()