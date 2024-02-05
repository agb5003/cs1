import pygame
import math


PgVector = pygame.math.Vector2


class World:
    def __init__(self, size, dt, gravity_acc):
        self.size = size
        self.dt = dt
        self.gravity_acc = PgVector(gravity_acc)


class CircleDrawer:
    def __init__(self, color, width):
        self.color = pygame.Color(color)
        self.width = width

    def __call__(self, screen, center, radius):
        pygame.draw.circle(screen, self.color, center, radius, self.width)


class LineDrawer:
    def __init__(self, color, width):
        self.color = pygame.Color(color)
        self.width = width

    def __call__(self, screen, pos1, pos2):
        pygame.draw.line(screen, self.color, pos1, pos2, self.width)


'''
Exercise 7-1

(Continuation of the explanation from ex7-1.py)
To draw a dotted line, we first get the distance between points, then set the desired radius and length of the gaps between dots. Then, we use the distance between points to compute how many dots are required to be drawn between the particles. Finally, we change dx and dy to be the distance between each dot, and use those to draw dots between the particles. I added one to the range because without it, the dot will stop a bit before reaching the center of the second particle, even though we want the dotted line to span the length between the center of two particles.

'''
class DottedLineDrawer(LineDrawer):
    def __call__(self, screen, pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dot_radius = 2
        gap_length = 5
        distance = math.sqrt(dx**2 + dy**2)
        dot_count = int(distance / (dot_radius * 2 + gap_length))

        if dot_count == 0:
            return  # Prevent division by zero

        dx = dx / dot_count
        dy = dy / dot_count

        for i in range(dot_count + 1):
            pygame.draw.circle(screen, self.color, (int(pos1[0] + i * dx), int(pos1[1] + i * dy)), dot_radius)


def compute_gravity_force(mass, gravity_acc):
    return mass * gravity_acc


def compute_viscous_damping_force(viscous_damping, vel):
    return -viscous_damping * vel


def compute_harmonic_force(amplitude, frequency):
    time = pygame.time.get_ticks() // 16
    return PgVector((amplitude * math.sin(frequency * time)), 0)


def integrate_symplectic(pos, vel, force, mass, dt):
    vel_new = vel + force / mass * dt
    pos_new = pos + vel_new * dt
    return pos_new, vel_new


class PointMass:
    def __init__(self, pos, vel, world, radius=10.0, mass=10.0,
                 viscous_damping=0.01, restitution=0.95, harmonic_force = False, 
                 amplitude=0, frequency=0, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or CircleDrawer("blue", 1)

        self.pos = PgVector(pos)
        self.vel = PgVector(vel)
        self.radius = radius
        self.mass = mass
        self.viscous_damping = viscous_damping
        self.restitution = restitution

        self.harmonic_force = harmonic_force

        if harmonic_force == True:
            self.amplitude = amplitude
            self.frequency = frequency

        self.total_force = PgVector((0, 0))
        self.message_list = []

    def update(self):
        self.generate_force()
        self.move()
        self.total_force = PgVector((0, 0))
        self.message_list.clear()

    def draw(self, screen):
        self.drawer(screen, self.pos, self.radius)

    def receive_force(self, force):
        self.total_force += PgVector(force)

    def receive_message(self, msg):
        self.message_list.append(msg)

    def generate_force(self):
        force_g = compute_gravity_force(self.mass, self.world.gravity_acc)
        force_v = compute_viscous_damping_force(self.viscous_damping, self.vel)
        if self.harmonic_force == True:
            force_f = compute_harmonic_force(self.amplitude, self.frequency)
            self.receive_force(force_g + force_v + force_f)
        else:
            self.receive_force(force_g + force_v)

    def move(self):
        self.pos, self.vel = \
            integrate_symplectic(self.pos, self.vel, self.total_force, self.mass, self.world.dt)

        for msg in self.message_list:
            if msg["type"] == "floor_hit" and self.vel.y > 0:
                # constrain y on or above floor
                self.pos.y = msg["y"] - self.radius
        

class FixedPointMass(PointMass):
    def __init__(self, pos, vel, world, radius=10.0, mass=10.0,
                 viscous_damping=0.01, restitution=0.95, harmonic_force = False, 
                 amplitude=0, frequency=0, drawer=None):
        super().__init__(pos, vel, world, radius, mass,
                         viscous_damping, restitution, harmonic_force, amplitude, frequency, drawer)
        self.vel, self.mass = PgVector((0, 0)), 1e9

    def move(self):
        pass


def compute_restoring_force(pos1, pos2, spring_const, natural_len):
    if pos1 == pos2:
        return None
    vector12 = pos2 - pos1
    distance = vector12.magnitude()
    unit_vector12 = vector12 / distance
    f1 = unit_vector12 * spring_const * (distance - natural_len)
    return f1


class Spring:
    def __init__(self, point_mass1, point_mass2, world,
                 spring_const=0.01, natural_len=0.0, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or DottedLineDrawer("blue", 1, )

        self.p1 = point_mass1
        self.p2 = point_mass2
        self.spring_const = spring_const
        self.natural_len = natural_len

    def update(self):
        if not (self.p1.is_alive and self.p2.is_alive):
            self.is_alive = False
            return
        self.generate_force()

    def draw(self, screen):
        self.drawer(screen, self.p1.pos, self.p2.pos)

    def generate_force(self):
        f1 = compute_restoring_force(self.p1.pos, self.p2.pos, self.spring_const, self.natural_len)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)


class FragileSpring(Spring): # Inherits from Spring, except it breaks when a certain restoring force threshold is met
    def __init__(self, point_mass1, point_mass2, world,
                 spring_const=0.01, natural_len=0.0, drawer=None,
                 break_threshold=1e9):
        super().__init__(point_mass1, point_mass2, world, spring_const,
                         natural_len, drawer)
        self.break_threshold = break_threshold

    def generate_force(self):
        f1 = compute_restoring_force(self.p1.pos, self.p2.pos, self.spring_const, self.natural_len)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)
        if f1.magnitude() > self.break_threshold:
            self.is_alive = False

'''
Exercise 7-4

(Continuation of the explanation from ex7-4.py)
It is somewhat unsightly/smelly code to see Electrostatic force inheriting Spring force, but they 
are both conservative forces, so it also might make some sense. In my mind, it would look neater if 
both classes inherit from another parent class, but that's not needed for what needs to be done in 
Exercise 7-4.

Instead of spring constant, we have a coulomb constant (usually represented by k), and instead of 
only passing the positions of p1 and p2 to the calculator function, we pass the whole particle so 
that we have access to their masses as well. The formula for electrostatic force is F = k*q1*q2/
(r^2), making it inversely proportional to the square of the distance between particles. Although 
we don't have charges associated with our particles, I chose to substitute masses for charges here. 
Granted this would really make the force closer to the gravitational force F = G*m1*m2 / (r^2), but 
since we already have a gravity vector in the simulation, I thought it would be more appropriate to 
think of this force as electrostatic force instead.

'''

def compute_electrostatic_force(p1, p2, coulomb_const):
    pos1 = p1.pos
    pos2 = p2.pos
    if pos1 == pos2:
        return None
    vector12 = pos2 - pos1
    distance = vector12.magnitude()
    unit_vector12 = vector12 / distance
    f1 = unit_vector12 * coulomb_const * p1.mass * p2.mass / distance**2
    return -f1

class Electrostatic(Spring):
    def __init__(self, point_mass1, point_mass2, world,
                 coulomb_const=0.01, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or LineDrawer("blue", 3, )

        self.p1 = point_mass1
        self.p2 = point_mass2
        self.coulomb_const = coulomb_const
    
    def generate_force(self):
        f1 = compute_electrostatic_force(self.p1, self.p2, self.coulomb_const)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)


def is_point_mass(actor):
    return isinstance(actor, PointMass)


def compute_impact_force_between_points(p1, p2, dt):
    if (p1.pos - p2.pos).magnitude() > p1.radius + p2.radius:
        return None
    if p1.pos == p2.pos:
        return None
    normal = (p2.pos - p1.pos).normalize()
    v1 = p1.vel.dot(normal)
    v2 = p2.vel.dot(normal)
    if v1 < v2:
        return None
    e = p1.restitution * p2.restitution
    m1, m2 = p1.mass, p2.mass
    f1 = normal * (-(e + 1) * v1 + (e + 1) * v2) / (1/m1 + 1/m2) / dt
    return f1


def compute_impact_force_by_fixture(p, normal, point_included, dt):
    invasion = normal.dot(p.pos - point_included)
    if invasion + p.radius > 0 and normal.dot(p.vel) > 0:
        e = p.restitution
        v = normal.dot(p.vel)
        m = p.mass
        f = normal * (-(e + 1) * v) * m / dt
    else:
        f = None
    return f


class Boundary:
    def __init__(self, normal, point_included, world, actor_list,
                 target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or (lambda surface: None)

        self.normal = PgVector(normal).normalize()
        self.point_included = PgVector(point_included)
        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        self.drawer(surface)


    def is_floor(self):
        return self.normal == PgVector((0,1))
    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        for p in plist:
            f = compute_impact_force_by_fixture(p, self.normal, self.point_included, self.world.dt)
            if f is None:
                continue
            p.receive_force(f)
            if self.is_floor():
                p.receive_message({"type": "floor_hit", "y": self.point_included.y})


def is_point_mass(actor):
    return isinstance(actor, PointMass)


def compute_impact_force_between_points(p1, p2, dt):
    if (p1.pos - p2.pos).magnitude() > p1.radius + p2.radius:
        return None
    if p1.pos == p2.pos:
        return None
    normal = (p2.pos - p1.pos).normalize()
    v1 = p1.vel.dot(normal)
    v2 = p2.vel.dot(normal)
    if v1 < v2:
        return None
    e = p1.restitution * p2.restitution
    m1, m2 = p1.mass, p2.mass
    f1 = normal * (-(e + 1) * v1 + (e + 1) * v2) / (1/m1 + 1/m2) / dt
    return f1


class CollisionResolver:
    def __init__(self, world, actor_list, target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or (lambda surface: None)

        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        self.drawer(surface)

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = compute_impact_force_between_points(p1, p2, self.world.dt)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)

'''

Exercise 7-3

This exercise exhibits the use of placeholder methods in parent classes. The draw() method in the 
CollisionResolver class is a placeholder method, meant to do nothing when used with the parent 
class, but allows classes which are children of it to use the method with the defined arguments. In 
this case, the argument is surface, which is the surface on which the drawer will draw on. I made 
two significant modifications here: first, instead of a lambda function that does and returns 
nothing, when DisplayCollisions is used instead of CollisionResolver, the default value for drawer 
is TextDrawer, a function that prints the number of collisions to the top left of the screen.

Here, the amount of things that needed to be changed means that the inheritance doesn't really do 
anything other than reusing the update() method. I think in the textbook, when "By referring to the 
Spring class implementation" is written, it meant that I was supposed to see the similarities that 
the two classes have and write the new class by referring to those similarities, instead of 
literally referring to it as a parent class. However, I will keep the inheritance because I think 
it's also possible that I'm wrong and inheritance can be used to a much higher degree here. 
Frankly, I need to learn much more about inheritance and design patterns relating to classes.

This is what I mean by the textbook quote: https://web.tohoku.ac.jp/kc_kyomu/computer_seminar1/py/textbook_en/spring.html#:~:text=By%20referring%20to%20the%20Spring%20class%20implementation

'''

class TextDrawer:
    def __init__(self, color=pygame.Color("yellow")):
        self.color = color
        self.font = pygame.font.Font(None, 50)

    def __call__(self, surface, collisions):
        self.text_surf = self.font.render(f"{collisions} total collisions", True, self.color)
        surface.blit(self.text_surf, (20,20))

class DisplayCollisions(CollisionResolver):
    def __init__(self, world, actor_list, target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or TextDrawer(pygame.Color("Yellow"))

        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

        self.collisions = 0

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = compute_impact_force_between_points(p1, p2, self.world.dt)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)
                self.collisions += 1
    
    def draw(self, surface):
        self.drawer(surface, self.collisions)
        
