import pygame
import sys
from random import randint
from particle import Particle

# Screen dimensions
width, height = 1200, 800
trail_intensity = 0.95 # [0.0 -> 1.0]

# list of particles
particles = []

def setup_particles():
    for i in range(40):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(5,45))
        p.set_bounds(width, height)
        init_speed = 12
        p.vx = randint(-init_speed,init_speed)
        p.vy = randint(-init_speed,init_speed)
        particles.append(p)


def main_loop():
    # Main game loop
    clock = pygame.time.Clock()

    fill_color = trail_intensity*255.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen black

        screen.fill( (fill_color,fill_color,fill_color, 254), special_flags=pygame.BLEND_RGBA_MULT )

        dt = clock.tick()
        dt /= 75 # slow the sim down
        # print(dt)

        # Update particle positions and apply gravity
        for particle in particles:
            for other in particles:
                if particle != other:
                    particle.apply_gravity(other)
            particle.update(dt)

        # Draw the particle
        for particle in reversed(particles):
            # cleanup time
            if not particle.active:
                # cull out any inactive
                particles.remove(  particle )
                continue
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y),), particle.radius)
            pygame.draw.circle(screen, (255,255,100,50), (int(particle.x + randint(-2,2) + particle.radius/3), int(particle.y)+randint(-3,3) , ), particle.radius/2)
                

        # Update the screen
        pygame.display.update()

def main():
    # Initialize Pygame
    pygame.init()

    # screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particle Sim")

    setup_particles()

    main_loop()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
