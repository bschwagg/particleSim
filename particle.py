
from random import randint
import math
    
# Particle class
class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = int(math.sqrt(mass) * 2)
        self.set_color_automatic()
        self.vx = 0
        self.vy = 0
        self.active = True


    def set_color_automatic(self):
        # TODO: use lerp b/w various colors given the radius
        # color is based on radius.  
        # rgb values from 0 to 255
        g = min(self.radius*15, 255)
        r = max(255-self.radius*4, 100)
        b = min(self.radius*10, 200)
        self.color = (r,g,b)


    def set_color_direct(self, r,g,b):
        self.color = (r,g,b)


    def update(self, dt):
        if not self.active: return
        self.x += self.vx*dt
        self.y += self.vy*dt