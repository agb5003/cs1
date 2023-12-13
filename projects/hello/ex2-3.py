'''
    Computer Seminar I, Homework Chapter 2
    Maximilian Fernaldy
    C2TB1702
    
    README

    This file has to be ran from the parent directory of week2, which
    contains the folder assets/. This can be circumvented using the
    built-in Python module 'os' and changing the working directory to
    the folder where this file is located:

    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    Which will allow running the file from any working directory in the
    filesystem, but since this is outside the scope of the class, I will 
    refrain from using it.
'''

import pygame

# Screen size
WIDTH = 600
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hello, pygame")  # Window title
clock = pygame.time.Clock()

# Image
image = pygame.image.load("assets/player/p1_walk01.png")
image_rect = image.get_rect()

# Text
mainfont = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)
text_surf = mainfont.render("hello, pygame", True, pygame.Color("Green"))
text_rect = text_surf.get_rect()

# Make a new rectangle for ellipse, which is an inflated version of text_rect
ellipse_rect = pygame.Rect.inflate(text_rect, 45, 15)

while True:
    # Handle exit when escape is pressed
    pygame.event.clear()  # Without an event loop, the events need to be cleared
    key_pressed = pygame.key.get_pressed()  # Get a list of the state of keys
    if key_pressed[pygame.K_ESCAPE]:  
        # pygame.K_ESCAPE is a predefined integer value corresponding to the index of the state
        # of the Escape key in the key_pressed list.
        break

    # Get mouse position
    mousepos = pygame.mouse.get_pos()
    ## Update character position
    '''
        Since we relate the position of the text and ellipse to the image, when the position
        of the image is changed, the other elements will follow, which means their positions
        relative to each other do not change.

        Simply change the attribute from topleft to center, and the mouse position will now be
        at the center of the character instead of the top left.
    '''
    image_rect.center = mousepos
    ## Update ellipse position
    ellipse_rect.midtop = (image_rect.topright[0] + int(ellipse_rect.width/2), image_rect.topright[1])
    ## Update text position
    text_rect.center = ellipse_rect.center
    
    # Fill background
    screen.fill(pygame.Color("Black"))


    # Show display elements

    ## Display crosshair
    pygame.draw.line(screen, "Blue", (mousepos[0], 0), (mousepos[0], HEIGHT), width=3)
    pygame.draw.line(screen, "Blue", (0, mousepos[1]), (WIDTH, mousepos[1]), width=3)

    ## Show character sprite
    ## Show character AFTER crosshair so it's drawn over the lines
    screen.blit(image, image_rect)

    ## Ellipse
    pygame.draw.ellipse(screen, "Red", ellipse_rect, width=4)
    ### Show text last so it's in front of the ellipse
    screen.blit(text_surf, text_rect)


    # Screen update
    pygame.display.update()
    clock.tick(60) # Limit FPS to temper CPU usage

pygame.quit()
exit()

