import pygame
from math import sqrt, atan2, cos, sin
import random
pygame.init()

WIDTH, HEIGHT = (1500, 775)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Particle:
    SCALE = 1
    TIMESTEP = 1

    def __init__(self, xPosition, yPosition, volume, color):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.volume = volume
        self.color = color

        self.xVelocity = 0
        self.yVelocity = 0

    def draw(self):
        x = self.xPosition * self.SCALE + WIDTH // 2 - self.volume//2
        y = - self.yPosition * self.SCALE + WIDTH // 2 - self.volume//2

        particleRect = pygame.Rect(x, y, self.volume, self.volume)
        pygame.draw.rect(WIN, self.color, particleRect)

    def attration_repultion(self, other):
        if self.color == other.color: coefficient = -1
        else: coefficient = 1

        xDistance = self.xPosition - other.xPosition
        yDistance = self.yPosition - other.yPosition
        distance = sqrt(xDistance**2 + yDistance**2)

        force = coefficient / distance**2
        angle = atan2(yDistance, xDistance)
        xForce = force * cos(angle)
        yForce = force * sin(angle)
        return xForce, yForce


def createParticles(quantity, volume, color):
    listOfParticles = list()
    for n in range(quantity):
        randomX = random.randrange(-WIDTH//2, WIDTH//2)
        randomY = random.randrange(0, HEIGHT)
        listOfParticles.append(Particle(randomX, randomY, volume, color))
    return listOfParticles


def draw_particles(particle_lists:list):
    WIN.fill(BLACK)

    for particles in particle_lists:
        for patricle in particles:
            patricle.draw()

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    Yellow_Particles = createParticles(10, 10, YELLOW)
    White_Particles = createParticles(200, 2, WHITE)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False

        draw_particles([Yellow_Particles, White_Particles])

    pygame.quit()


if __name__ == '__main__':
    main()
