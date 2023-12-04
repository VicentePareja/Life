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

	def update_position(self, particles):
		
		total_fx = total_fy = 0
		for particle in particles:
			if self == particle:
				continue

			fx, fy = self.attraction(particle)
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

class Red_particle(Particule):
	def __init__(self, x, y, radius = 5, color = RED, mass=1):
		super().__init__(x, y, radius, color, mass)

	def draw(self, win):
		super().draw(win)

	def update_position(self, planets):
		super().update_position(planets)
	
	def attraction(self, other):

		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = distance_x ** 2 + distance_y ** 2

		force = self.G * self.mass * other.mass / distance
		if force > 10:
			force = 10
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force

		if other.color == BLUE:
			force_x *= -1
			force_y *= -1
		
		if other.color == YELLOW:
			force_x *= -1
			force_y *= -1

		if other.color == RED:
			force_x *= 1
			force_y *= 1

		return force_x, force_y
	
	
class Blue_particle(Particule):
	def __init__(self, x, y, radius = 5, color = BLUE, mass=1):
		super().__init__(x, y, radius, color, mass)

	def draw(self, win):
		super().draw(win)

	def update_position(self, planets):
		super().update_position(planets)
	
	def attraction(self, other):

		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = distance_x ** 2 + distance_y ** 2

		force = self.G * self.mass * other.mass / distance
		if force > 20:
			force = 20
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force

		if other.color == BLUE:
			force_x *= 0
			force_y *= 0
		
		if other.color == YELLOW:
			force_x *= -1
			force_y *= -1

		if other.color == RED:
			force_x *= -1
			force_y *= -1

		return force_x, force_y

class Yellow_particle(Particule):
	def __init__(self, x, y, radius = 5, color = YELLOW, mass=1):
		super().__init__(x, y, radius, color, mass)

	def draw(self, win):
		super().draw(win)

	def update_position(self, planets):
		super().update_position(planets)
	
	def attraction(self, other):

		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = distance_x ** 2 + distance_y ** 2

		force = self.G * self.mass * other.mass / distance
		if force > 20:
			force = 20
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force

		if other.color == BLUE:
			force_x *= 1
			force_y *= 1
		
		if other.color == YELLOW:
			force_x *= 0
			force_y *= 0

		if other.color == RED:
			force_x *= 1
			force_y *= 1

		return force_x, force_y


def create_particules(number, color):
    
	particules = []
    
	for _ in range(number):
		
		x = random.randint(-WIDTH / 2, WIDTH / 2)
		y = random.randint(-HEIGHT / 2, HEIGHT / 2)
		mass = random.randint(1, 4)

		if color == RED:
			particules.append(Red_particle(x, y, mass=mass))

		elif color == BLUE:
			particules.append(Blue_particle(x, y, mass=mass))

		elif color == YELLOW:
			particules.append(Yellow_particle(x, y, mass=mass))

		else:
			print("Error: color not recognized")
        
	return particules

def print_position(particules):
	for particule in particules:
            print(particule.x, particule.y)

def friction(particules):
	for particule in particules:
		particule.x_vel *= 0.99
		particule.y_vel *= 0.99

def main():
	run = True
	clock = pygame.time.Clock()

	particules = create_particules(25, RED)
	particules += create_particules(25, BLUE)
	particules += create_particules(25, YELLOW)
	

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for particule in particules:
			particule.update_position(particules)
			friction(particules)
			particule.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()