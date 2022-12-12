import pygame
from math import sqrt, atan2, cos, sin
import random
pygame.init()

def sign(number:int): 
    if number != 0: return abs(number)/number
    else: return 0

WIDTH, HEIGHT = (400, 400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

FPS = 60
BLK = (0, 0, 0)
WHT = (255, 255, 255)
YLW = (255, 255, 0)
RED = (255, 100, 50)
GRN = (100, 255, 50)
BLU = (100, 100, 255)


class Particle:
    SCALE = 1
    TIMESTEP = 1

    def __init__(self, xPosition, yPosition, volume, color, coefficients):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.volume = volume
        self.color = color
        self.coefficients = coefficients

        self.xVelocity = 0
        self.yVelocity = 0

    def draw(self):
        x = self.xPosition * self.SCALE + WIDTH // 2 - self.volume//2
        y = - self.yPosition * self.SCALE + HEIGHT // 2 - self.volume//2

        particleRect = pygame.Rect(x, y, self.volume, self.volume)
        pygame.draw.rect(WIN, self.color, particleRect)

    def attration_repultion(self, other, coefficient):
        xDistance = self.xPosition - other.xPosition
        yDistance = self.yPosition - other.yPosition
        distance = sqrt(xDistance**2 + yDistance**2)

        force = xForce = yForce = 0
        if 5 < distance < 80:
            force = coefficient / distance
        elif 0 < distance < 5: 
            force = -0.1 * abs(coefficient / distance)
        xForce += force * xDistance
        yForce += force * yDistance
        return xForce, yForce
    
    def update_position(self, all_particles:list):
        totalXForce, totalYForce = 0, 0
        for otherParticle in all_particles:
            if self == otherParticle:
                continue
            
            for otherColor in self.coefficients:
                if otherColor[0] == otherParticle.color:
                    coefficient = otherColor[1]
                    break

            xForce, yForce = self.attration_repultion(otherParticle, coefficient)
            totalXForce += xForce
            totalYForce += yForce

        if abs(self.xPosition) > WIDTH // 2:
            self.xVelocity *= -0.99
        if abs(self.yPosition) > HEIGHT // 2:
            self.yVelocity *= -0.99

        self.xVelocity += totalXForce * self.TIMESTEP
        self.yVelocity += totalYForce * self.TIMESTEP

        self.xVelocity *= 0.99
        self.yVelocity *= 0.99

        if abs(self.xVelocity) > 75: self.xVelocity = sign(self.xVelocity) * 75
        if abs(self.yVelocity) > 75: self.yVelocity = sign(self.yVelocity) * 75

        self.xPosition += self.xVelocity * self.TIMESTEP * 0.1
        self.yPosition += self.yVelocity * self.TIMESTEP * 0.1


def createParticles(quantity, volume, color, coefficients:list):
    listOfParticles = list()
    for n in range(quantity):
        randomX = random.randrange(-WIDTH//2 + 10, WIDTH//2 - 10)
        randomY = random.randrange(-HEIGHT//2 + 10, HEIGHT//2 - 10)
        listOfParticles.append(Particle(randomX, randomY, volume, color, coefficients))
    return listOfParticles


def draw_particles(particles:list):
    WIN.fill(BLK)

    for patricle in particles:
        patricle.draw()

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    Red_Particles   = createParticles(100, 4, RED, [(RED, -0.63), (WHT, +0.65), (GRN, -0.31), (BLU, -0.31)])
    White_Particles = createParticles(100, 4, WHT, [(RED,  0.00), (WHT, -0.20), (GRN, -0.44), (BLU, +0.68)])
    Green_Particles = createParticles(100, 4, GRN, [(RED, +0.96), (WHT, -0.56), (GRN, +0.60), (BLU, +0.37)])
    Blue_Particles  = createParticles(100, 4, BLU, [(RED, -0.10), (WHT, -0.49), (GRN, +1.00), (BLU, +1.00)])

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False

        All_Particles = Red_Particles + White_Particles + Green_Particles + Blue_Particles
        for particle in (All_Particles):
            particle.update_position(All_Particles) 
        draw_particles(All_Particles)

    pygame.quit()


if __name__ == '__main__':
    main()
