'''
Exercise 7-4

This exercise asks for the creation of an inverse-square law force. In physics, gravitational force 
and electrostatic force between point-particles follow the inverse-square law. In this example, I 
chose to think of the force as an electrostatic force between particles having the same polarity, 
which is why you will find the returned electrostatic force is negative. This results in particles 
repelling each other, growing further apart. Additionally, as the force is inversely proportional 
to the square of the distance between particles, you will find that particles placed close together 
will have a larger force occur, while particles placed far from each other will appear stationary 
at first, until it starts to move slowly, because the force is significantly lower.

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

import pygame
import spring_mass as spm


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

class Electrostatic(spm.Spring):
    def __init__(self, point_mass1, point_mass2, world,
                 coulomb_const=0.01, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or spm.LineDrawer("blue", 1, )

        self.p1 = point_mass1
        self.p2 = point_mass2
        self.coulomb_const = coulomb_const
    
    def generate_force(self):
        f1 = compute_electrostatic_force(self.p1, self.p2, self.coulomb_const)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)


class ActorFactory:
    def __init__(self, world, actor_list):
        self.world = world
        self.actor_list = actor_list

    def create_point_mass(self, pos, fixed=False):
        # !!! Initial velocity is set to zero to make coulomb force clear
        vel = 0
        mass = 10
        radius = 10
        viscous = 0.01
        restitution = 0.95
        if fixed:
            PointMassClass = spm.FixedPointMass
            color = "gray"
        else:
            PointMassClass = spm.PointMass
            color = "green"
        return PointMassClass(pos, vel, self.world, radius, mass, viscous,
                              restitution, drawer=spm.CircleDrawer(color, width=0))

    def create_spring(self, p1, p2):
        coulomb_const = 25
        return Electrostatic(p1, p2, self.world, coulomb_const)

    def create_collision_resolver(self):
        return spm.CollisionResolver(self.world, self.actor_list)

    def create_boundary(self, name):
        width, height = self.world.size
        geometry = {"top": ((0, -1), (0, 0)),
                    "bottom": ((0, 1), (0, height)),
                    "left": ((-1, 0), (0, 0)),
                    "right": ((1, 0), (width, 0))}
        normal, point_included = geometry[name]
        return spm.Boundary(normal, point_included, self.world, self.actor_list)
    

class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 600, 400
        self.screen = pygame.display.set_mode((width, height))

        # Gravity is set to zero to make the electrostatic force clearer
        self.world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0))
        self.actor_list = []
        self.factory = ActorFactory(self.world, self.actor_list)

        self.actor_list.append(self.factory.create_collision_resolver())
        self.actor_list.append(self.factory.create_boundary("top"))
        self.actor_list.append(self.factory.create_boundary("bottom"))
        self.actor_list.append(self.factory.create_boundary("left"))
        self.actor_list.append(self.factory.create_boundary("right"))

        self.point_mass_prev = None

    def add_connected_point_mass(self, pos, button):
        if button == 1:
            fixed = False
        elif button == 3:
            fixed = True
        else:
            return
        p = self.factory.create_point_mass(pos, fixed)
        self.actor_list.append(p)

        if self.point_mass_prev is not None:
            sp = self.factory.create_spring(p, self.point_mass_prev)
            self.actor_list.append(sp)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.point_mass_prev = p

    def update(self):
        for a in self.actor_list:
            a.update()
        self.actor_list[:] = [a for a in self.actor_list if a.is_alive]

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for a in self.actor_list:
            a.draw(self.screen)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            frames_per_second = 60
            clock.tick(frames_per_second)

            should_quit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.point_mass_prev = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.add_connected_point_mass(event.pos, event.button)
            if should_quit:
                break

            self.update()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    AppMain().run()