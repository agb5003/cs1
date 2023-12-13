import pygame


def init_screen():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    return screen


def create_text(font_size=50, font_file=None, text_string="hello, pygame"):
    antialias = True
    font = pygame.font.Font(font_file, font_size)
    text_image = font.render(text_string, antialias, pygame.Color("green"))
    return text_image


def draw(screen, player_image, text_image, mouse_pos):
    screen.fill(pygame.Color("black"))
    screen.blit(player_image, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    text_offset_x = 100
    screen.blit(text_image, (mouse_x + text_offset_x, mouse_y))
    pygame.display.update()


def main():
    screen = init_screen()
    text_image = create_text()
    player_image = pygame.image.load("../../assets/player/p1_walk01.png").convert()

    change_text = False

    while True:
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.key == pygame.K_b:
                    pass
                elif event.key == pygame.K_SPACE:
                    change_text = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    change_text = False
        if should_quit:
            break
        mouse_pos = pygame.mouse.get_pos()

        if change_text == True:
            text_image = create_text(text_string="I'm Max.")
        else:
            text_image = create_text()

        draw(screen, player_image, text_image, mouse_pos)

    pygame.quit()

# Make sure the main block only gets executed when invoked directly and not as module
if __name__ == "__main__":
    main()