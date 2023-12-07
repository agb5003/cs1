import pygame
from sys import exit

WIDTH = 600
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill("Black")

# Prototype declarations
mousepos = (0,0)

# Image
image = pygame.image.load("assets/player/p1_walk01.png")

# Text
mainfont = pygame.font.Font(None, 50)
text_surf = mainfont.render("hello, pygame", True, pygame.Color("red"))

# Crosshair
crosshairx = pygame.Surface((WIDTH*2, 1))
crosshairx.fill("Blue")
crosshairy = pygame.Surface((1, HEIGHT*2))
crosshairy.fill("Blue")



while True:
    # In pygame, keyboard events can be handled two ways: in the event loop and
    # using pygame.key.get_pressed(). Using the event loop, we can handle combinations
    # of keys by checking if a key was pressed before pressing another key at the same
    # time, essentially checking for a shortcut/hotkey. I will not use it this time
    # as it's outside the scope of the class.

    # Handle exit when escape is pressed
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    # Alternatively,
    # for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         pygame.quit()
        #         exit()

    
    # Get mouse position
    mousepos = pygame.mouse.get_pos()

    # Position crosshair in relation to mouse position
    crosshairx_rect = crosshairx.get_rect(center=mousepos)
    crosshairy_rect = crosshairy.get_rect(center=mousepos)

    # Position text in relation to mouse position.
    # mousepos[] is a tuple of x and y coordinates, mousepos[0] corresponding to x and
    # mousepos [1] to the y coordinate. By positioning the rectangle's top left as the 
    # position of the mouse pointer 
    text_rect = text_surf.get_rect(left=mousepos[0] + 100, top = mousepos[1])
    
    
    # blits
    screen.blit(crosshairy, crosshairy_rect)
    screen.blit(crosshairx, crosshairx_rect)
    screen.blit(image, mousepos)
    screen.blit(text_surf, text_rect)
    pygame.display.update()
    clock.tick(60)

    # Ellipse
    ellipse = pygame.draw.ellipse(background, "Red", text_rect)

    screen.blit(background, (0, 0))
pygame.quit()
exit()