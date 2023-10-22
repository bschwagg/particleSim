
from random import randint
import math
    
# Particle class
class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = int(math.sqrt(mass) * 2)
        self.set_color()
        self.vx = 0
        self.vy = 0
        self.active = True

    def set_bounds(self, w, h):
        self.width = w
        self.height = h

    def set_color(self):

        # color is based on radius.  
        # rgb values from 0 to 255
        g = min(self.radius*15, 255)
        r = max(255-self.radius*4, 100)
        b = min(self.radius*10, 200)
        self.color = (r,g,b)


    def apply_gravity(self, other):
        if not self.active or not other.active: return

        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0: distance = 0.00000001
        force = (self.mass * other.mass) / (distance**2)
        angle = math.atan2(dy, dx)
        self.vx += force * math.cos(angle) / self.mass
        self.vy += force * math.sin(angle) / self.mass

        # combine objects if collision (to the core of particle)
        collision_factor = 0.3
        if distance < self.radius*collision_factor  or distance < other.radius*collision_factor:
            print('boom')
            # conservation of momentum
            # m1v1+m2v2= (m1+m2)v′
            self.vx = (self.mass*self.vx + other.mass*other.vx)/(self.mass+other.mass)
            self.vy = (self.mass*self.vy + other.mass*other.vy)/(self.mass+other.mass)
            self.mass += other.mass
            self.radius = int(math.sqrt(self.mass) * 2)
            # self.x = (self.x + other.x)/2
            # self.y = (self.y + other.y)/2
            other.active = False
            self.set_color()
            del other # does this work?


    def update(self, dt):
        if not self.active: return
        self.x += self.vx*dt
        self.y += self.vy*dt

        # pin-ball the objects in our box
        if self.x > self.width or self.x < 0:
            self.vx *= -1
        if self.y > self.height or self.y < 0:
            self.vy *= -1
