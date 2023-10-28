import math


def gravity(p1, p2, gravity_exponent):
    if p1 == p2: return
    def _gravity(a1,a2,gravity_exponent):
        # F=ma  however, play with acceleration dropoff m/s^gravity_exponent
        dx = a2.x - a1.x
        dy = a2.y - a1.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0: distance = 0.00000001
        force = (a1.mass * a2.mass) / (distance**gravity_exponent)
        angle = math.atan2(dy, dx)
        a1.vx += force * math.cos(angle) / a1.mass
        a1.vy += force * math.sin(angle) / a1.mass
    # apply symmetrically...
    _gravity(p2, p1, gravity_exponent)
    _gravity(p1, p2, gravity_exponent)


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


def collision_bounce(p1, p2, damping_factor):
    if p1 == p2: return
    if not p1.active or not p2.active: return
    # combine objects if collision (to the core of particle)
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance <= (p1.radius+p2.radius):
        # print("boink--------------------")
        if distance == 0: distance = 0.00000001

        # TODO: balls get stuck together. which is called "tunneling"

        # Initial conditions for p1
        m1 = p1.mass
        x1 = p1.x
        y1 = p1.y
        v1_initial_x = p1.vx
        v1_initial_y = p1.vy
        r1 = p1.radius

        # Initial conditions for p2
        m2 = p2.mass
        x2 = p2.x
        y2 = p2.y
        v2_initial_x = p2.vx
        v2_initial_y = p2.vy
        r2 = p2.radius

        # Calculate the relative position and velocity vectors
        relative_x = x2 - x1
        relative_y = y2 - y1
        relative_velocity_x = v2_initial_x - v1_initial_x
        relative_velocity_y = v2_initial_y - v1_initial_y

        # Calculate the dot product of the relative position and relative velocity
        dot_product = relative_x * relative_velocity_x + relative_y * relative_velocity_y
        if dot_product > 0:
            # balls are moving away from one another! lets skip collision!
            return


        # Calculate the angle of impact
        angle_of_impact = math.atan2(relative_y, relative_x)

        # Calculate the relative velocity magnitude
        relative_velocity = math.sqrt(relative_velocity_x**2 + relative_velocity_y**2)

        # Calculate the final velocities after the collision
        v1_final = (v1_initial_x * math.cos(angle_of_impact) + v1_initial_y * math.sin(angle_of_impact))
        v2_final = (v2_initial_x * math.cos(angle_of_impact) + v2_initial_y * math.sin(angle_of_impact))

        # Perform the elastic collision calculations
        v1_final_after_collision = ((m1 - m2) * v1_final + (m2 + m2) * v2_final) / (m1 + m2)
        v2_final_after_collision = (2 * m1 * v1_final + (m2 - m1) * v2_final) / (m1 + m2)

        v1_final_after_collision *= damping_factor
        v2_final_after_collision *= damping_factor


        # Update the p1 and p2 objects with their final velocities
        p1.vx = v1_final_after_collision * math.cos(angle_of_impact) - v1_final * math.sin(angle_of_impact)
        p1.vy = v1_final_after_collision * math.sin(angle_of_impact) + v1_final * math.cos(angle_of_impact)
        p2.vx = v2_final_after_collision * math.cos(angle_of_impact) - v2_final * math.sin(angle_of_impact)
        p2.vy = v2_final_after_collision * math.sin(angle_of_impact) + v2_final * math.cos(angle_of_impact)

        # print('-----------------angle=', angle_of_impact)
        # print('p1 mass=', m1)
        # print('p1 vx:',v1_initial_x,'->',p1.vx)
        # print('p1 vy:',v1_initial_y,'->',p1.vy)
        # print('p2 mass=', m2)
        # print('p2 vx:',v2_initial_x,'->',p2.vx)
        # print('p2 vy:',v2_initial_y,'->',p2.vy)
        

def downforce(p1, gravity):
    p1.vy += gravity


def bounce(p1, width, height, coef_fric=1.0):
    # pin-ball the objects in our box
    if p1.x + p1.radius >= float(width) and p1.vx > 0:
        p1.vx *= -coef_fric
    elif p1.x - p1.radius < 0.0 and p1.vx < 0:
        p1.vx *= -coef_fric

    if p1.y + p1.radius >= float(height) and p1.vy > 0:
        p1.vy *= -coef_fric
    elif p1.y - p1.radius < 0 and p1.vy < 0:
        p1.vy *= -coef_fric


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

    magnitude = math.sqrt(p1.vx**2 + p1.vy**2)

    r =  (magnitude)/40.0*255.0 
    r = min(r,255)
    r = max(0, r)

    g =  255 - (magnitude)/40.0*255.0 
    g = min(g,255)
    g = max(0, g)
    
    b = 100 
    p1.set_color_direct(r,g,b)


def wind(p1, x_center, y_center, max_force, distance_reached, use_mouse_pos):
    attracted = False
    doubled = False

    if use_mouse_pos:
        import pygame
        if pygame.mouse.get_focused():
            x_center, y_center = pygame.mouse.get_pos()
            attracted, middle_button, doubled = pygame.mouse.get_pressed(3)
            if middle_button:
                return
    # Calculate the distance from the particle to the wind source
    dx = p1.x - x_center
    dy = p1.y - y_center
    # Calculate the vector from nozzle to p1
    # Calculate the vector from nozzle to p1
    vector_to_p1 = (p1.x - x_center, p1.y - y_center)

    # the magnitude and direction of the vector from "nozzle" to "p1."
    magnitude = math.sqrt(vector_to_p1[0]**2 + vector_to_p1[1]**2)
    direction = math.atan2(vector_to_p1[1], vector_to_p1[0])

    if magnitude > distance_reached: 
        return
    
    if doubled: 
        max_force *= 2.0

    force = max_force - max_force*magnitude/distance_reached
    
    if attracted:
        force -= 1.0

    p1.vx += force * math.cos(direction)
    p1.vy += force * math.sin(direction)