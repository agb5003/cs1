import pygame
import spring_mass as spm


class ImageDrawer:
    def __init__(self, image):
        self.image = image

    def __call__(self, screen, center, radius):
        screen.blit(self.image, (center[0] - self.image.get_width() / 2,
                                 center[1] - self.image.get_height() / 2))


def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0.5))
    actor_list = []

    pos, vel = (100, 200), (10, -15)
    radius, mass = 10, 10
    viscous_damping = 0.01
    restitution = 0.95
    circle_drawer = spm.CircleDrawer("green", 0)
    actor_list.append(spm.PointMass(pos, vel, world, radius, mass,
                                    viscous_damping, restitution, circle_drawer))
    
    # Boundaries
    actor_list.append(spm.Boundary((1, 0), (width, 0), world, actor_list))
    actor_list.append(spm.Boundary((0, 1), (0, height), world, actor_list))
    actor_list.append(spm.Boundary((-1, 0), (0, width), world, actor_list))
    actor_list.append(spm.Boundary((0, -1), (height, 0), world, actor_list))

    # Particles with springs
    p1 = spm.PointMass((300, 100), (0, 0), world, drawer=circle_drawer)
    p2 = spm.PointMass((400, 120), (0, 0), world, drawer=circle_drawer)
    spring_const = 0.01
    natural_len = 20
    line_drawer = spm.LineDrawer("white", 3)
    sp12 = spm.Spring(p1, p2, world, spring_const, natural_len, line_drawer)
    actor_list += [p1, p2, sp12]
    
    p3 = spm.FixedPointMass((350, 50), (0, 0), world, drawer=circle_drawer)
    p4 = spm.PointMass((450, 80), (0, 0), world, drawer=circle_drawer)
    sp34 = spm.Spring(p3, p4, world, spring_const, natural_len, line_drawer)
    actor_list += [p3, p4, sp34]

    actor_list.append(spm.CollisionResolver(world, actor_list))

    image = pygame.image.load("../../assets/player/p1_walk03.png").convert_alpha()
    image_drawer = ImageDrawer(image)
    p5 = spm.PointMass((200, 300), (5, -5), world, radius=image.get_height() / 2,
                       mass=50, restitution=0.6, drawer=image_drawer)
    actor_list.append(p5)
    
    while True:
        frames_per_second = 60
        clock.tick(frames_per_second)

        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_quit = True
        if should_quit:
            break

        for a in actor_list:
            a.update()
        actor_list[:] = [a for a in actor_list if a.is_alive]

        screen.fill(pygame.Color("black"))
        for a in actor_list:
            a.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()