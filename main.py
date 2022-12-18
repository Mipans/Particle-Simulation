import pygame
from math import sqrt
from random import random, randrange
def rand(): return round(200*random()-100)/100
pygame.init()

def sign(number:int): 
    if number != 0: return abs(number)/number
    else: return 0

WIDTH, HEIGHT = (250, 250)
WIN = pygame.display.set_mode((2*WIDTH, 2*HEIGHT))
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

    def __init__(self, xPosition, yPosition, volume, color, coefficients, id):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.volume = volume
        self.color = color
        self.coefficients = coefficients
        self.id = id

        self.xVelocity = 0
        self.yVelocity = 0

    def draw(self):
        x = self.xPosition * self.SCALE + WIDTH - self.volume//2
        y = - self.yPosition * self.SCALE + HEIGHT - self.volume//2

        particleRect = pygame.Rect(x, y, self.volume, self.volume)
        pygame.draw.rect(WIN, self.color, particleRect)

    def attration_repultion(self, other, coefficient):
        xDistance = self.xPosition - other.xPosition
        yDistance = self.yPosition - other.yPosition
        distance = sqrt(xDistance**2 + yDistance**2)

        # calculation of the force
        force = xForce = yForce = 0
        if 2*(self.volume + other.volume) < distance < 80:
            force = coefficient / distance
        elif 0 < distance < 2*(self.volume + other.volume): 
            force = abs(coefficient / distance / 2)
        xForce += force * xDistance
        yForce += force * yDistance
        return xForce, yForce
    
    def update_position(self, all_particles:list):
        totalXForce, totalYForce = 0, 0
        for otherParticle in all_particles:
            if self == otherParticle:
                continue
            
            # getting the correct coefficient
            coefficient = self.coefficients[otherParticle.id]
            
            # calculating the total force for each particle
            xForce, yForce = self.attration_repultion(otherParticle, coefficient)
            totalXForce += xForce
            totalYForce += yForce

        # bouncing off of edges
        if abs(self.xPosition + self.xVelocity * 0.1) > WIDTH:
            self.xVelocity *= -0.99
        if abs(self.yPosition + self.yVelocity * 0.1) > HEIGHT:
            self.yVelocity *= -0.99

        # changing speed based on force
        self.xVelocity += totalXForce * self.TIMESTEP
        self.yVelocity += totalYForce * self.TIMESTEP

        # friction
        self.xVelocity *= 0.99
        self.yVelocity *= 0.99

        # speed cap
        if abs(self.xVelocity) > 75: self.xVelocity = sign(self.xVelocity) * 75
        if abs(self.yVelocity) > 75: self.yVelocity = sign(self.yVelocity) * 75

        # changing position based on speed
        self.xPosition += self.xVelocity * self.TIMESTEP * 0.1
        self.yPosition += self.yVelocity * self.TIMESTEP * 0.1

        # teleporting back in bounds
        if self.xPosition >  (WIDTH - self.volume): self.xPosition = WIDTH - self.volume
        if self.xPosition < -(WIDTH - self.volume): self.xPosition = -WIDTH + self.volume
        if self.yPosition >  (HEIGHT - self.volume): self.yPosition = HEIGHT - self.volume
        if self.yPosition < -(HEIGHT - self.volume): self.yPosition = -HEIGHT + self.volume


def createParticles(quantity, volume, color, coefficients:list, id):
    listOfParticles = list()
    for n in range(quantity):
        randomX = randrange(10 - WIDTH, 10 + WIDTH)
        randomY = randrange(10 - HEIGHT, 10 + HEIGHT)
        listOfParticles.append(Particle(randomX, randomY, volume, color, coefficients, id))
    return listOfParticles


def draw_particles(particles:list):
    WIN.fill(BLK)

    for patricle in particles:
        patricle.draw()

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    
    # x_weights   = [  RED(), WHITE(), GREEN(),  BLUE()]
    red_weights   = [rand(), rand(), rand(), rand()]
    white_weights = [rand(), rand(), rand(), rand()]
    green_weights = [rand(), rand(), rand(), rand()]
    blue_weights  = [rand(), rand(), rand(), rand()]
    #               [rand(), rand(), rand(), rand()]

    all_weights   = [red_weights, white_weights, green_weights, blue_weights]

    def edit(inText:str):
        newText = inText.replace(" 1", " + 1").replace(" 0.", " + 0.").replace(" -", " - ")
        if (len(newText) - newText.find('.', -4)) == 2: newText += "0"
        return newText

    def print_weights():
        print("\n"*10)
        for n in range(len(red_weights)): print(edit(f"RED[{n}]: {red_weights[n]}"))
        print()
        for n in range(len(white_weights)): print(edit(f"WHITE[{n}]: {white_weights[n]}"))
        print()
        for n in range(len(green_weights)): print(edit(f"GREEN[{n}]: {green_weights[n]}"))
        print()
        for n in range(len(blue_weights)): print(edit(f"BLUE[{n}]: {blue_weights[n]}"))
    
    print_weights()

    Red_Particles   = createParticles(125, 4, RED, red_weights, 0)
    White_Particles = createParticles(125, 4, WHT, white_weights, 1)
    Green_Particles = createParticles(125, 4, GRN, green_weights, 2)
    Blue_Particles  = createParticles(125, 4, BLU, blue_weights, 3)

    All_Particles = Red_Particles + White_Particles + Green_Particles + Blue_Particles

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            selectedParticle = input("Which particle do you want to effect? [R/W/G/B] : ")
            if   selectedParticle.capitalize() == "R": selectedParticle = 0
            elif selectedParticle.capitalize() == "W": selectedParticle = 1
            elif selectedParticle.capitalize() == "G": selectedParticle = 2
            elif selectedParticle.capitalize() == "B": selectedParticle = 3
            else: continue
            selectedWeight = input("Which weight do you want to modify? [R/W/G/B] : ")
            if   selectedWeight.capitalize() == "R": selectedWeight = 0
            elif selectedWeight.capitalize() == "W": selectedWeight = 1
            elif selectedWeight.capitalize() == "G": selectedWeight = 2
            elif selectedWeight.capitalize() == "B": selectedWeight = 3
            else: continue
            try: all_weights[selectedParticle][selectedWeight] = round(100*float(input("Enter a weight (float) : ")))/100
            except: continue
            else: print_weights()

        for particle in (All_Particles):
            particle.update_position(All_Particles) 
        draw_particles(All_Particles)

    pygame.quit()


if __name__ == '__main__':
    main()
