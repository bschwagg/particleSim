import pygame
import sys
import time
from particle import Particle


def is_pow2(num):
    return bin(num).count("1") == 1

class PyGrid:
    '''
    Given a pygame screen
    this divides up the screen into a grid 
    which is more manageble for collision detection
    '''
    def __init__(self, x, y):
        w, h = pygame.display.get_surface().get_size()
        if not is_pow2(x) or not is_pow2(y) or not is_pow2(w) or not is_pow2(h):
            print('Error: PyGrid y and x and screen size need to be a power of two')
            sys.exit()

        self.y = y
        self.x = x
        self.x_len = int(w/x)
        self.y_len = int(h/y)
        self.x_shift = self.x_len.bit_length()-1
        self.y_shift = self.y_len.bit_length()-1
        # hash map from key to (x,y)
        self.grid = {}

        # a list of functions to simulate physics to run
        self.physics = []


    def get_key(self, x, y):
        return int(x) >> self.x_shift , int(y) >> self.y_shift


    def add_particle(self, particle):
        key =  self.get_key(particle.x, particle.y)
        cell = self.grid.get(key, [])
        cell.append(particle)
        self.grid[key] = cell


    def get_neighboring_cell_particles(self, cell):
        key, particle_list = cell
        x,y = key
        cells_adj = [(x-1,y-1),(x,y-1),(x+1,y-1),
                     (x-1,y  ), (x,y), (x+1,y  ),
                     (x-1,y+1),(x,y+1),(x+1,y+1)
                     ]
        cells_adj = [self.grid[(a,b)] for (a,b) in cells_adj
                        if a>=0 and b>=0 and a<self.x and b<self.y and (a,b) in self.grid ]
        # get a list of all the particles
        all_particles = []
        for other in cells_adj:
            all_particles.extend( other )
        return all_particles


    def get_all_particles(self):
        ret = []
        for cell in self.grid.items():
            key, particle_list = cell
            ret.extend(particle_list)
        return ret


    def remove(self, key, particle):
        cell = self.grid[key]
        cell.remove(particle)


    def add_physics(self, dict_obj):
        print(f'adding physics: {dict_obj["name"]}')
        self.physics.append( dict_obj )
        #TODO: check all needed keys are present


    def apply_physics(self):
        for cell in self.grid.items():
            key, particle_list = cell
            x,y=key

            for physics in self.physics:
                if physics['check_neighbor_cells'] == True:
                    particle_list = self.get_neighboring_cell_particles(cell)
                # run physics
                for particle in particle_list:
                    if not physics['interact_with_other_particles']:
                        physics['function']( particle, *physics['arguments'] )
                    else:
                        for other in particle_list:
                            physics['function']( particle, other, *physics['arguments'] )


    def update(self, dt):
        for cell in list(self.grid.items() ):
            key, particle_list = cell

            remove_list = []
            for particle in reversed(particle_list):

                # tag for removal if not active 
                if not particle.active:
                    remove_list.append( (key, particle) )
                    self.remove(key, particle)
                    continue

                particle.update(dt)

                # check if particle moved to a new cell
                new_key = self.get_key(particle.x, particle.y)
                if new_key != key:
                    particle_list.remove(particle)
                    self.add_particle(particle)


if __name__ == "__main__":

    print("View the grid for testing")
    pygame.init()
    screen = pygame.display.set_mode( (1024, 512) )

    pygame.display.set_caption("Grid")

    grid_size = 2**3
    grid = PyGrid(grid_size,grid_size)

    print( grid.__dict__ )

    # dump in some particles
    for x in range(0,1024,10):
        for y in range(0,512,10):
            p = Particle(x,y, 0)
            grid.add_particle(p)
    # print( grid.__dict__ )

    # print results
    screen.fill( (255,255,255) )
    for cell in grid.grid:
        for particle in grid.grid[cell]:
            x,y = cell
            pygame.draw.circle(screen, (x/grid_size*255.0, y/grid_size*255.0, 0), (int(particle.x), int(particle.y),), 5)
    pygame.display.update()

    time.sleep(5)
    pygame.quit()