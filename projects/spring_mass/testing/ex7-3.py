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

Finally, instead of CollisionResolver, DisplayCollisions is used as the collision resolver (see line 121 in this file).

This is what I mean by the textbook quote: https://web.tohoku.ac.jp/kc_kyomu/computer_seminar1/py/textbook_en/spring.html#:~:text=By%20referring%20to%20the%20Spring%20class%20implementation


'''

import random
import pygame
import spring_mass as spm
import math


class DottedLineDrawer(spm.LineDrawer):
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


class TextDrawer:
    def __init__(self, color=pygame.Color("yellow")):
        self.color = color
        self.font = pygame.font.Font(None, 50)

    def __call__(self, surface, collisions):
        self.text_surf = self.font.render(f"{collisions} total collisions", True, self.color)
        surface.blit(self.text_surf, (20,20))

class DisplayCollisions(spm.CollisionResolver):
    def __init__(self, world, actor_list, target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or TextDrawer(pygame.Color("Yellow"))

        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = spm.is_point_mass
        else:
            self.target_condition = target_condition

        self.collisions = 0

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = spm.compute_impact_force_between_points(p1, p2, self.world.dt)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)
                self.collisions += 1
    
    def draw(self, surface):
        self.drawer(surface, self.collisions)


class ActorFactory:
    def __init__(self, world, actor_list):
        self.world = world
        self.actor_list = actor_list

    def create_point_mass(self, pos, fixed=False):
        vel = (random.uniform(-10, 10), random.uniform(-10, 0))
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
        spring_const = 0.01
        natural_len = 20
        break_threshold = 5.0
        return spm.FragileSpring(p1, p2, self.world, spring_const, natural_len,
                                 DottedLineDrawer("white", width=2), break_threshold)


    def create_collision_resolver(self):
        return DisplayCollisions(self.world, self.actor_list)

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

        self.world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0.1))
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