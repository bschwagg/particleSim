import pygame
import sys
import inspect
from random import randint
from particle import Particle
import configs


def main_loop():

    # late import of the grid.
    # TODO: make the grid a singleton object
    from configs import grid, trail_intensity
    
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
        # TODO: abstract drawing out
        for particle in reversed(grid.get_all_particles()):
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y),), particle.radius)
            # pygame.draw.circle(screen, (255,255,100,50), (int(particle.x + randint(-2,2) + particle.radius/3), int(particle.y)+randint(-3,3) , ), particle.radius/2)
        
        # Update the screen
        pygame.display.update()


def parse_arg_to_config_func():
    funcs = inspect.getmembers(configs, inspect.isfunction)
    if len(sys.argv) != 2:
        print("Please provide one of the following scenarios:")
        for f in funcs:
            name, func = f
            print(name)
        sys.exit()

    # get the function reference from the user argument given
    setup_func = None
    for f in funcs:
        name, func = f
        if name == sys.argv[1]:
            setup_func = func
            break
    else:
        print('invalid scenario given')
        sys.exit()
    return setup_func

def main():

    setup_func = parse_arg_to_config_func()

    # Initialize Pygame
    pygame.init()

    global screen
    screen = pygame.display.set_mode((configs.width, configs.height)) #  pygame.FULLSCREEN
    
    # screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particle Sim")

    setup_func()

    main_loop()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
