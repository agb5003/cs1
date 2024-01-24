import pygame
import spring_mass as spm


def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0.5))
    actor_list = []


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