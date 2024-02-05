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
    frames_per_second = 60

    world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0))
    actor_list = []

    circle_drawer = spm.CircleDrawer("green", 0)
    
    # Boundaries are deleted to allow for overflow when amplitude grows

    # Particles with springs
    spring_const = 0.05
    natural_len = 250
    line_drawer = spm.DottedLineDrawer("white", 3)

    p3 = spm.FixedPointMass((100, 100), (0, 0), world, drawer=circle_drawer)
    p4 = spm.PointMass((400, 100), (0, 0), world, harmonic_force=True, amplitude=1, frequency=0.071, drawer=circle_drawer)
    sp34 = spm.Spring(p3, p4, world, spring_const, natural_len, line_drawer)

    p5 = spm.FixedPointMass((100, 200), (0, 0), world, drawer=circle_drawer)
    p6 = spm.PointMass((400, 200), (0, 0), world, harmonic_force=True, amplitude=1, frequency=0.3, drawer=circle_drawer)
    sp56 = spm.Spring(p5, p6, world, spring_const, natural_len, line_drawer)

    actor_list += [p3, p4, sp34, p5, p6, sp56]

    actor_list.append(spm.CollisionResolver(world, actor_list))
    
    while True:
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