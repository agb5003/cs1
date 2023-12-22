import pygame


def init_screen():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    return screen


def create_text(font_size=50, font_file=None):
    antialias = True
    font = pygame.font.Font(font_file, font_size)
    text_images = [
        font.render("hello, pygame", antialias, pygame.Color("green")),
        font.render("R", antialias, pygame.Color("red")),
        font.render("A", antialias, pygame.Color("orange")),
        font.render("I", antialias, pygame.Color("yellow")),
        font.render("N", antialias, pygame.Color("green")),
        font.render("B", antialias, pygame.Color("blue")),
        font.render("O", antialias, pygame.Color("violet")),
        font.render("W", antialias, pygame.Color("purple")),
    ]
    return text_images

def create_player():
    player_images = [
        pygame.image.load("../../assets/player/p1_walk04.png").convert(),
        pygame.image.load("../../assets/player/p1_walk05.png").convert(),
        pygame.image.load("../../assets/player/p1_walk06.png").convert(),
        pygame.image.load("../../assets/player/p1_walk07.png").convert()
    ]
    return player_images

def draw(screen, player_image, text_image, mouse_pos):
    screen.fill(pygame.Color("black"))
    screen.blit(player_image, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    if text_image is not None:
        text_offset_x = 100
        screen.blit(text_image, (mouse_x + text_offset_x, mouse_y))
    pygame.display.update()


def main():
    screen = init_screen()
    clock = pygame.time.Clock()
    frame_index = 0
    text_index = -1
    player_images = create_player()
    text_images = create_text()

    while True:
        frames_per_second = 144
        clock.tick(frames_per_second)
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.key == pygame.K_b:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                text_index += 1
        if should_quit:
            break
        mouse_pos = pygame.mouse.get_pos()
        buttons_pressed = pygame.mouse.get_pressed()

        text_index %= len(text_images)
        if buttons_pressed[0]:
            text_image_shown = text_images[text_index]
        else:
            text_image_shown = None

        frame_index += 1
        animation_period = 12
        animation_index = frame_index // animation_period % len(player_images)

        draw(screen, player_images[animation_index], text_image_shown, mouse_pos)
    pygame.quit()

# Make sure the main block only gets executed when invoked directly and not as module
if __name__ == "__main__":
    main()