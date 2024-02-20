import numpy as np
import pygame
import math
from random import randint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 1/120 #delta time 1/FPS

# particle class
class Particle:
    acc = pygame.Vector2(0,0)
    vel = pygame.Vector2(0,0)
    pos = pygame.Vector2(0,0)
    def __init__(self, mass, radius, velocity, position):
        self.mass = mass
        self.radius = radius
        self.vel = velocity
        self.pos = position

# init particles
noParticles = 200
particles = []
size = 1

for i in range(noParticles):
    p = Particle(8000, size, pygame.Vector2(0,0), pygame.Vector2(randint(200,1000), randint(200, 600)))
    particles.append(p)

p = Particle(160000, 3, pygame.Vector2(0,0), pygame.Vector2(screen.get_width()/2, screen.get_height()/2))
particles.append(p)

prevpos = [pygame.Vector2(0,0)] * len(particles) #vector used to store the previous position of each particle

# continous collision detection
def box_collision(p1, i):
    if p1.pos.x + p1.radius >= screen.get_width():
        if p1.pos.x - prevpos[i].x:
            tc = (screen.get_width() - p1.radius - prevpos[i].x)/(p1.pos.x - prevpos[i].x)
            p1.pos = tc*p1.pos + (1-tc)*prevpos[i]
        p1.vel.x = -p1.vel.x
    if p1.pos.x - p1.radius <= 0:
        if p1.pos.x - prevpos[i].x:
            tc = (p1.radius - prevpos[i].x)/(p1.pos.x - prevpos[i].x)
            p1.pos = tc*p1.pos + (1-tc)*prevpos[i]
        p1.vel.x = -p1.vel.x
    if p1.pos.y + p1.radius >= screen.get_height():
        if p1.pos.y - prevpos[i].y:
            tc = (screen.get_height() - p1.radius - prevpos[i].y)/(p1.pos.y - prevpos[i].y)
            p1.pos = tc*p1.pos + (1-tc)*prevpos[i]
        p1.vel.y = -p1.vel.y
    if p1.pos.y - p1.radius <= 0:
        if p1.pos.y - prevpos[i].y:
            tc = (p1.radius - prevpos[i].y)/(p1.pos.y - prevpos[i].y)
            p1.pos = tc*p1.pos + (1-tc)*prevpos[i]
        p1.vel.y = -p1.vel.y

def acc_update():
    for i in range(len(particles)):
        p1 = particles[i]
        pos1 = p1.pos
        for j in range(len(particles)):
            if i != j:
                p2 = particles[j]
                radius = max(p1.radius, p2.radius)
                pos2 = p2.pos
                m2 = p2.mass
                r = pos2 - pos1
                mag = r.x*r.x + r.y*r.y
                if math.sqrt(mag) > radius:
                    mag_sq = max(math.sqrt(r.x*r.x + r.y*r.y),0.01)
                    acc = (m2/(mag_sq*mag))*r
                    p1.acc += acc


while running:
	# poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("darkblue")

    # draw the particle
    for p in particles:
        pygame.draw.circle(screen, "yellow", p.pos, p.radius)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # acceleration update
    acc_update()

    # box collision
    for p, i in zip(particles, range(len(particles))):
        prevpos[i].x = p.pos.x
        prevpos[i].y = p.pos.y
        p.vel += p.acc*dt
        p.pos += p.vel*dt
        p.acc = pygame.Vector2(0,0)
        box_collision(p, i)

    # limits FPS to 120
    clock.tick(120)
pygame.quit()