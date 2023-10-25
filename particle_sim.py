import pygame
import sys
from random import randint
from particle import Particle
from pygrid import PyGrid
import physics

# Screen dimensions
width, height = 1024, 512
trail_intensity = 0.95 # [0.0 -> 1.0]
global grid
grid_size = 2**3

def setup_grid():
    global grid
    grid = PyGrid(grid_size,grid_size)

    # add a bunch of particles to the grid
    num_particles=300
    global trail_intensity
    trail_intensity = 0
    for i in range(num_particles):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(2,10))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 12
        p.vx = randint(-init_speed,init_speed)
        # p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)

    # put a big ball in middle
    # TODO: if radius is bigger than the grid the physics won't work
    radius = width/20.0
    p = Particle(width/2.5, height-radius, radius)
    p.radius = radius
    p.mass = 9999999
    print('big ball', p.__dict__)
    grid.add_particle(p)


    info = {
            'name': 'hit floor',
            'function': physics.bounce, 
            'arguments': {width, height, 0.9555555},
            'interact_with_other_particles': False, 
            'check_neighbor_cells': True
            }
    grid.add_physics(info) 

    info = {
            'name': 'interact with one another',
            'function': physics.collision_bounce, #physics., combine_collision
            'arguments': {},
            'interact_with_other_particles': True,
            'check_neighbor_cells': False
            }
    grid.add_physics(info)

    info = {
            'name': 'drop down',
            'function': physics.downforce, 
            'arguments': { 0.1 },
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 


def main_loop():

    global grid
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
        dt /= 75 # slow the sim down (found by trail and error)

        # Apply physics and then update the particles location
        grid.apply_physics()
        grid.update(dt)

        # Draw the particle
        for particle in reversed(grid.get_all_particles()):
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y),), particle.radius)
            # pygame.draw.circle(screen, (255,255,100,50), (int(particle.x + randint(-2,2) + particle.radius/3), int(particle.y)+randint(-3,3) , ), particle.radius/2)
                

        # Update the screen
        pygame.display.update()

def main():
    # Initialize Pygame
    pygame.init()

    global screen
    screen = pygame.display.set_mode((width, height)) #  pygame.FULLSCREEN
    
    # screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particle Sim")

    setup_grid()

    main_loop()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
