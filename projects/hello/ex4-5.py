import pygame
import math

def init_screen():
    """Initialize pygame screen.

    Library pygame is initialized and screen size is set to 600x400.

    Returns
    -------
    Surface
        Screen surface
    """
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    return screen


def create_text(font_size=50, font_file=None):
    """Create text surfaces to iterate through.
    
    Parameters
    ----------
    font_size : Integer
        Size of the font to be used to render text
    font_file : String
        If any, path to a .ttf file to be used to render text
    
    Returns
    -------
    text_images : Surface
        An array of text surfaces.
    """
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
    """Create character frame surfaces to iterate through.
    
    Returns
    -------
    player_images : Surface
        An array of text surfaces.
    """
    player_images = [
        pygame.image.load("../../assets/player/p1_walk04.png").convert(),
        pygame.image.load("../../assets/player/p1_walk05.png").convert(),
        pygame.image.load("../../assets/player/p1_walk06.png").convert(),
        pygame.image.load("../../assets/player/p1_walk07.png").convert()
    ]
    return player_images

def draw(screen, player_image, text_image, mouse_pos):
    """Draw images onto screen.

    player_image is drawn at mouse_pos on screen, and text_image,
    unless it is None, is drawn to the right of player_image.

    Parameters
    ----------
    screen : Surface
        Screen onto which images are drawn.
    player_image : Surface
        Player image to be blit'ed.
    text_image : Surface
        Text image to be blit'ed.  If None is passed, nothing is drawn.
    mouse_pos : tuple[int, int]
        Position where player_image is blit'ed.
    """
    screen.fill(pygame.Color("black"))
    screen.blit(player_image, mouse_pos)
    mouse_x, mouse_y = mouse_pos
    if text_image is not None:
        text_offset_x = 100
        screen.blit(text_image, (mouse_x + text_offset_x, mouse_y))
    pygame.display.update()

def get_mouse_speed(mouse_rel):
    """Get the speed of the mouse cursor.
    
    distance_units is used here so that small changes in mouse cursor speed doesn't
    erratically change the speed of the animation. Without this, the mouse needs
    to be moved very slowly in order to see the difference in speed between slow
    and fast mouse movements. Ideally, having more frames in the walk cycle would
    also improve the animation when the cursor is moved slowly.

    Parameters
    ----------
    mouse_rel : Integer
        relative movement of cursor since last pygame.get_rel call
    Returns
    -------
    mouse_speed: Integer
        Speed of mouse cursor in distance units
    """
    distance_units = 4 #pixels
    return int(math.sqrt(mouse_rel[0]**2 + mouse_rel[1]**2) // distance_units)

def update_animation_index(frame_index, mouse_speed, frame_number):
    """Update the animation index.
    
    Parameters
    ----------
    frame_index : Integer
        Counter for the current frame
    mouse_speed : Integer
        Speed of mouse cursor in distance units
    frame_number : Integer
        The total number of surfaces inside the array containing the character frames
    
    Returns
    -------
    animation_index : Integer
        The index of the frame that should be displayed.
    """
    animation_period = int(max(6 // mouse_speed, 1))
    animation_index = frame_index // animation_period % frame_number
    return animation_index


def main():
    screen = init_screen()
    clock = pygame.time.Clock()
    frame_index = 0
    animation_index = frame_index
    text_index = -1
    player_images = create_player()
    text_images = create_text()

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
                elif event.key == pygame.K_b:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                text_index += 1
        if should_quit:
            break
        mouse_pos = pygame.mouse.get_pos()
        mouse_rel = pygame.mouse.get_rel()
        buttons_pressed = pygame.mouse.get_pressed()

        text_index %= len(text_images)
        if buttons_pressed[0]:
            text_image_shown = text_images[text_index]
        else:
            text_image_shown = None

        mouse_speed = get_mouse_speed(mouse_rel)
        if mouse_speed != 0:
            animation_index = update_animation_index(frame_index, mouse_speed, len(player_images))

        draw(screen, player_images[animation_index], text_image_shown, mouse_pos)
        frame_index += 1
    pygame.quit()

# Make sure the main block only gets executed when invoked directly and not as module
if __name__ == "__main__":
    main()