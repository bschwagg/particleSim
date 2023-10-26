import math

def gravity(p1, p2, gravity_exponent):
    if p1 == p2: return

    # F=ma  however, play with acceleration dropoff m/s^gravity_exponent

    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0: distance = 0.00000001
    force = (p1.mass * p2.mass) / (distance**gravity_exponent)
    angle = math.atan2(dy, dx)
    p1.vx += force * math.cos(angle) / p1.mass
    p1.vy += force * math.sin(angle) / p1.mass


def combine_collision(p1, p2):
    if p1 == p2: return
    if not p1.active or not p2.active: return
    # combine objects if collision (to the core of particle)
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    collision_factor = 0.3
    if distance < p1.radius*collision_factor  or distance < p2.radius*collision_factor:
        print('boom')
        # conservation of momentum
        # m1v1+m2v2= (m1+m2)v′
        p1.vx = (p1.mass*p1.vx + p2.mass*p2.vx)/(p1.mass+p2.mass)
        p1.vy = (p1.mass*p1.vy + p2.mass*p2.vy)/(p1.mass+p2.mass)
        p1.mass += p2.mass
        p1.radius = int(math.sqrt(p1.mass) * 2)
        # p1.x = (p1.x + p2.x)/2
        # p1.y = (p1.y + p2.y)/2
        p2.active = False
        p1.set_color_automatic()


def collision_bounce(p1, p2):
    if p1 == p2: return
    if not p1.active or not p2.active: return
    # combine objects if collision (to the core of particle)
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance <= (p1.radius+p2.radius):
        if distance == 0: distance = 0.00000001

        #conservation of momentum  vel1*mass1
        # Initial conditions for p1
        m1 = p1.mass
        v1_initial_x = p1.vx
        v1_initial_y = p1.vy

        # Initial conditions for p2
        m2 = p2.mass
        v2_initial_x = p2.vx
        v2_initial_y = p2.vy

        # Calculate the final velocities after the collision
        v1_final_x = ((m1 - m2) / (m1 + m2)) * v1_initial_x + (2 * m2 / (m1 + m2)) * v2_initial_x
        v1_final_y = ((m1 - m2) / (m1 + m2)) * v1_initial_y + (2 * m2 / (m1 + m2)) * v2_initial_y

        v2_final_x = (2 * m1 / (m1 + m2)) * v1_initial_x + ((m2 - m1) / (m1 + m2)) * v2_initial_x
        v2_final_y = (2 * m1 / (m1 + m2)) * v1_initial_y + ((m2 - m1) / (m1 + m2)) * v2_initial_y

        # Update the p1 and p2 objects with their final velocities
        p1.vx = v1_final_x
        p1.vy = v1_final_y
        p2.vx = v2_final_x
        p2.vy = v2_final_y


def downforce(p1, gravity):
    p1.vy += gravity


def bounce(p1, width, height, coef_fric=1.0):
    # pin-ball the objects in our box
    if p1.x + p1.radius >= float(width):
        p1.vx *= -coef_fric
        p1.x = width - p1.radius
    elif p1.x - p1.radius < 0.0:
        p1.vx *= -coef_fric
        p1.x = p1.radius

    if p1.y + p1.radius >= float(height):
        p1.vy *= -coef_fric
        p1.y = height - p1.radius
    elif p1.y - p1.radius < 0:
        p1.vy *= -coef_fric
        p1.y = p1.radius


def portal(p1, width, height):
    # pin-ball the objects in our box
    if p1.x > width:
        p1.x -= (width + abs(p1.vx))
    elif p1.x < 0:
        p1.x += width + abs(p1.vx)

    if p1.y > height:
        p1.y -= (height  + abs(p1.vy))
    elif p1.y < 0:
        p1.y += height  + abs(p1.vy)


def speed_limit(p1, vx_max, vy_max):
    if p1.vx > vx_max: p1.vx = vx_max
    if p1.vy > vy_max: p1.vy = vy_max

    if p1.vx < -vx_max: p1.vx = -vx_max
    if p1.vy < -vy_max: p1.vy = -vy_max


def set_color_by_speed(p1):
    # lerp map is:
    # -20 -> 255
    # 0 -> 0
    # 20 -> 255

    r =  abs(p1.vx)/20.0*255.0 
    r = min(r,255)
    r = max(0, r)

    g =  abs(p1.vy)/20.0*255.0 
    g = min(g,255)
    g = max(0, g)
    
    b = 100 
    p1.set_color_direct(r,g,b)
