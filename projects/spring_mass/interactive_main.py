import random
import pygame
import spring_mass as spm


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
                                 spm.DottedLineDrawer("white", width=2), break_threshold)

    def create_collision_resolver(self):
        return spm.DisplayCollisions(self.world, self.actor_list, drawer=spm.TextDrawer)

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