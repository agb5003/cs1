import pygame
import spring_mass as spm


def create_point_mass(pos, world, fixed=False):
    vel = (0, 0)
    radius = 10
    mass = 0.1
    viscous = 0.01
    restitution = 0.95
    if fixed:
        PointMassClass = spm.FixedPointMass
    else:
        PointMassClass = spm.PointMass
    return PointMassClass(pos, vel, world, radius, mass, viscous, restitution,
                          spm.CircleDrawer("green", width=0))


def create_spring(p1, p2, world):
    spring_const = 0.02
    natural_len = 5
    return spm.Spring(p1, p2, world, spring_const, natural_len,
                      spm.LineDrawer("white", width=2))


def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0.5))
    actor_list = []

    p = []
    sp = []
    spacing = 30
    p.append(create_point_mass((width/2, 0), world, fixed=True))
    for k in range(1, 15):
        p.append(create_point_mass((width/2, spacing * k), world))
        sp.append(create_spring(p[k - 1], p[k], world))
    actor_list += p + sp

    while True:
        frames_per_second = 60
        clock.tick(frames_per_second)

        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.key == pygame.K_SPACE:
                    sp[0].is_alive = False
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