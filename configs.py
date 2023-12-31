from random import randint
from particle import Particle
from pygrid import PyGrid
import physics

grid = None
# Screen dimensions
width, height = 1024, 512
trail_intensity = 0.8 # [0.0 -> 1.0]


def mouse_wind():
    global grid
    grid_size = 2**0 # if a radius goes across the 3x3 grid it won't collide. so disable grid.
    grid = PyGrid(grid_size,grid_size)

    # add a bunch of particles to the grid
    num_particles=800
    global trail_intensity
    trail_intensity = 0.4
    for i in range(num_particles):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(1,100))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        grid.add_particle(p)

    info = {
            'name': 'container',
            'function': physics.bounce, 
            'arguments': [width, height, 0.6],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)
    # info = {
    #         'name': 'interact with one another',
    #         'function': physics.collision_bounce, #physics., combine_collision
    #         'arguments': [.85],
    #         'interact_with_other_particles': True,
    #         'check_neighbor_cells': True
    #         }
    # grid.add_physics(info)
    info = {
            'name': 'wind',
            'function': physics.wind, 
            'arguments': [width/2, height, 1.2, height*4/5, True],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)
    # info = {
    #         'name': 'drop down',
    #         'function': physics.downforce, 
    #         'arguments': [ 0.25 ],
    #         'interact_with_other_particles': False, 
    #         'check_neighbor_cells': False
    #         }
    # grid.add_physics(info)


def wind():
    global grid
    grid_size = 2**0 # if a radius goes across the 3x3 grid it won't collide. so disable grid.
    grid = PyGrid(grid_size,grid_size)

    # add a bunch of particles to the grid
    num_particles=80
    global trail_intensity
    trail_intensity = 0.6
    for i in range(num_particles):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(6,150))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 12
        p.vx = randint(-init_speed,init_speed)
        # p.vy = randint(-10,00)
        grid.add_particle(p)

    info = {
            'name': 'container',
            'function': physics.bounce, 
            'arguments': [width, height, 0.8],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)
    info = {
            'name': 'interact with one another',
            'function': physics.collision_bounce, #physics., combine_collision
            'arguments': [.85],
            'interact_with_other_particles': True,
            'check_neighbor_cells': True
            }
    grid.add_physics(info)
    info = {
            'name': 'wind',
            'function': physics.wind, 
            'arguments': [width/2, height, 1.1, height*4/5, False],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)
    info = {
            'name': 'drop down',
            'function': physics.downforce, 
            'arguments': [ 0.25 ],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)


def dropped_balls():
    global grid
    grid_size = 2**0 # if a radius goes across the 3x3 grid it won't collide. so disable grid.
    grid = PyGrid(grid_size,grid_size)

    # add a bunch of particles to the grid
    num_particles=150
    global trail_intensity
    trail_intensity = 0.3
    for i in range(num_particles):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(6,22))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 12
        p.vx = randint(-init_speed,init_speed)
        # p.vy = randint(-10,00)
        grid.add_particle(p)

    # put a big ball in middle
    # TODO: if radius is bigger than the grid the physics won't work
    radius = 20
    mass = (radius/2)**2
    p = Particle(width/2.5, height-radius, mass)
    p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
    print('big ball', p.__dict__)
    grid.add_particle(p)

    radius = 40
    mass = (radius/2)**2
    p = Particle(width*3/4+20, height/2, mass)
    p.set_color_direct(0,128,255)
    p.vx = 40
    grid.add_particle(p)


    radius = 40
    mass = (radius/2)**2
    p = Particle(width*1/4-20, height/2, mass)
    p.vx = -50
    # p.vy = 10
    p.set_color_direct(255,128,255)
    grid.add_particle(p)


    radius = 39
    mass = (radius/2)**2
    p = Particle(width*2/4-20, height/2, mass)
    # p.vx = 10
    # p.vy = -30
    p.set_color_direct(0,255,255)
    grid.add_particle(p)

    radius = 40
    mass = (radius/2)**2
    p = Particle(width*2/4-20-radius*1.9, height/4, mass)
    # p.vx = 10
    # p.vy = -20
    p.set_color_direct(0,128,0)
    grid.add_particle(p)

    info = {
            'name': 'hit floor',
            'function': physics.bounce, 
            'arguments': [width, height, 0.75],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 
    info = {
            'name': 'interact with one another',
            'function': physics.collision_bounce, #physics., combine_collision
            'arguments': [.85],
            'interact_with_other_particles': True,
            'check_neighbor_cells': True
            }
    grid.add_physics(info)
    info = {
            'name': 'drop down',
            'function': physics.downforce, 
            'arguments': [ 0.25 ],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info)
    # info = {
    #         'name': 'colorize it',
    #         'function': physics.set_color_by_speed, 
    #         'arguments': [],
    #         'interact_with_other_particles': False, 
    #         'check_neighbor_cells': False
    #         }
    # grid.add_physics(info) 


def dropped_balls_portal():
    global grid
    grid_size = 2**3
    grid = PyGrid(grid_size,grid_size)

    # add a bunch of particles to the grid
    num_particles=10
    global trail_intensity
    trail_intensity = 0
    for i in range(num_particles):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(20,100))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 20
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
            'name': 'go around',
            'function': physics.portal, 
            'arguments': [width, height],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 

    info = {
            'name': 'interact with one another',
            'function': physics.collision_bounce, #physics., combine_collision
            'arguments': [],
            'interact_with_other_particles': True,
            'check_neighbor_cells': True
            }
    grid.add_physics(info)

    info = {
            'name': 'drop down',
            'function': physics.downforce, 
            'arguments': [ 0.1 ],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 


def gravity():
    global grid
    grid_size = 2**3
    grid = PyGrid(grid_size,grid_size)
    

    # add a bunch of particles to the grid
    # a few big ones
    for i in range(5):
        p = Particle(randint(width/4,width*3/4), randint(height/4, height*3/4), randint(25,50))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 14
        p.vx = randint(-init_speed,init_speed)
        p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)
    # a bunch of little ones
    for i in range(35):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(5,10))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 0
        p.vx = randint(-init_speed,init_speed)
        p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)

    # do the bounds checking first, because the last operation was updating position
    # info = {
    #         'name': 'stay in container',
    #         'function': physics.bounce, 
    #         'arguments': {width, height, 1.0},
    #         'interact_with_other_particles': False, 
    #         'check_neighbor_cells': False
    #         }
    info = {
        'name': 'stay in container',
        'function': physics.portal, 
        'arguments': [width, height],
        'interact_with_other_particles': False, 
        'check_neighbor_cells': False
        }
    grid.add_physics(info)


    info = {
            'name': 'gravity',
            'function': physics.gravity, 
            'arguments': [1.9],
            'interact_with_other_particles': True, 
            'check_neighbor_cells': True
            }
    grid.add_physics(info) 

    info = {
        'name': 'limit the speed',
        'function': physics.speed_limit, 
        'arguments': [ 15.0, 15.0 ],
        'interact_with_other_particles': False, 
        'check_neighbor_cells': False
        }
    grid.add_physics(info) 


def gravity_big():
    global grid
    grid_size = 2**3
    grid = PyGrid(grid_size,grid_size)
    
    global trail_intensity
    trail_intensity = 0.3

    # add a bunch of particles to the grid
    # a few big ones
    for i in range(5):
        p = Particle(randint(width/4,width*3/4), randint(height/4, height*3/4), randint(50,100))
        init_speed = 20
        p.vx = randint(-init_speed,init_speed)
        init_speed = 2
        p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)

    # do the bounds checking first, because the last operation was updating position
    info = {
        'name': 'stay in container',
        'function': physics.bounce, 
        'arguments': [width, height, 1.0],
        'interact_with_other_particles': False, 
        'check_neighbor_cells': False
        }
    grid.add_physics(info)


    info = {
            'name': 'gravity',
            'function': physics.gravity, 
            'arguments': [2],
            'interact_with_other_particles': True, 
            'check_neighbor_cells': True
            }
    grid.add_physics(info) 

    info = {
            'name': 'colorize it',
            'function': physics.set_color_by_speed, 
            'arguments': [],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 

    info = {
        'name': 'limit the speed',
        'function': physics.speed_limit, 
        'arguments': [ 20.0, 20.0 ],
        'interact_with_other_particles': False, 
        'check_neighbor_cells': False
        }
    # grid.add_physics(info) 


def three_body_problem():
    
    global grid
    grid_size = 2**0
    grid = PyGrid(grid_size,grid_size)
    
    global trail_intensity
    trail_intensity = 0.95

    for i in range(3):
        # initial conditions, see:
        # https://www.maths.ed.ac.uk/~ateckent/vacation_reports/Report_Faustino.pdf
        p = Particle(width/4*(i-1) + width/2, height/2, width/6)
        
        p.vx = -0.3471128135672417 * width/350
        p.vy = -0.532726851767674  * width/350
        if i == 1:
            p.vx *= -1.0
            p.vy *= -1.0    
        grid.add_particle(p)

    info = {
            'name': 'gravity',
            'function': physics.gravity, 
            'arguments': [2.0],
            'interact_with_other_particles': True, 
            'check_neighbor_cells': True
            }
    grid.add_physics(info) 

    info = {
            'name': 'colorize it',
            'function': physics.set_color_by_speed, 
            'arguments': [],
            'interact_with_other_particles': False, 
            'check_neighbor_cells': False
            }
    grid.add_physics(info) 



def gravity_combine():
    global grid
    grid_size = 2**3
    grid = PyGrid(grid_size,grid_size)
    

    # add a bunch of particles to the grid
    # a few big ones
    for i in range(5):
        p = Particle(randint(width/4,width*3/4), randint(height/4, height*3/4), randint(25,50))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 14
        p.vx = randint(-init_speed,init_speed)
        p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)
    # a bunch of little ones
    for i in range(80):
        p = Particle(randint(1,width-1), randint(1,height-1), randint(5,10))
        p.set_color_direct(randint(1,255), randint(1,255), randint(1,255) )
        init_speed = 5
        p.vx = randint(-init_speed,init_speed)
        p.vy = randint(-init_speed,init_speed)
        grid.add_particle(p)

    # do the bounds checking first, because the last operation was updating position
    info = {
        'name': 'stay in container',
        'function': physics.portal, 
        'arguments': [width, height],
        'interact_with_other_particles': False, 
        'check_neighbor_cells': False
        }
    grid.add_physics(info)


    info = {
            'name': 'gravity',
            'function': physics.gravity, 
            'arguments': [1.9],
            'interact_with_other_particles': True, 
            'check_neighbor_cells': True
            }
    grid.add_physics(info) 

    info = {
        'name': 'limit the speed',
        'function': physics.combine_collision, 
        'arguments': [  ],
        'interact_with_other_particles': True, 
        'check_neighbor_cells': False
        }
    grid.add_physics(info) 
